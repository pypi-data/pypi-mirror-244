import docker.models.containers
import click
from click.exceptions import MissingParameter
import os, subprocess

import docker
import logging
import sys
import re, time, signal

logger = logging.getLogger('root')

logger.setLevel(logging.INFO)  # set logger level
logFormatter = logging.Formatter("%(threadName)-34s %(name)-12s %(asctime)s "
                                 "%(levelname)-8s %(filename)s:%(funcName)s %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
consoleHandler = logging.StreamHandler(sys.stdout)  # set streamhandler to stdout
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


def target_valid(target: docker.models.containers.Container, require: str) -> bool:
    """
    :param target: The Docker container to check.
    :param require: The requirement for the container's status. Must be either 'healthy' or 'running'.
    :return: True if the container meets the requirement, False otherwise.
    """
    try:
        target.reload()
    except Exception as e:
        return False
    if require not in ('healthy', 'running'):
        raise RuntimeError("Invalid requirement. Only healthy or running is supported")
    if require == "healthy":
        if target.attrs['State']['Health']['Status'] != "healthy":
            return False
    elif require == "running":
        if target.attrs['State']['Status'] != "running":
            return False
    return True


SHUTDOWN = False


def handle_stop(sig_num, frame):
    """
    :param sig_num: The signal number that was caught.
    :param frame: The current stack frame at the time the signal was caught.
    :return: None

    Handles the stop signal (SIGINT or SIGTERM) by setting the global SHUTDOWN variable to True and logging a message indicating the received signal.
    """

    logger.info(f'Received {sig_num}, stopping...')
    global SHUTDOWN
    SHUTDOWN = True


def setup_signals():
    import signal
    """
    Setup signals for handling SIGINT and SIGTERM.

    :return: None
    """
    signal.signal(signal.SIGINT, handle_stop)
    signal.signal(signal.SIGTERM, handle_stop)


def shutdown_child(process: subprocess.Popen):
    """
    Shuts down a child process gracefully by sending SIGSTOP, SIGTERM, and SIGKILL signals.

    :param process: The subprocess.Popen object representing the child process.
    :return: None
    """
    os.kill(process.pid, signal.SIGSTOP)
    try:
        # Wait for process to finish; Timeout if it doesn't finish in 30 seconds
        process.wait(timeout=30)

    except subprocess.TimeoutExpired:
        print(f'Process {process.pid} did not exit on time, sending SIGTERM...')
        os.kill(process.pid, signal.SIGTERM)
        try:
            # Wait for process to finish; Timeout if it doesn't finish in 30 seconds
            process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            print(f'Process {process.pid} did not exit on time, sending SIGKILL...')
            # Send SIGKILL to the process
            os.kill(process.pid, signal.SIGKILL)


@click.command()
@click.option(
    "--label", prompt=False,
    default=lambda: os.environ.get("INJECTOR_LABEL", ""),
    help="Label to match target container could be either label or label=value or label:value"
)
@click.option(
    "--require", prompt=False,
    default=lambda: os.environ.get("INJECTOR_REQUIRE", "healthy"),
    help="Requirement the target container to be healthy or just running"
)
@click.option(
    "--ns", prompt=False,
    default=lambda: os.environ.get("INJECTOR_NS", None),
    help="Namespaces to inject into divided by comma: --ns=net,uts"
)
@click.option("--proc", prompt=False, default=lambda: os.environ.get("INJECTOR_PROC", '/proc'),
              help="Path to the proc filesystem")
@click.option("--cmd", prompt=False, default=lambda: os.environ.get("INJECTOR_CMD", None),
              help="The command to run in the namespace")
def inject(label, require, ns, proc, cmd):
    if label is None:
        raise MissingParameter("Label is not specified", param=label)
    l = re.split("[:=]", label)
    name = l[0]
    if len(l) == 2:
        value = l[1]
    else:
        value = None
    if ns is None:
        raise MissingParameter("Namespaces are not specified", param=ns)
    nslist = ns.split(',')
    client = docker.from_env()
    if value is None:
        targets = [c for c in client.containers.list(all=True)
                   if name in c.labels.keys()]
    else:
        targets = [c for c in client.containers.list(all=True)
                   if c.labels.get(name, None) == value]
    if len(targets) == 0:
        raise RuntimeError("No target container found")
    if len(targets) > 1:
        raise RuntimeError("Only one target container is supported")
    target = targets[0]
    if not target_valid(target, require):
        raise RuntimeError("Target container is not %s" % require)
    pid = target.attrs['State']['Pid']
    logger.info("Target container: %s" % target.name)
    nsargs = []
    for ns in nslist:
        nsargs.append(f"--{ns}={proc}/{pid}/ns/{ns}")
    logger.info("Namespaces: %s" % nslist)
    command = f'nsenter {" ".join(nsargs)} {cmd}'
    setup_signals()
    process = subprocess.Popen(command, shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    global SHUTDOWN
    while not SHUTDOWN:  # None value indicates that process is not yet finished
        time.sleep(1)  # Wait and then check again
        if not target_valid(target, require):
            logger.info("Target container is not %s" % require)
            break
        if process.poll() is None:
            logger.info("Command exited with return code: %s" % process.returncode)
            return
    shutdown_child(process)


def main():
    inject()


if __name__ == '__main__':
    main()

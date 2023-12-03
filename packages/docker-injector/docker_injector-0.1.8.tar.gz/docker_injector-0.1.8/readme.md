# Docker Namespace Injector

This Python script allows you to inject commands into specified Docker namespaces of a running or healthy Docker container. It is operated through various command-line options.


## **Overview**

The Docker Namespace Injector script offers the following functionalities:

- Identifying a target Docker container using labels.
- Validation checks to ensure that the Docker container state is either 'healthy' or 'running'.
- The ability to set `SIGINT` and `SIGTERM` signal handlers for graceful shutdown upon user request.
- Command injections into specified Docker namespaces of the target Docker container.
- Monitoring the running state of the Docker container and the injected process, and terminating the process when necessary.

## **Usage**

You can control the script execution via the command line:

- `--label`: Specify the label used to identify the target Docker container. This parameter can be defined in either the 'label' or 'label=value' or 'label:value' formats.
- `--require`: Set the requirement for the Docker container’s state. This should be either 'healthy' or 'running'.
- `--ns`: Specify the namespaces to inject. These should be divided by a comma (e.g., '--ns=net,uts').
- `--proc`: Path to the proc filesystem. The default setting is '/proc'.
- `--cmd`: Define the command to run in the Docker container’s namespace.

Most of the command-line parameters can be defined using environment variables:

- `INJECTOR_LABEL`
- `INJECTOR_REQUIRE`
- `INJECTOR_NS`
- `INJECTOR_PROC`
- `INJECTOR_CMD`

## **Code Structure**

The script comprises several functions, each one providing a specific operational feature:

- `target_valid(target: docker.models.containers.Container, require: str) -> bool`: This function checks if the Docker container meets the specified requirement.
- `handle_stop(sig_num, frame)`: Handles the stop signal (SIGINT or SIGTERM) and triggers the required processes.
- `setup_signals()`: Sets up signal handlers for SIGINT and SIGTERM signals.
- `shutdown_child(process: subprocess.Popen)`: Ensures a graceful shutdown of a child process that has been triggered by the script.

The `inject(label, require, ns, proc, cmd)` function initiates the main functionality of the script, using all the helper functions defined above.

## **Running the Code**

Run the script using the following command:

\`\`\`bash
python3 script.py --label=label=value --require=healthy --ns=net --proc=/proc --cmd="command_to_run"
\`\`\`

Make sure to replace the `label=value` parameter with the label of your target Docker container, `net` with the namespace to inject the commands, and `command_to_run` with the specific command you want to run in the selected namespace.
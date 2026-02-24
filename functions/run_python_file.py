import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(
            os.path.join(working_dir_abs, file_path))

        valid_target_path = os.path.commonpath(
            [working_dir_abs, file_path_abs]) == working_dir_abs

        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if os.path.splitext(file_path)[1] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        commands = ["python", file_path_abs]
        if args:
            commands.extend(args)

        completed_process = subprocess.run(
            args=commands,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = []
        if completed_process.returncode != 0:
            output.append(
                f"Process exited with code {completed_process.returncode}")

        if not completed_process.stdout and not completed_process.stderr:
            output.append("No output produced")
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}")
        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"

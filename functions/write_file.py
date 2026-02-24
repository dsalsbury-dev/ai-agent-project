import os


def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(
            os.path.join(working_dir_abs, file_path))

        valid_target_path = os.path.commonpath(
            [working_dir_abs, file_path_abs]) == working_dir_abs

        if not valid_target_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(file_path_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Creates the parent directory path to the file if it does not exsit already. exist_ok just suppresses the error if it already exists.
        os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)

        with open(file_path_abs, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error writing to file: "{file_path}": {e}'

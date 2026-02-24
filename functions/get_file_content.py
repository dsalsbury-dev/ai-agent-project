import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Open file contents in a specified file path relative to the working directory, and return the content as a string. Content is truncated over 10000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path for which data will be read from, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(
            os.path.join(working_dir_abs, file_path))

        valid_target_path = os.path.commonpath(
            [working_dir_abs, file_path_abs]) == working_dir_abs

        if not valid_target_path:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_path_abs, "r") as f:
            content = f.read(MAX_CHARS)
            # Checking if file was larger than the limit. By reading again it checks the next character after the initial MAX_CHARS
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return content
    except Exception as e:
        return f'Error reading file: "{file_path}": {e}'

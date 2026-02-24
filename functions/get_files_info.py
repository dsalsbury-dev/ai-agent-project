import os


def get_files_info(working_directory, directory="."):
    try:
        if not isinstance(directory, str):
            raise Exception(f'"{directory}" is not a directory')

        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # checks to see if the target directory falls within the absolute path of the selected working directory.
        # Don't want the Agent to go outside of the area of influence we give it.
        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            raise Exception(
                f'Cannot list "{directory}" as it is outside the permitted working directory')

        directory_contents = os.listdir(target_dir)
        results = []

        for item in directory_contents:
            item_dir = os.path.join(target_dir, item)
            item_details = f"- {item}: file_size={os.path.getsize(item_dir)}, is_dir={os.path.isdir(item_dir)}"
            results.append(item_details)

        return "\n".join(results)
    except Exception as e:
        return f"\tError: {e}"

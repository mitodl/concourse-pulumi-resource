import os


# =============================================================================
# read_value_from_file
# =============================================================================
def read_value_from_file(file_path: str, working_dir=None) -> str:
    # get original working directory
    original_working_dir = os.getcwd()  # noqa: PTH109
    # change to specified working dir
    if working_dir:
        os.chdir(working_dir)
    # read the contents of the value file
    with open(file_path) as value_file:  # noqa: PTH123
        file_value = value_file.read()
    # trim any trailing newline
    file_value = file_value.rstrip("\n")
    # change back to original working dir
    if os.getcwd() != original_working_dir:  # noqa: PTH109
        os.chdir(original_working_dir)
    return file_value

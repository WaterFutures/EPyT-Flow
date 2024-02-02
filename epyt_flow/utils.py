import tempfile


def get_temp_folder() -> str:
    return tempfile.gettempdir()

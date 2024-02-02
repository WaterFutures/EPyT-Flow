import os
import tempfile


def get_temp_folder(folder_name:str="epyt_flow-test") -> str:
    folder_tmp = os.path.join(tempfile.gettempdir(), folder_name)
    if not os.path.exists(folder_tmp):
        os.mkdir(folder_tmp)
    return folder_tmp

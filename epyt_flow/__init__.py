import sys
import subprocess
import os
import shutil


with open(os.path.join(os.path.dirname(__file__), 'VERSION'), encoding="utf-8") as f:
    VERSION = f.read().strip()


if sys.platform.startswith("linux"):
    path_to_custom_libs = os.path.join(os.path.dirname(__file__), "customlibs")
    path_to_lib_epanet = os.path.join(path_to_custom_libs, "libepanet2_2.so")

    update = False
    if os.path.isfile(path_to_lib_epanet):
        if os.path.getmtime(__file__) > os.path.getmtime(path_to_lib_epanet):
            update = True

    if not os.path.isfile(path_to_lib_epanet) or update is True:
        if shutil.which("gcc") is not None:
            print("Compiling EPANET and EPANET-MSX...")
            path_to_epanet = os.path.join(os.path.dirname(__file__), "EPANET")
            subprocess.check_call(f"cd \"{path_to_epanet}\"; bash compile.sh", shell=True)

import subprocess
import warnings
import shutil
import sys
import os

with open(os.path.join(os.path.dirname(__file__), 'VERSION'), encoding="utf-8") as f:
    VERSION = f.read().strip()
    __version__ = VERSION


def compile_libraries_unix(lib_epanet_name: str, compile_script_name: str,
                           gcc_name: str = "gcc") -> None:
    """Compile EPANET and EPANET-MSX libraries if needed."""
    path_to_custom_libs = os.path.join(os.path.dirname(__file__), "customlibs")
    path_to_lib_epanet = os.path.join(path_to_custom_libs, lib_epanet_name)
    path_to_epanet = os.path.join(os.path.dirname(__file__), "EPANET")

    update = False
    if os.path.isfile(path_to_lib_epanet):
        if os.path.getmtime(__file__) > os.path.getmtime(path_to_lib_epanet):
            update = True

    if not os.path.isfile(path_to_lib_epanet) or update:
        if shutil.which(gcc_name) is not None:
            print("Compiling EPANET and EPANET-MSX...")
            try:
                subprocess.check_call(f"cd \"{path_to_epanet}\"; bash {compile_script_name}",
                                      shell=True)
                print("Done")
            except subprocess.CalledProcessError as ex:
                print(f"Compilation failed\n{ex}")
                warnings.warn("Falling back to pre-compiled library shipped by EPyT.")
        else:
            warnings.warn("GCC is not available to compile the required libraries.\n" +
                          "Falling back to pre-compiled library shipped by EPyT.")


if sys.platform.startswith("linux"):
    compile_libraries_unix("libepanet2_2.so", "compile_linux.sh")
elif sys.platform.startswith("darwin"):
    compile_libraries_unix("libepanet2_2.dylib", "compile_macos.sh", gcc_name="gcc-12")

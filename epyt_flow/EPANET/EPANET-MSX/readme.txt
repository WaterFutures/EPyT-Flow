The EPANET-MSX program is a free software and can be used to model water quality problems involving multiple components. 
EPANET-MSX will only run correctly with release 2.0.12 or higher of the EPANET2 engine. 

CMake (https://cmake.org/) can be used to build EPANETMSX applications. The project's CMake file (CMakeLists.txt) is located in its 
root directory and supports builds for Linux, Mac OS and Windows. To build the EPANETMSX library and its command line executable 
using CMake, first open a console window and navigate to the project's root directory. Then enter the following commands:

mkdir build
cd build
cmake ..
cmake --build . --config Release

Note: under Windows, the third command should be cmake .. -A Win32 for a 32-bit build or cmake .. -A x64 for a 64-bit build 
when Microsoft Visual Studio is the default compiler. 64-bit EPANETMSX application need to work with 64-bit EPANET2 engine. 
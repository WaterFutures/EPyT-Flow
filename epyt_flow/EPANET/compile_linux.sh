#!/bin/bash
mkdir -p "../customlibs/"
gcc -w -O3 -march=native -shared -Wl,-soname,libepanet2_2.so -fPIC -o "../customlibs/libepanet2_2.so" EPANET/SRC_engines/*.c -IEPANET/SRC_engines/include -lc -lm -pthread
gcc -w -O3 -march=native -fPIC -shared -Wl,-soname,libepanetmsx2_2_0.so -o "../customlibs/libepanetmsx2_2_0.so" -fopenmp -Depanetmsx_EXPORTS -IEPANET-MSX/Src/include -IEPANET/SRC_engines/include EPANET-MSX/Src/*.c -Wl,-rpath=. "../customlibs/libepanet2_2.so" -lm -lgomp -lpthread

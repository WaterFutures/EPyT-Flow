#!/bin/bash
mkdir -p "../customlibs/"
gcc-12 -w -O3 -march=native -dynamiclib -fPIC -install_name libepanet2_2.dylib -o "../customlibs/libepanet2_2.dylib" EPANET/SRC_engines/*.c -IEPANET/SRC_engines/include -lc -lm -pthread
gcc-12 -w -O3 -march=native -dynamiclib -fPIC -install_name libepanetmsx2_2_0.dylib -o "../customlibs/libepanetmsx2_2_0.dylib" -fopenmp -Depanetmsx_EXPORTS -IEPANET-MSX/Src/include -IEPANET/SRC_engines/include EPANET-MSX/Src/*.c -L'../customlibs' -lepanet2_2 -lm -lgomp -lpthread

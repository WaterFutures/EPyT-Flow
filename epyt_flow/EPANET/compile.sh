#!/bin/bash
mkdir -p ../customlibs/
gcc -shared -fPIC -o ../customlibs/libepanet2_2.so EPANET/SRC_engines/*.c -lc -lm
gcc -shared -fPIC -o ../customlibs/libepanetmsx2_2_0.so EPANET-MSX/Src/*.c -lc -lgomp -ldl -lepanet2_2 -Wl,-rpath=.

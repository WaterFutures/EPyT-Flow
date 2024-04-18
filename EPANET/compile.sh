#!/bin/bash
mkdir -p ../epyt_flow/customlibs/
gcc -shared -fPIC -o ../epyt_flow/customlibs/libepanet2_2.so EPANET/SRC_engines/*.c -lc -lm
gcc -shared -fPIC -o ../epyt_flow/customlibs/libepanetmsx2_2_0.so EPANET-MSX/Src/*.c -lc -lgomp -ldl -lepanet2_2 -Wl,-rpath=.

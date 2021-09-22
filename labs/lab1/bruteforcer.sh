#!/bin/bash
# James Raphael Tiovalen / 1004555

for i in {0..255}; do
    echo "CURRENT KEY: $i"
    python3 ex2.py -i flag -o out -k $i -m d
    file out
    echo ""
done

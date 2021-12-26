#!/bin/sh

if [ "$#" -ne 1 ] # number of args must be 1
then
    echo "Usage: $0 [number]"
else
    for i in `seq $1`; do python3 GeneraTabelle.py; done
fi

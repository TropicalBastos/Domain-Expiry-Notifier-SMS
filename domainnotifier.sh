#!/bin/bash

cd src

if [ "$1" == "--background" ]; then
    python main.py > /dev/null &
else
    python main.py
fi
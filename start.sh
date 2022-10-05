#!/bin/bash
log=/proc/1/fd/1

cd ./webserver 
python3 main.py > $log 2>&1 &
cd ..

python3 SaveTheWorldClaimer.py > $log 2>&1

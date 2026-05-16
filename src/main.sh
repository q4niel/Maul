#!/bin/bash

task=main

while getopts "t:" opt; do
    case "$opt" in
        t) task="$OPTARG" ;;
        *) echo "Usage: ???"; exit 1 ;;
    esac
done

printf '\033[2J\033[H'
python3 "tsk/$task.py"
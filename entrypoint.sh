#!/bin/bash
# git reset --hard origin/master ; 
# git pull origin master --force
git pull origin master

# Execute the Python script with all arguments passed to this script
exec python main.py "$@"

# `./entrypoint.sh arg1 "arg 2" arg3` => "python main.py "$@" => `python main.py arg1 "arg 2" arg3`
#!/bin/bash

# Check for correct number of arguments
if [ "$#" -ne 1 ]; then
  echo "You must enter exactly 1 command line argument."
  echo "Use the '-help' option to see options!"
  exit 1
fi

if [ "$1" == "-help" ]; then
  echo "Use 'install' to install server"
  echo "    'start' to start the server"
  echo "    'test' to run server tests"
  echo "    'clean' to clean (remove) install"
elif [ "$1" == "install" ]; then
  echo "Installing flask server environment"
  pip3 install virtualenv
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  pip install -e .
  deactivate
elif [ "$1" == "start" ]; then
  source venv/bin/activate
  # Set up variables from .env file
  export $(grep -v '^#' .env | xargs -d '\n')
  python -m regex_server.app localhost 8000
  deactivate
elif [ "$1" == "test" ]; then
  source venv/bin/activate
  touch test_output.txt
  # Set up variables from .env file
  export $(grep -v '^#' .env | xargs -d '\n')
  python -m pytest ./tests > test_output.txt
  deactivate
elif [ "$1" == "clean" ]; then
  echo "Cleaning install..."
  rm -r __pycache__
  rm -r .pytest_cache
  rm -r venv
  rm test_output.txt
  rm test_database.db
else
  echo "Invalid command line argument!"
  echo "Use the '-help' command to see options!"
  exit 1
fi

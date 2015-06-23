#! /bin/bash

# Remove nasty .pyc files
rm -f *.pyc
find ai/ -name *.pyc -delete

# Run the test suite
export PYTHONPATH=ai
virtualenv/bin/flake8 -v ai
virtualenv/bin/nosetests tests

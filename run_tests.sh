#! /bin/bash

# Remove nasty .pyc files
rm -f *.pyc
find ai/ -name *.pyc -delete

# Run the test suite
export PYTHONPATH=ai
virtualenv/bin/nosetests tests
virtualenv/bin/flake8 -v tests

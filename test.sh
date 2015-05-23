#! /bin/bash

# Remove nasty .pyc files
rm -f *.pyc
find agent/ -name *.pyc -delete

# Run the test suite
export PYTHONPATH=agent
virtualenv/bin/nosetests tests
virtualenv/bin/flake8 -v tests

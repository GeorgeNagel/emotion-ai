#! /bin/bash

# Remove nasty .pyc files
rm -f *.pyc
find agent/ -name *.pyc -delete

# Run the test suite
virtualenv/bin/nosetests agent
virtualenv/bin/flake8 -v agent

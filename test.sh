#! /bin/bash

virtualenv/bin/nosetests agent
virtualenv/bin/flake8 -v agent

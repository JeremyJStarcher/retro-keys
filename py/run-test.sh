#!/bin/sh

#python -m unittest parser_test.py
python -m unittest discover -s tests/ -v -cov

#!/usr/bin/env python3
import subprocess

python3_command = "matrixfactorization.py"  # launch your python2 script using bash

process = subprocess.Popen('matrixfactorization.py', stdout=subprocess.PIPE)
output, error = process.communicate()  # receive output from the python2 script
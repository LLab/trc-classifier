#!/usr/bin/python
import os, sys

numTests = int(sys.argv[1])
turnOff = sys.argv[2:]

files = ['tmp/testing_' + str(x) + '.out' for x in range(1,numTests+1)]

os.system('python makeConcise.py ' + ' '.join(files) + ' > results' + '_'.join(turnOff))

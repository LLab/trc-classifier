#!/usr/bin/python
import os, sys

num = sys.argv[1]
turnOffs = sys.argv[2:]

for eachTurnOff in turnOffs:
   line = ['python', 'trainer.py', num, eachTurnOff, '&&', 'python', 'evaluate.py', num, eachTurnOff]
   print ' '.join(line)
   os.system(' '.join(line))

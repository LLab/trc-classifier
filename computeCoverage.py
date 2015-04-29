#!/usr/bin/python

import sys, crfForCodeSwitching as c
num = int(sys.argv[1])

ddd = {'0':0, '1': 0}
for i in range(1, num+1):
   fileName = 'trc_data_'+str(i)+'_clean'
   lines = c.getLinesFromCorpus(fileName)
   for eachLine in lines:
      words = c.getWordsFromLine(eachLine)
      for eachWord in words:
         (w, a) = c.getAnswer(eachWord)
         if a != 'O':
            continue
         r = c.wordlistFeature(eachWord)
         ddd[r[0]] += 1

print ddd

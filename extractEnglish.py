#!/usr/bin/python

import re, sys, os, string, crfForCodeSwitching as cf


def pickWord(s):
   PREFIX = cf.getWordPrefix()
   l = s.split('\t')
   return cf.getFirstEngWord(l[1][len(PREFIX):])[0]


def recognize(l, c, i):
   toReturn = [pickWord(c[i])]
   ind = int()
   for ind in range(i+1, len(l)):
      if not l[ind].startswith('I'):
         break
      toReturn.append(pickWord(c[ind]))
   return (' '.join(toReturn), ind)


server = None


def getItParsed(s):
   if s is None or len(s) is 0:
      return None
   import jsonrpclib
   from simplejson import loads
   global server
   if server is None:
      server = jsonrpclib.Server("http://localhost:8080")
   result = loads(server.parse(s))
   return result


if __name__ == '__main__':
   corpus = sys.argv[1]
   predicted = sys.argv[2]
   corpusLines = [x for x in open(corpus).read().split('\n')]
   predictedLines = [x for x in open(predicted).read().split('\n')]

   recognizedPhrases = [None] * len(predictedLines)
   recognized = ''
   for i in range(len(predictedLines)):
      if predictedLines[i].startswith('B'):
         (recognized, endpoint) = recognize(predictedLines, corpusLines, i)
         for j in range(i, endpoint):
            recognizedPhrases[j] = recognized
         i = endpoint
   
   recognizedAndParsed = [getItParsed(s) for s in recognizedPhrases]
   
   for r in recognizedAndParsed:
      if r is None or r.get('sentences', None) is None or len(r['sentences']) < 1:
         print 'None'
         continue
      print r['sentences'][0]['dependencies']


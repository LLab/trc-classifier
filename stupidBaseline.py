#!/usr/bin/python

import crfForCodeSwitching, sys, string, re

def getAnswers(currentAnswers, isEng):
   if not isEng:
      return 'O'
   if len(currentAnswers) == 0:
      return 'B'
   if currentAnswers[-1] == 'O':
      return 'B'
   return 'I'


def getCorrectCount(l1, l2, c):
   if len(l1)!=len(l2) or len(c) == 0:
      return 0
   toReturn = 0
   for i in range(len(l1)):
      if l1[i] == l2[i] and l1[i] == c:
         toReturn+=1
   return toReturn


if __name__ == '__main__':
   refO = 0
   modO = 0
   corrO = 0
   refB = 0
   modB = 0
   corrB = 0
   refI = 0
   modI = 0
   corrI = 0
   lines = crfForCodeSwitching.getLinesFromCorpus(sys.argv[1])
   for eachLine in lines:
      refAnswers = list()
      answers = list()
      words = crfForCodeSwitching.getWordsFromLine(eachLine)
      for eachWord in words:
         isE = False
         (word, answer) = crfForCodeSwitching.getAnswer(eachWord)
         if answer.endswith('P'):
            answer = 'O'
         # is English word a substring?
         # (extractedEng, pos) = crfForCodeSwitching.getFirstEngWord(word.lower())
         # if len(extractedEng) > 0:
         #    isE = True
         enOrZu = crfForCodeSwitching.langidFeature(eachWord)
         if enOrZu == 'en':
            isE = True
         refAnswers.append(answer)
         answers.append(getAnswers(answers, isE))
      refO += refAnswers.count('O')
      modO += answers.count('O')
      corrO += getCorrectCount(refAnswers, answers, 'O')
      refB += refAnswers.count('B')
      modB += answers.count('B')
      corrB += getCorrectCount(refAnswers, answers, 'B')
      refI += refAnswers.count('I')
      modI += answers.count('I')
      corrI += getCorrectCount(refAnswers, answers, 'I')
   print 'refO:\t' + str(refO)
   print 'modO:\t' + str(modO)
   print 'corrO:\t' + str(corrO)
   print 'prec:\t' + str(1.0*corrO/modO)
   print 'recall:\t' + str(1.0*corrO/refO)
   print 'refI:\t' + str(refI)
   print 'modI:\t' + str(modI)
   print 'corrI:\t' + str(corrI)
   print 'prec:\t' + str(1.0*corrI/modI)
   print 'recall:\t' + str(1.0*corrI/refI)
   print 'refB:\t' + str(refB)
   print 'modB:\t' + str(modB)
   print 'corrB:\t' + str(corrB)
   print 'prec:\t' + str(1.0*corrB/modB)
   print 'recall:\t' + str(1.0*corrB/refB)

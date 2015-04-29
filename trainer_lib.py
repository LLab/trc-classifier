import os

def createAllCRFs(cleanFiles, trainingFiles, turnOff):
   if len(cleanFiles) != len(trainingFiles):
      return
   for i in range(len(cleanFiles)):
      print('python crfForCodeSwitching.py ' + cleanFiles[i] + ' ' + ' '.join(turnOff) + ' ' + ' > ' + trainingFiles[i])
      os.system('python crfForCodeSwitching.py ' + cleanFiles[i] + ' ' + ' '.join(turnOff) + ' ' + ' > ' + trainingFiles[i])


def aggregateFiles(toAggregate, target):
   to_cat = ' '.join(toAggregate)
   print('cat ' + to_cat + ' > ' + target)
   os.system('cat ' + to_cat + ' > ' + target)


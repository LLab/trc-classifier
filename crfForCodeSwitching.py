#!/usr/bin/python

import sys,re

ZE_ENCODING = True

def getLinesFromCorpus(fileName):
        fh = open(fileName)
	return [x for x in fh.read().split('\n') if len(x)>0]
        fh.close()


def getWordsFromLine(line):
	p = re.compile('\s+')
	return [x for x in p.split(line) if len(x)>0]


zuluDictionary = None
affixDict = None

def getZuluDictionary():
	fileName = '2010.07.17.AnalysisList.txt'
	global zuluDictionary
	if zuluDictionary == None:
	        with open(fileName) as fh:
		        p = re.compile('<.*?>')
		        zuluDictionary = set([p.sub('', x) for x in fh.read().split()])	
	return zuluDictionary


def getAffixDict():
	fileName = '2010.07.17.AnalysisList.txt'
	global affixDict
	if affixDict == None:
		affixDict = dict()
		p = re.compile('<.*?>')
		opened = open(fileName).read().split()
		for eachLine in opened:
			tags = p.findall(eachLine)
			morphemes = p.split(eachLine)
			for i in range(len(tags)):
				if tags[i].endswith('vr>') or tags[i].endswith('nr>') or tags[i].endswith('ar>'):
					continue
				if len(morphemes[i]) < 2 and re.match('[aeiou]', morphemes[i]) == None:
					continue
				affixDict.setdefault(tags[i], set()).add(morphemes[i])
	return affixDict


def getEncodedAffixFeatures(encodedDict):
	universe = getAffixDict().keys()
	myTags = set(encodedDict.keys())

	toReturn = list()

	for eachTag in universe:
		if eachTag in myTags:
			toReturn.extend([eachTag, encodedDict.get(eachTag)])
		else:
			toReturn.extend(['NONE', 'NONE'])
	
	return toReturn


def getEncodedDict(st, usedTags):
	if len(st) is 0 or st is None:
		return dict()

	universeDict = getAffixDict()

	candidate = None

	for eachTag in universeDict:
		if eachTag in usedTags:
			continue
		morphemes = universeDict.get(eachTag)
		for eachMorph in morphemes:
			if st.startswith(eachMorph):
				# print st + ' starts with ' + eachMorph
				trial = getEncodedDict(st[len(eachMorph):], usedTags.union({eachTag}))
				if trial is not None:
					trial.update({eachTag: eachMorph})
					if candidate is None or len(candidate) > len(trial):
						candidate = trial
	
	return candidate


def wordlistFeature(w):
	if w in getZuluDictionary():
		return ['1']
	return ['0']

def substr(string):
    j=1
    a=set()
    while True:
        for i in range(len(string)-j+1):
            a.add(string[i:i+j])
        if j==len(string):
            break
        j+=1
        #string=string[1:]
    return a


dictSet = None
def isInEngDictFile(w):
   global dictSet
   if dictSet is None:
      dictFile = '/usr/share/dict/words'
      dictSet = set(open(dictFile).read().split())
   if w in dictSet:
      return True
   return False


def isEnglishWord(w):
	from nltk.corpus import wordnet
	if not wordnet.synsets(w):
		return isInEngDictFile(w)
	return True


def getFirstEngWord(w):
	toReturn = ''
	s = substr(w)
	for x in s:
	        if len(x) <= len(w) / 2:
	           continue
		# if len(w) - len(x) > 5:
		#   continue
		if isEnglishWord(x) and len(x) > len(toReturn):
		   toReturn = x
	from nltk.corpus import wordnet
	pos = ['2', '2', '2', '2', '2']

        # TODO testing
        # return (toReturn, pos)
        # TODO end testing

	if len(toReturn) > 0:
		pos = ['0', '0', '0', '0', '0']
		poses = {x.pos for x in wordnet.synsets(toReturn)}
		if 'n' in poses:
			pos[0] = '1'
		if 'v' in poses:
			pos[1] = '1'
		if 'a' in poses:
			pos[2] = '1'
		if 'r' in poses:
			pos[3] = '1'
		if 's' in poses:
			pos[4] = '1'
		
	return (toReturn, pos)


def engFeature(w):
	toReturn = list()
	(first, pos) = getFirstEngWord(w)
	
	# contains english word?
	if len(first) > 0:
		toReturn.extend(['1'])
		toReturn.extend([first])
	else:
		toReturn.extend(['0'])
		toReturn.extend(['NONE'])
	
	toReturn.extend(pos)

	# get prefix before word
	if len(first)>0:
		prefix = w.split(first)[0]
		suffix = w.split(first)[-1]
	else:
		prefix = ''
		suffix = ''
	
	encodedPreDict = getEncodedDict(prefix, set())
	if encodedPreDict is None:
		encodedPreDict = dict()
		preFeatures = ['NOVALIDAFFIX']
	else:
		preFeatures = ['HASAFFIX']

	encodedSufDict = getEncodedDict(suffix, set())
	if encodedSufDict is None:
		encodedSufDict = dict()
		sufFeatures = ['NOVALIDAFFIX']
	else:
		sufFeatures = ['HASAFFIX']
	preFeatures.extend(getEncodedAffixFeatures(encodedPreDict))
	sufFeatures.extend(getEncodedAffixFeatures(encodedSufDict))
	
	toReturn.extend(preFeatures)
	toReturn.extend(sufFeatures)

	return toReturn


def affixFeature(w):
	NUM_PREFIX_CONST = 7
	NUM_SUFFIX_CONST = 5

	toReturn = list()
	
	# prefix
	for i in range(NUM_PREFIX_CONST):
		if i + 1 > len(w):
			toReturn.append('LESS')
		else:
			toReturn.append(w[:i+1])
	
	# suffix
	for i in range(NUM_SUFFIX_CONST):
		if i + 1 > len(w):
			toReturn.append('LESS')
		else:
			toReturn.append(w[-(i+1):])
	
	return toReturn


def langidFeature(word):
	import langid
	langid.set_languages(['zu','en'])
	return langid.classify(word)[0]


allBigrams = None

def getAllBigrams():
   import string
   global allBigrams
   if allBigrams is None:
      allBigrams = set()
      for i in string.lowercase:
         for j in string.lowercase:
            allBigrams.add(i+j)
   return allBigrams


def getBigramsFromWord(w):
   import string
   toReturn = set()
   word = string.lower(w)
   for i in range(len(word)-1):
      toReturn.add(word[i] + word[i+1])

   return toReturn


def getBigramFeatures(w):
   toReturn = list()
   universe = getAllBigrams()
   theBigrams = getBigramsFromWord(w)
   for bi in universe:
      if bi in theBigrams:
         toReturn.append(bi)
      else:
         toReturn.append('NONE')
   return toReturn

allTrigrams = None

def getAllTrigrams():
   import string
   global allTrigrams
   if allTrigrams is None:
      allTrigrams = set()
      for i in string.lowercase:
         for j in string.lowercase:
            for k in string.lowercase:
               allTrigrams.add(i+j+k)
   return allTrigrams


def getTrigramsFromWord(w):
   import string
   toReturn = set()
   word = string.lower(w)
   for i in range(len(word)-2):
      toReturn.add(word[i] + word[i+1] + word[i+2])

   return toReturn


def getTrigramFeatures(w):
   toReturn = list()
   universe = getAllTrigrams()
   theTrigrams = getTrigramsFromWord(w)
   for tri in universe:
      if tri in theTrigrams:
         toReturn.append(tri)
      else:
         toReturn.append('NONE')
   return toReturn


usingCRFSuite = True

usingLR = False

featureVocab = None

def getSVMFeature(s):
   global featureVocab
   import shelve
   if featureVocab is None:
      featureVocab = shelve.open('featureVocab.shelf')
   return str(featureVocab.setdefault(s,len(featureVocab)+1))+':1'

def addNonExistentFeats(someSet):
   global featureVocab
   toReturn = set(someSet)
   for i in range(0, len(featureVocab)):
      if str(i+1)+':1' not in someSet:
         toReturn.add(str(i+1)+':0')
   return toReturn

def getFeaturesOf(w, t, turnOff):
	l = list()

	# incorporate treetagger results
        if 'treeTagger' not in turnOff:
           l.extend(t)

	# get bigram features
        if 'bigram' not in turnOff:
           l.extend(getBigramFeatures(w))

	# get trigram features
	# l.extend(getTrigramFeatures(w))

	# in Zulu wordlist?
        if 'wordList' not in turnOff:
           l += wordlistFeature(w)

	# output from langid
        if 'langid' not in turnOff:
           l.append(langidFeature(w))

	# affix on entire word
        if 'affixFeature' not in turnOff:
           l += affixFeature(w)

	# in English wordlist?
        if 'engFeature' not in turnOff:
           l += engFeature(w)

        if usingCRFSuite:
           newL = list()
           for i in range(len(l)):
              # if l[i].endswith('NONE'):
              #    continue
              newL.append('FEAT_'+str(i)+'='+l[i])
           return ('\t'.join(newL), len(newL))
        elif usingLR:
           newL = set()
           for i in range(len(l)):
              newL.add(getSVMFeature('FEAT_'+str(i)+'='+l[i]))

           # add wordform to features for SVM format
           newL.add(getSVMFeature(getWordPrefix()+w))
           fixed = addNonExistentFeats(newL)
           return ('\t'.join(fixed), len(fixed))
        else:
           return ('\t'.join(l), len(l))


def getAnswer(w):
	if len(w) is 0:
		return (w, '')

	answers = w.split('_')
	if len(answers) is 1:
		answers.append('O')
	
	return ((answers[0][0].lower() + answers[0][1:]), answers[1])


def getResultsFromTreeTagger(toTag):
        tagger = 'tree-tagger/cmd/tree-tagger-english'
	import subprocess
	# print 'tagging ' + toTag
	p = subprocess.Popen('echo \"' + toTag + '\"' + ' | {}'.format(tagger), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	results = p.stdout.readlines()
	# print results
	stripped_results = [s.strip() for s in results]
	stripped = stripped_results[3:]
	toReturn = list()
	for eachStripped in stripped:
		lstStripped = [x for x in eachStripped.split() if len(x.strip())>0]
		# print 'to append: ' + str(lstStripped)
		toReturn.append( (lstStripped[1], lstStripped[2]) )
	return toReturn


def tag(sentence):
	toTag = ' '.join(sentence)
	return getResultsFromTreeTagger(toTag)


def getWordPrefix():
   return 'WORD_'


def getSVMLabel(a):
   global ZE_ENCODING
   if ZE_ENCODING:
      if a == 'O' or a == 'OB':
         return '0'
      else:
         return '1'

   if a == 'O':
      return '0'
   elif a == 'B':
      return '1'
   elif a == 'I':
      return '2'
   elif a == 'OB':
      return '3'
   else:
      return '4'


def getLine(w, f, a):
   if usingCRFSuite == True:
      return '\t'.join((a, getWordPrefix()+w, f))
   elif usingLR == True:
      return '\t'.join((getSVMLabel(a), f))
   else:
      return '\t'.join((w,f,a))


def fixOBTagging(words):
   if len(words) == 0:
      return words
   toReturn = list()
   if ZE_ENCODING:
      for word in [getAnswer(w) for w in words]:
         if word[1] == 'O' or word[1] == 'OB':
            toAppend = word[0] +  '_O'
         else:
            toAppend = word[0] + '_I'
         toReturn.append(toAppend)
      return toReturn
   toReturn.append(words[0])
   for i in range(1, len(words)):
      if getAnswer(words[i])[1] == 'O' and (getAnswer(words[i-1])[1] == 'B' or getAnswer(words[i-1])[1] == 'I'):
         toReturn.append(words[i]+'_OB')
      else:
         toReturn.append(words[i])
   return toReturn


if __name__ == '__main__':
	lines = getLinesFromCorpus(sys.argv[1])
        turnOff = sys.argv[2:]
	numFeatures = 0
	flag = 1
	for eachLine in lines:
		words = getWordsFromLine(eachLine)
		words = fixOBTagging(words)
		asASentence = [getAnswer(w)[0] for w in words]
		treeTaggerResults = tag(asASentence)

		taggedWords = list()
		for i in range(len(words)):
			taggedWords.append( (words[i], treeTaggerResults[i]) )

                outputBuffer = list()
                lastBuffer = list()
		for (eachWord, eachTag) in taggedWords:
			(word, answer) = getAnswer(eachWord)
			(feat, length) = getFeaturesOf(word, eachTag, turnOff)
			outputBuffer.append(getLine(word, feat, answer))
			lastBuffer.append(getLine(word, feat, answer))
			if length != numFeatures:
				if numFeatures == 0:
					numFeatures = length
				else:
					flag = 0

                if usingCRFSuite:
                   # we have to unroll ourselves...
                   for i in range(len(outputBuffer)):
                      if i > 0:
                         last = lastBuffer[i-1]
                         lastFeatures = [x + '_LAST_' for x in last.split()]
                         outputBuffer[i] += ('\t' + '\t'.join(lastFeatures))

                         # outputBuffer[i] += '\t-1:'+wordFormNeighbors[i-1]
                         # outputBuffer[i] += '\tT-1:'+tagNeighbors[i-1]
                      '''
                      if i > 1:
                         outputBuffer[i] += '\tT-2:'+tagNeighbors[i-2]
                         # outputBuffer[i] += '\t-2:'+wordFormNeighbors[i-2]
                      if i < len(outputBuffer)-1:
                         outputBuffer[i] += '\tT+1:'+tagNeighbors[i+1]
                         # outputBuffer[i] += '\t+1:'+wordFormNeighbors[i+1]
                      if i < len(outputBuffer)-2:
                         outputBuffer[i] += '\tT+2:'+tagNeighbors[i+2]
                         # outputBuffer[i] += '\t+2:'+wordFormNeighbors[i+2]
                      '''
                   outputBuffer[0] += '\t___BOS___'
                   outputBuffer[-1] += '\t___EOS___'
                for eachOutputLine in outputBuffer:
                   print eachOutputLine
		print ''

	if flag is 0 and not usingCRFSuite and not usingLR:
		print 'sth wrong'
	else:
		import crfTemplateGenerator as tg
		tg.generator(numFeatures+1, 'template')

        if featureVocab is not None:
           featureVocab.close()

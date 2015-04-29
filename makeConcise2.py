#!/usr/bin/python
import sys,re,string


numB = 0
numI = 0
numO = 0

b1 = 0
b2 = 0
b3 = 0

o1 = 0
o2 = 0
o3 = 0

i1 = 0
i2 = 0
i3 = 0

for i in range(1,len(sys.argv)):
	lines = open(sys.argv[i]).read().split('\n')
	for eachLine in lines:
		if eachLine == '':
			print eachLine
			continue
		words = eachLine.split('\t')
		if words[-2] == 'B' and words[-1] == 'B':
			b1 += 1
		if words[-2] == 'B' and words[-1] != 'B':
			b2 += 1
		if words[-2] != 'B' and words[-1] == 'B':
			b3 += 1

		if words[-2] == 'I' and words[-1] == 'I':
			i1 += 1
		if words[-2] == 'I' and words[-1] != 'I':
			i2 += 1
		if words[-2] != 'I' and words[-1] == 'I':
			i3 += 1

		if words[-2] == 'O' and words[-1] == 'O':
			o1 += 1
		if words[-2] == 'O' and words[-1] != 'O':
			o2 += 1
		if words[-2] != 'O' and words[-1] == 'O':
			o3 += 1

		if words[-2] == 'B':
			numB+=1
		if words[-2] == 'I':
			numI+=1
		if words[-2] == 'O':
			numO+=1
		print words[0]+'\t'+words[-2]+'\t'+words[-1]

print 'B: ' + str(numB) + ' I: ' + str(numI) + ' O: ' + str(numO)
print 'B recall: '
print (b1*1.0/(b1+b3))
print 'B precision: '
print (b1*1.0/(b1+b2))
print 'I recall: '
print (i1*1.0/(i1+i3))
print 'I precision: '
print (i1*1.0/(i1+i2))
print 'O recall: '
print (o1*1.0/(o1+o3))
print 'O precision: '
print (o1*1.0/(o1+o2))

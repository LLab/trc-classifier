#!/usr/bin/python
import sys

def generator(i, fileName):
	templateFile = open(fileName, 'w+')
	print >>templateFile,'A:%x[-2,0]'
	print >>templateFile,'B:%x[-1,0]'
	print >>templateFile,'C:%x[0,0]'
	print >>templateFile,'D:%x[1,0]'
	print >>templateFile,'E:%x[2,0]'

	for i in range(i):
		print >>templateFile,'U'+str(i)+':%x[0,'+str(i)+']'
	print >>templateFile,'B'

	templateFile.close()

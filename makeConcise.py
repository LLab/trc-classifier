#!/usr/bin/python
import sys,re,string

b1 = 1e-15
b2 = 1e-15
b3 = 1e-15

o1 = 1e-15
o2 = 1e-15
o3 = 1e-15

i1 = 1e-15
i2 = 1e-15
i3 = 1e-15

oRecognizer = re.compile('O:\s\((\d+),\s(\d+),\s(\d+)\)')
iRecognizer = re.compile('I:\s\((\d+),\s(\d+),\s(\d+)\)')
bRecognizer = re.compile('B:\s\((\d+),\s(\d+),\s(\d+)\)')

for i in range(1,len(sys.argv)):
	lines = open(sys.argv[i]).read().split('\n')
	for eachLine in lines:
	   o_s = oRecognizer.findall(eachLine)
           if len(o_s) > 0:
              o1 += int(o_s[0][0])
              o2 += int(o_s[0][1])
              o3 += int(o_s[0][2])

	   i_s = iRecognizer.findall(eachLine)
           if len(i_s) > 0:
              i1 += int(i_s[0][0])
              i2 += int(i_s[0][1])
              i3 += int(i_s[0][2])

	   b_s = bRecognizer.findall(eachLine)
           if len(b_s) > 0:
              b1 += int(b_s[0][0])
              b2 += int(b_s[0][1])
              b3 += int(b_s[0][2])

print 'B: ' + str(b3) + ' I: ' + str(i3) + ' O: ' + str(o3)
print 'B precision: '
print (b1*1.0/(b2))
print 'B recall: '
print (b1*1.0/(b3))
print 'I precision: '
print (i1*1.0/(i2))
print 'I recall: '
print (i1*1.0/(i3))
print 'O precision: '
print (o1*1.0/(o2))
print 'O recall: '
print (o1*1.0/(o3))

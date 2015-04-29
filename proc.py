#!/usr/bin/python
import sys,re, string

raw_trc = open(sys.argv[1]).read().split('\n')

p = re.compile("[" + re.escape(string.punctuation) + "]")

output = list()
for eachLine in raw_trc:
	if not eachLine.isspace():
		filtered = [x for x in p.split(eachLine) if not re.match('^\s*$', x)]
		for eachFiltered in filtered:
			output.append(eachFiltered.strip())
			# output.extend([x for x in eachFiltered.split()])
			#if output[-1] != '':
			#	output.append('')

print '\n'.join(output)

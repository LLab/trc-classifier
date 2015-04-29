#!/usr/bin/python

import os, sys, trainer_lib

# number of texts
num = int(sys.argv[1])
turnOff = sys.argv[2:]
usingCRFSuite = True

allCleanFiles = ['data/trc_data_' + str(x) + '_clean' for x in range(1, num+1)]
allTrainingFiles = ['tmp/trc_data_' + str(x) + '_clean.crf' for x in range(1, num+1)]
trainer_lib.createAllCRFs(allCleanFiles, allTrainingFiles, turnOff)

for i in range(1, num+1): 

	# concat training texts
	training_files = [x for x in allTrainingFiles if x != 'tmp/trc_data_' + str(i) + '_clean.crf']

	# make crf format
	training_agg = 'tmp/training_' + str(i)
	training_agg_crf = training_agg + '.crf'
	training_agg_model = training_agg + '.model'
	trainer_lib.aggregateFiles(training_files, training_agg_crf)
	if usingCRFSuite:
	    print('crfsuite learn -m ' + training_agg_model + ' ' + training_agg_crf)
	    os.system('crfsuite learn -m ' + training_agg_model + ' ' + training_agg_crf)
        else:
	    print('crf_learn template ' + training_agg_crf + ' ' + training_agg_model)
	    os.system('crf_learn template ' + training_agg_crf + ' ' + training_agg_model)

	test_file_crf = 'tmp/trc_data_' + str(i) + '_clean.crf'
	test_file_out = 'tmp/testing_' + str(i) + '.out'

	if usingCRFSuite:
	    print('crfsuite tag -t -m ' + training_agg_model + ' ' + test_file_crf + ' > ' + test_file_out)
	    os.system('crfsuite tag -t -m ' + training_agg_model + ' ' + test_file_crf + ' > ' + test_file_out)
        else:
	    print('crf_test -m ' + training_agg_model + ' ' + test_file_crf + ' > ' + test_file_out)
	    os.system('crf_test -m ' + training_agg_model + ' ' + test_file_crf + ' > ' + test_file_out)

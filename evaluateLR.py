#!/usr/local/bin/python
import sys,re,trainer_lib

def invokeLR(training_agg, test_file, output_file, training_model ):
   import os
   print 'java -jar weka/LR.jar ' + training_agg + ' ' + test_file + ' ' + training_model + ' > ' + output_file
   os.system('java -jar weka/LR.jar ' + training_agg + ' ' + test_file + ' ' + training_model + ' > ' + output_file)

num = int(sys.argv[1])

allCleanFiles = ['trc_data_' + str(x) + '_clean' for x in range(1, num+1)]
allTrainingFiles = ['/tmp/trc_data_' + str(x) + '_clean.libsvm' for x in range(1, num+1)]
trainer_lib.createAllCRFs(allCleanFiles, allTrainingFiles, [])


for i in range(1, num+1): 
        test_file = '/tmp/trc_data_' + str(i) + '_clean.libsvm'
	# concat training texts
	training_files = [x for x in allTrainingFiles if x != test_file]
	training_agg = '/tmp/training_' + str(i) + '.libsvm'
	training_model = training_agg+'.model'
	trainer_lib.aggregateFiles(training_files, training_agg)
	output_file = '/tmp/trc_data_'+str(i)+'.out'
	# invokeLR(training_agg,test_file,output_file, training_model)


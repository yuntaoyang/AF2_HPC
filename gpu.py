#!/usr/bin/env python
# coding: utf-8

af2_script = ''
af2_data = ''
path_fasta = ''
path_out = ''
path_log = ''

logname = 'logfile'
max_template_date = '2022-03-10'
file_name = '' # a csv file with a column for file name and a column for length
n_tasks =  # number of tasks in parallel (1 or 2)
gpu_1 = '' # gpu for the first task
gpu_2 = '' # gpu for the second task

# 2 parameters for monomer and multimer
# 'monomer_ptm' & 'model_1,model_2,model_3,model_4,model_5' 
# 'multimer' & 'model_1_multimer,model_2_multimer,model_3_multimer,model_4_multimer,model_5_multimer'
parameter_1 = ''
parameter_2 = ''

import subprocess
import os
import logging
import pandas as pd

def divide_chunks(l, n):    
    for i in range(0, len(l), n): 
        yield l[i:i + n] 

def parallelfold_gpu(f,n):
    script = ['bash',af2_script+'run_alphafold.sh',
              '-d',af2_data,
              '-o',path_out,
              '-p',parameter_1,
              '-m',parameter_2,
              '-i',path_fasta+f+'.fasta',
              '-t',max_template_date,
              '-u',n,
              '>',path_log+f+'.log'+' '+'2>&1']
    return ' '.join(script)

if __name__ == "__main__":
    # define logfile
    logging.basicConfig(level=logging.DEBUG, 
                        filename=logname, 
                        filemode="a",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logger = logging.getLogger(__name__)
    logger.info("parallelfold start!")
    
    # directory for log files
    if not os.path.exists(path_log):
        os.mkdir(path_log)
        
    # divide jobs into chunks
    job = pd.read_csv(file_name)
    files_chunk = list(divide_chunks(job['file'].tolist(), n_tasks))
    
    # run af2
    for files in files_chunk:
        commands = []
        if len(files) == 2:
            commands.append(parallelfold_gpu(files[0],gpu_1))
            commands.append(parallelfold_gpu(files[1],gpu_2))
        else:
            commands.append(parallelfold_gpu(files[0],gpu_1))
        procs = [subprocess.Popen(i,shell=True,cwd=af2_script,
                                  stdout=subprocess.PIPE,stderr=subprocess.STDOUT) for i in commands]
        for p in procs:
            p.communicate()
        for file in files:
            logger.info(file+" is done!")

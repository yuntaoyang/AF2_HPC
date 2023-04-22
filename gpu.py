#!/usr/bin/env python
# coding: utf-8

# Run 2 AF2 jobs in parallel
# --s: the directory of AF2 script
# --d: the directory of AF2 data
# --m: monomer or multimer
# --t: max template date
# --u1: gpu for the first job 
# --u2: gpu for the second job

import os
import argparse
import logging
import subprocess
import pandas as pd

def script(file,arg_s,arg_d,p,arg_t,m,u):
    script = ['bash',os.path.join(arg_s,'run_alphafold.sh'),
              '-d',arg_d,
              '-o','./out/',
              '-p',p,
              '-i',os.path.join('./fasta/',file),
              '-t',arg_t,
              '-m',m,
              '-u',u,'>',
              os.path.join('./log_gpu/',file.replace('.fasta','.log')),'2>&1']
    return ' '.join(script)

def divide_chunks(l, n):    
    for i in range(0, len(l), n): 
        yield l[i:i + n] 
        
def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--s', required=True)
    parser.add_argument('--d', required=True)
    parser.add_argument('--m', required=True)
    parser.add_argument('--t', required=True)
    parser.add_argument('--u1', required=True)
    parser.add_argument('--u2', required=True)
    return parser

def main():
    # Set up parameters
    parser = get_parser()
    args = parser.parse_args()
    arg_s = args.s
    arg_d = args.d
    arg_m = args.m
    arg_t = args.t
    arg_u1 = args.u1
    arg_u2 = args.u2
    if arg_m == 'monomer':
        m = 'model_1,model_2,model_3,model_4,model_5'
        p = 'monomer_ptm'
    if arg_m == 'multimer':
        m = 'model_1_multimer,model_2_multimer,model_3_multimer,model_4_multimer,model_5_multimer'
        p = 'multimer'
    # define logfile
    logname = 'log_parafold'
    logging.basicConfig(level=logging.DEBUG, 
                        filename=logname, 
                        filemode="a",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logger = logging.getLogger(__name__)
    logger.info("ParaFold Start!")
    # Create directory for log
    if not os.path.exists('./log_gpu/'):
        os.mkdir('./log_gpu/')
    # Divide files in chunks
    df = pd.read_csv('jobs.csv')
    df = df.sort_values(by=['length'])
    files_chunk = list(divide_chunks(df['file'].tolist(), 2))
    # Run ParaFold
    for files in files_chunk:
        commands = []
        if len(files) == 2:
            commands.append(script(files[0],arg_s,arg_d,p,arg_t,m,arg_u1))
            commands.append(script(files[1],arg_s,arg_d,p,arg_t,m,arg_u2))
        else:
            commands.append(script(files[0],arg_s,arg_d,p,arg_t,m,arg_u1))
        procs = [subprocess.Popen(i,shell=True) for i in commands]
        for proc in procs:
            proc.communicate()
        for file in files:
            logger.info(file+" is done!")
            
if __name__ == "__main__":
    main()    
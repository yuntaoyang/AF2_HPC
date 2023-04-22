#!/usr/bin/env python
# coding: utf-8

# Generate a job file for TACC computing clusters
# --s: the directory of AF2 script
# --d: the directory of AF2 data
# --m: monomer or multimer
# --t: max template date

import os
import pandas as pd
import argparse

def script(file,arg_s,arg_d,p,arg_t,m):
    script = ['bash',os.path.join(arg_s,'run_alphafold.sh'),
              '-d',arg_d,
              '-o','./out/',
              '-p',p,
              '-i',os.path.join('./fasta/',file),
              '-t',arg_t,
              '-m',m,
              '-f','>',
              os.path.join('./log_cpu/',file.replace('.fasta','.log')),'2>&1']
    return ' '.join(script)

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--s', required=True)
    parser.add_argument('--d', required=True)
    parser.add_argument('--m', required=True)
    parser.add_argument('--t', required=True)
    return parser

def main():
    # Set up parameters
    parser = get_parser()
    args = parser.parse_args()
    arg_s = args.s
    arg_d = args.d
    arg_m = args.m
    arg_t = args.t
    if arg_m == 'monomer':
        m = 'model_1'
        p = 'monomer_ptm'
    if arg_m == 'multimer':
        m = 'model_1_multimer'
        p = 'multimer'
    # Create directory for output and log
    if not os.path.exists('./out/'):
        os.makedirs('./out/')
    if not os.path.exists('./log_cpu/'):
        os.makedirs('./log_cpu/')
    # Load the job list
    df = pd.read_csv('jobs.csv')
    df = df.sort_values(by=['length'])
    # Generate a job file for TACC
    f = open("jobfile", 'a')
    for file in df['file']:
        f.write(script(file,arg_s,arg_d,p,arg_t,m)+'\n')
    f.close()
            
if __name__ == "__main__":
    main()    

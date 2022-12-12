#!/usr/bin/env python
# coding: utf-8

af2_script = '/work/07225/yang1995/ls6/software/ParallelFold_212/run_alphafold.sh'
af2_data = '/scratch/tacc/apps/bio/alphafold/data'
path_out = ''
path_fasta = ''
path_log = ''

max_template_date = '2022-03-10'
file_name = '' # a csv file with a column for file name and a column for length

# 2 parameters for monomer and multimer
# 'monomer_ptm' & 'model_1'
# 'multimer' & 'model_1_multimer'
parameter_1 = ''
parameter_2 = ''

import os
import pandas as pd

if __name__ == "__main__":
    job = pd.read_csv(file_name)
    f = open("jobfile", 'a')
    for file in job['file']:
        line = ['bash',af2_script,
                '-d',af2_data,
                '-o',path_out,
                '-p',parameter_1,
                '-i',path_fasta+file+'.fasta',
                '-t',max_template_date,
                '-m',parameter_2,
                '-f','>',
                path_log+file+'.log','2>&1']
        f.write(' '.join(line)+'\n')
    f.close()
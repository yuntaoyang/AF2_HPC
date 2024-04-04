#!/usr/bin/env python
# coding: utf-8

"""
Run 2 AF2-GPU jobs in parallel in GPUs.
"""

import os
import argparse
import logging
import subprocess
import pandas as pd

def build_script(af2_model, af2_data, fasta_dir, fasta_file, max_template_date, gpu):
    # Paramters related to the AF2 model
    model_settings = {
        'monomer': ('model_1,model_2,model_3,model_4,model_5', 
                    'monomer_ptm', 
                    './workflow/ParaFold_GPU/'),
        'multimer': ('model_1_multimer,model_2_multimer,model_3_multimer,model_4_multimer,model_5_multimer', 
                     'multimer',
                     './workflow/ParaFold_GPU/')
    }  
    model, model_preset, script_dir = model_settings[af2_model]
    ## Path to the script
    script_path = os.path.join(script_dir, 'run_alphafold.sh')
    # Path to the fasta data
    input_fasta_path = os.path.join(fasta_dir, fasta_file)
    # Path to the log data
    log_file_path = os.path.join('./log_gpu', fasta_file.replace('.fasta', '.log'))
    # The script
    script_cmd = f"bash {script_path} -d {af2_data} -o ./out/ -p {model_preset} -i {input_fasta_path} " \
              f"-t {max_template_date} -m {model} -u {gpu} > {log_file_path} 2>&1"
    return script_cmd

def divide_chunks(l, n):
    """Yield successive n-sized chunks from list l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def get_parser():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description='Run AF2-GPU jobs in parallel.')
    parser.add_argument('--af2_model', choices=['monomer', 'multimer'], required=True, help='Type of AF2 model: monomer or multimer')
    parser.add_argument('--af2_data', required=True, help='Directory of the AF2 data in Texas Advanced Computing Center')
    parser.add_argument('--fasta_dir', required=True, help='Directory of the fasta files')
    parser.add_argument('--fasta_list', required=True, help='A list of fasta files and their lengths')
    parser.add_argument('--max_template_date', required=True, help='Maximum template date')
    parser.add_argument('--gpu1', required=True, help='GPU ID for the first job')
    parser.add_argument('--gpu2', required=True, help='GPU ID for the second job')
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    # Ensure log_gpu directories exist
    os.makedirs('./log_gpu/', exist_ok=True)
    # Run the GPU part
    df_jobs = pd.read_csv(args.fasta_list).sort_values(by='length')
    files_chunk = list(divide_chunks(df_jobs['file'].tolist(), 2))
    for files in files_chunk:
        commands = [build_script(args.af2_model, args.af2_data, args.fasta_dir, file, args.max_template_date, args.gpu1 if i == 0 else args.gpu2)
                    for i, file in enumerate(files)]
        print(commands[0])
        print(commands[1])
        # procs = [subprocess.Popen(cmd, shell=True, executable='/bin/bash') for cmd in commands]
        # for proc in procs:
        #     proc.wait()

if __name__ == "__main__":
    main()
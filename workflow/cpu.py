#!/usr/bin/env python
# coding: utf-8

"""
Generate a job file for Texas Advanced Computing Center.
"""

import pandas as pd
import os
import argparse

def build_script(af2_model, af2_data, fasta_dir, fasta_file, max_template_date):
    # Paramters related to the AF2 model
    model_settings = {
        'monomer': ('model_1', 'monomer_ptm', './workflow/ParaFold_CPU/ParaFold_Monomer'),
        'multimer': ('model_1_multimer', 'multimer', './workflow/ParaFold_CPU/ParaFold_Multimer')
    }  
    model, model_preset, script_dir = model_settings[af2_model]
    # Path to the script
    script_path = os.path.join(script_dir, 'run_alphafold.sh')
    # Path to the fasta data
    input_fasta_path = os.path.join(fasta_dir, fasta_file)
    # Path to the log data
    log_file_path = os.path.join('./log_cpu', fasta_file.replace('.fasta', '.log'))
    # The script
    script_cmd = f"bash {script_path} -d {af2_data} -o ./out/ -p {model_preset} " \
                 f"-i {input_fasta_path} -t {max_template_date} -m {model} -f > {log_file_path} 2>&1"
    return script_cmd

def get_parser():
    parser = argparse.ArgumentParser(description='Generate a job file for TACC computing clusters.')
    parser.add_argument('--af2_model', choices=['monomer', 'multimer'], required=True, help='Type of AF2 model: monomer or multimer')
    parser.add_argument('--af2_data', required=True, help='Directory of the AF2 data in Texas Advanced Computing Center')
    parser.add_argument('--fasta_dir', required=True, help='Directory of the fasta files')
    parser.add_argument('--fasta_list', required=True, help='A list of fasta files and their lengths')
    parser.add_argument('--max_template_date', required=True, help='Maximum template date')
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    # Ensure output and log_cpu directories exist
    os.makedirs('./out/', exist_ok=True)
    os.makedirs('./log_cpu/', exist_ok=True)
    # Make the jobfile
    df_jobs = pd.read_csv(args.fasta_list).sort_values(by='length')
    with open("jobfile", 'a') as jobfile:
        for fasta_file in df_jobs['file']:
            jobfile.write(build_script(args.af2_model, args.af2_data, args.fasta_dir, fasta_file, 
                                       args.max_template_date) + '\n')

if __name__ == "__main__":
    main()
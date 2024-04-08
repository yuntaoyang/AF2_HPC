#!/usr/bin/env python
# coding: utf-8

"""
Copy and rename the AF2-predicted structure with the highest pLDDT scores.
"""

import os
import argparse
import shutil

def get_parser():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description='Copy and rename the AF2-predicted structure with the highest pLDDT scores.')
    parser.add_argument('--out_dir', required=True, help='The path of the out directory')
    parser.add_argument('--pdb_dir', required=True, help='The path of the pdb directory')
    return parser

def copy_and_rename_pdb():
    parser = get_parser()
    args = parser.parse_args()
    # Ensure the pdb directory exists
    os.makedirs(args.pdb_dir, exist_ok=True)
    # Log missing pdb files
    with open(os.path.join(args.pdb_dir, "error.log"), 'a') as log_file:
        for folder in os.listdir(args.out_dir):
            source_file = os.path.join(args.out_dir, folder, 'ranked_0.pdb')
            if os.path.isfile(source_file):
                dest_file = os.path.join(args.pdb_dir, f'{folder}.pdb')
                shutil.copy2(source_file, dest_file)
            else:
                log_file.write(f'Error: Missing ranked_0.pdb in {folder}\n')

if __name__ == "__main__":
    copy_and_rename_pdb()
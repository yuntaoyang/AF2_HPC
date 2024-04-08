#!/usr/bin/env python
# coding: utf-8

"""
Extract secondary sturctures and relative ASA from the AF2 predicted structures.
"""

from Bio.PDB import PDBParser
from Bio.PDB.DSSP import DSSP
import pandas as pd
import argparse
import os

def get_parser():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description='Extract secondary sturctures and relative ASA from the AF2 predicted structures.')
    parser.add_argument('--pdb_dir', required=True, help='The path of the pdb directory')
    parser.add_argument('--dssp_dir', required=True, help='The path of the dssp directory')
    return parser

def extract_features(pdb_dir, pdb_file):
    parser = PDBParser()
    output_data = []
    structure = parser.get_structure(pdb_file, os.path.join(pdb_dir, pdb_file))
    model = structure[0]
    # Try the DSSP program
    try:
        dssp_data = DSSP(model, os.path.join(pdb_dir, pdb_file))
    except Exception as e:
        print(f'DSSP error with {pdb_file}: {e}')
        return
    # Save the secondary structures and relative ASA from AF2 prediction
    for i in list(dssp_data.keys()):
        chain, pos, res, ss, rel_asa = i[0], i[1][1], dssp_data[i][1], dssp_data[i][2], dssp_data[i][3]
        output_data.append([chain, pos, res, ss, rel_asa])
    df = pd.DataFrame(output_data, columns=['chain', 'position', 'residue', 'secondary_structure', 'relative_asa'])
    return df
    
def main():
    parser = get_parser()
    args = parser.parse_args()
    # Ensure dssp directory exists
    os.makedirs(args.dssp_dir, exist_ok=True)
    # Process each PDB file
    for pdb_file in os.listdir(args.pdb_dir):
        if pdb_file.split('.')[1] == 'pdb':
            df = extract_features(args.pdb_dir, pdb_file)
            df.to_csv(os.path.join(args.dssp_dir, pdb_file.replace('.pdb', '.csv')), index=False)
        else:
            continue

if __name__ == "__main__":
    main()
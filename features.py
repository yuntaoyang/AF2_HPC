#!/usr/bin/env python
# coding: utf-8

# Get secondary structures and relative_asa from AF2 prediction

import os
import pandas as pd
from Bio.PDB import PDBParser
from Bio.PDB.DSSP import DSSP

def dssp(file):
    p = PDBParser()
    chain = []
    position = []
    residue = []
    secondary_structure = []
    relative_asa = []
    structure = p.get_structure(file,os.path.join('./pdb/',file))
    model = structure[0]
    try:
        dssp = DSSP(model,os.path.join('./pdb/',file))
    except:
        print('DSSP error: '+file)
    for i in list(dssp.keys()):
        chain.append(i[0])
        position.append(i[1][1])
        residue.append(dssp[i][1])
        secondary_structure.append(dssp[i][2])
        relative_asa.append(dssp[i][3])
    df = pd.DataFrame({'chain':chain,
                       'position':position,
                       'residue':residue,
                       'secondary_structure':secondary_structure,
                       'relative_asa':relative_asa})
    df.to_csv(os.path.join('./features/',file.replace('.pdb','.csv')),index=False)
    
def main():
    # Create directory for features
    if not os.path.exists('./features/'):
        os.makedirs('./features/')
    # Run the dssp function
    for file in os.listdir('./pdb/'):
        dssp(file)
        
if __name__ == "__main__":
    main()    
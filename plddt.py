#!/usr/bin/env python
# coding: utf-8

# Get pLDDT from AF2 prediction

import json
import os
import pickle as pkl
import pandas as pd
from Bio import SeqIO

def seq_len(file):
    length = []
    for seq_record in SeqIO.parse(os.path.join('./fasta/',file+".fasta"), "fasta"):
        length.append(len(seq_record))
    return length

def find_model(file):
    with open(os.path.join('./out/',file,'ranking_debug.json'),'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict['order'][0]

def pLDDT(file,model,length):
    with open(os.path.join('./out/',file,'result_'+model+'.pkl'), 'rb') as f:
        obj = pkl.load(f)
    pLDDT_l = list(obj['plddt'])
    chain_l = []
    position_l = []
    for n,l in enumerate(length):
        for i in range(1,l+1):
            chain_l.append(chr(n+1+96).upper())
            position_l.append(str(i))
    df = pd.DataFrame({'chain':chain_l,
                       'position':position_l,
                       'pLDDT':pLDDT_l})
    return df

def main():
    # Create directory for plddt
    if not os.path.exists('./plddt/'):
        os.makedirs('./plddt/')
    # Run the interfaceResidues function
    for file in os.listdir('./out/'):
        plddt = pLDDT(file,find_model(file),seq_len(file))
        plddt.to_csv(os.path.join('./plddt/',file+'.csv'),index=False)

if __name__ == "__main__":
    main()    
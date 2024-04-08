#!/usr/bin/env python
# coding: utf-8

"""
Extract pLDDT scores from AlphaFold2 predictions.
"""

from Bio import SeqIO
import pandas as pd
import json
import os
import pickle
import argparse

def get_parser():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description='Extract pLDDT scores from AlphaFold2 predictions.')
    parser.add_argument('--out_dir', required=True, help='The path of the out directory')
    parser.add_argument('--fasta_dir', required=True, help='The path of the fasta directory')
    parser.add_argument('--plddt_dir', required=True, help='The path of the pLDDT directory')
    return parser

def get_sequence_lengths(fasta_file, fasta_dir):
    return [len(seq_record) for seq_record in SeqIO.parse(os.path.join(fasta_dir, f"{fasta_file}.fasta"), "fasta")]

def get_top_model(prediction_folder, out_dir):
    with open(os.path.join(out_dir, prediction_folder, 'ranking_debug.json'), 'r') as file:
        ranking_info = json.load(file)
    return ranking_info['order'][0]

def extract_pLDDT_scores(prediction_folder, model, seq_lengths, out_dir):
    with open(os.path.join(out_dir, prediction_folder, f'result_{model}.pkl'), 'rb') as file:
        prediction_data = pickle.load(file)
    plddt_scores = prediction_data['plddt']
    chain_labels, positions = [], []
    for chain_index, length in enumerate(seq_lengths, start=1):
        chain_labels.extend([chr(chain_index + 64)] * length)  # 65 is ASCII for 'A'
        positions.extend(range(1, length + 1))
    return pd.DataFrame({'chain': chain_labels, 'position': positions, 'pLDDT': plddt_scores})

def main():
    parser = get_parser()
    args = parser.parse_args()
    os.makedirs(args.plddt_dir, exist_ok=True)
    for prediction_folder in os.listdir(args.out_dir):
        try:
            sequence_lengths = get_sequence_lengths(prediction_folder, args.fasta_dir)
            top_model = get_top_model(prediction_folder, args.out_dir)
            plddt_df = extract_pLDDT_scores(prediction_folder, top_model, sequence_lengths, args.out_dir)
            plddt_df.to_csv(os.path.join(args.plddt_dir, f"{prediction_folder}.csv"), index=False)
        except Exception as e:
            print(f"AF2 processing error for {prediction_folder}: {e}")

if __name__ == "__main__":
    main()
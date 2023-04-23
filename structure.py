#!/usr/bin/env python
# coding: utf-8

import os
import shutil

def main():
    # directory for pdb files
    if not os.path.exists('./pdb/'):
        os.mkdir('./pdb/')   
    # generate pdb files
    f = open("error_parafold", 'a')
    for folder in os.listdir('./out/'):
        files = os.listdir(os.path.join('./out/',folder))
        if 'ranked_0.pdb' in files:
            shutil.copy2(os.path.join('./out/',folder,'ranked_0.pdb'),'./pdb/')
            os.rename(os.path.join('./pdb/','ranked_0.pdb'),os.path.join('./pdb/',folder+'.pdb'))
        else:
            f.write('Error: '+folder+'\n')
    f.close()
    
if __name__ == "__main__":
    main() 
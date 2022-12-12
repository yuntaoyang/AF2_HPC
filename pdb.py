#!/usr/bin/env python
# coding: utf-8

path_out = ''
path_pdb = ''

error = '' # a file to record errors

import os
import shutil
import logging

if __name__ == "__main__":
    # directory for pdb files
    if not os.path.exists(path_pdb):
        os.mkdir(path_pdb)
        
    # record files with error
    logging.basicConfig(level=logging.DEBUG, 
                        filename=error, 
                        filemode="a",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logger = logging.getLogger(__name__)
    
    # generate pdb files
    for folder in os.listdir(path_out):
        files = os.listdir(path_out+folder)
        if 'ranked_0.pdb' in files:
            shutil.copy2(path_out+folder+'/ranked_0.pdb',path_pdb)
            os.rename(path_pdb+'ranked_0.pdb',path_pdb+folder+'.pdb')
        else:
            logger.info('AF2 Error: '+folder)
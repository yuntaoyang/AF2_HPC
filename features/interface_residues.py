#!/usr/bin/env python
# coding: utf-8

"""
Finds 'interface' residues between two chains in a complex.
"""

from pymol import cmd, stored
import pandas as pd
import argparse
import os

def interfaceResidues(cmpx, cA='c. A', cB='c. B', cutoff=1.0, selName="interface"):
	"""
	interfaceResidues -- finds 'interface' residues between two chains in a complex.	
	"""
	# Save user's settings, before setting dot_solvent
	oldDS = cmd.get("dot_solvent")
	cmd.set("dot_solvent", 1)
	
	# set some string names for temporary objects/selections
	tempC, selName1 = "tempComplex", selName+"1"
	chA, chB = "chA", "chB"
	
	# operate on a new object & turn off the original
	cmd.create(tempC, cmpx)
	cmd.disable(cmpx)
	
	# remove cruft and inrrelevant chains
	cmd.remove(tempC + " and not (polymer and (%s or %s))" % (cA, cB))
	
	# get the area of the complete complex
	cmd.get_area(tempC, load_b=1)
	# copy the areas from the loaded b to the q, field.
	cmd.alter(tempC, 'q=b')
	
	# extract the two chains and calc. the new area
	# note: the q fields are copied to the new objects
	# chA and chB
	cmd.extract(chA, tempC + " and (" + cA + ")")
	cmd.extract(chB, tempC + " and (" + cB + ")")
	cmd.get_area(chA, load_b=1)
	cmd.get_area(chB, load_b=1)
	
	# update the chain-only objects w/the difference
	cmd.alter( "%s or %s" % (chA,chB), "b=b-q" )
	
	# The calculations are done.  Now, all we need to
	# do is to determine which residues are over the cutoff
	# and save them.
	stored.r, rVal, seen = [], [], []
	cmd.iterate('%s or %s' % (chA, chB), 'stored.r.append((model,resi,b))')

	cmd.enable(cmpx)
	cmd.select(selName1, 'none')
	for (model,resi,diff) in stored.r:
		key=resi+"-"+model
		if abs(diff)>=float(cutoff):
			if key in seen: continue
			else: seen.append(key)
			rVal.append( (model,resi,diff) )
			# expand the selection here; I chose to iterate over stored.r instead of
			# creating one large selection b/c if there are too many residues PyMOL
			# might crash on a very large selection.  This is pretty much guaranteed
			# not to kill PyMOL; but, it might take a little longer to run.
			cmd.select( selName1, selName1 + " or (%s and i. %s)" % (model,resi))

	# this is how you transfer a selection to another object.
	cmd.select(selName, cmpx + " in " + selName1)
	# clean up after ourselves
	cmd.delete(selName1)
	cmd.delete(chA)
	cmd.delete(chB)
	cmd.delete(tempC)
	# show the selection
	cmd.enable(selName)
	
	# reset users settings
	cmd.set("dot_solvent", oldDS)
	
	return rVal

def load(file, chain_a, chain_b):
    object_name = os.path.basename(file)
    cmd.load(file, object_name)
    foundResidues = interfaceResidues(object_name, cA="c. "+chain_a, cB="c. "+chain_b, cutoff=0.75)
    chain = []
    position = []
    dASA = []
    for i in foundResidues:
        if i[0][2:] == 'A':
            chain.append(chain_a)
        else:
            chain.append(chain_b)
        position.append(i[1])
        dASA.append(i[2])
    df = pd.DataFrame({'chain':chain,
                       'position':position,
                       'dASA':dASA})
    return df

def get_parser():
   """Parses command-line arguments."""
   parser = argparse.ArgumentParser(description='Finds interface residues between two chains in a complex.')
   parser.add_argument('--pdb_dir', required=True, help='The path of the pdb file')
   parser.add_argument('--interface_dir', required=True, help='The path of the output interface residues')
   parser.add_argument('--chain1', required=True, help='The first chain ID')
   parser.add_argument('--chain2', required=True, help='The second chain ID')
   return parser

def main():
    # Set up parameters
    parser = get_parser()
    args = parser.parse_args()
    # Run the interfaceResidues function
    interface_residues = load(args.pdb_dir, args.chain1, args.chain2)
    interface_residues.to_csv(args.interface_dir, index=False)

if __name__ == "__main__":
    main()    
    
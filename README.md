# Run AF2 in parallel in an HPC environment
## cpu.py
Generate an AF2 jobfile for running the CPU part in TACC computing clusters.
* --s: the directory of AF2 script
* --d: the directory of AF2 data ('/scratch/tacc/apps/bio/alphafold/data' in the Lonestar 6)
* --m: monomer or multimer
* --t: max template date
## cpu.sh
Submit the AF2 jobfile in TACC computing clusters.
## gpu.py
Run the GPU part in a GPU server.
* --s: the directory of AF2 script
* --d: the directory of AF2 data
* --m: monomer or multimer
* --t: max template date
* --u1: gpu for the first job 
* --u2: gpu for the second job
## structure.py
Collect structural files and record AF2 errors.
## interface_residues.py
Identify residues in the interface of different chains.
* --file: the name of the pdb file
* --a: the ID of the first chain (A)
* --b: the ID of the second chain (B)
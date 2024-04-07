# AF2_HPC
## Introduction
* A workflow to implement and accelerate the AF2 workflow in a high-performance computing environment.
* A collection of scripts to extract structural fetaures from AF2-predicted structures.
* **Reference**: Yang, Y., Li, Z., Shih, D. J., & Zheng, W. J. (2022). AlphaFold 2 Monomer: Deployment in an HPC Environment.
## Implementation of the AlphaFold 2 Workflow
### Set up the AF2 environment
```
conda env create -f environment.yml
conda activate af2
```
### The CPU part & Texas Advanced Computing Center
1. Place FASTA files in the respective directories. You can find example FASTA files under:
* Monomers: `./test_data/monomer_fasta`
* Multimers: `./test_data/multimer_fasta`
2. Place Lists of FASTA Files in the respective directories. You can find example lists under:
* Monomer: `./test_data/monomer_job.csv`
* Multimer: `./test_data/multimer_job.csv`
3. Monomer: generate a jobfile.
```
python workflow/cpu.py --af2_model monomer --af2_data ./af2_data --fasta_dir test_data/monomer_fasta/ --fasta_list test_data/monomer_jobs.csv --max_template_date 1800-01-01
```
4. Multimer: generate a jobfile.
```
python workflow/cpu.py --af2_model multimer --af2_data ./af2_data --fasta_dir test_data/multimer_fasta/ --fasta_list test_data/multimer_jobs.csv --max_template_date 1800-01-01
```
5. Ensure the **--af2_data** argument points to the correct AF2 data directory located at the Texas Advanced Computing Center.
6. Revise the parameters in `./workflow/cpu.bash`, especially **LAUNCHER_WORKDIR** to the correct work directory.
7. Submit the CPU part to Texas Advanced Computing Center.
```
sbatch workflow/cpu.sh
```
8. The CPU part generates the AF2 features in `./out` directory and  log files in `./log_cpu` directory.
### The GPU part & UTHealth Houston
1. Copy the `./out` directory and the `./log_cpu` directory to the GPU server in UTHealth Houston.
2. The following scripts can run 2 GPU jobs in parallel.
3. Monomer
```
python workflow/gpu.py --af2_model monomer --af2_data ./af2_data --fasta_dir ./test_data/monomer_fasta --fasta_list ./test_data/monomer_jobs.csv --max_template_date 1800-01-01 --gpu1 0 --gpu2 1
```
4. Multimer
```
python workflow/gpu.py --af2_model multimer --af2_data ./af2_data --fasta_dir ./test_data/multimer_fasta --fasta_list ./test_data/multimer_jobs.csv --max_template_date 1800-01-01 --gpu1 0 --gpu2 1
```
5. Ensure the **--af2_data** argument points to the correct AF2 data directory located at the GPU server in UTHealth Houston.
6. The GPU part generates AF2-predicted structures in `./out` directory  and log files `./log_gpu` directory.
## Extraction of structural features from AF2-predicted structures

#!/bin/bash

#SBATCH   -p spr
#SBATCH   -J neo4jtest
#SBATCH   -o neo4jtest.o%j
#SBATCH   -e neo4jtest.e%j
#SBATCH   -N 3
#SBATCH   -t 0:30:00
#SBATCH   -A TACC-SCI

module unload python
module load pylauncher

cd $SCRATCH/neo4j-arxiv

uv run python classic_launcher.py

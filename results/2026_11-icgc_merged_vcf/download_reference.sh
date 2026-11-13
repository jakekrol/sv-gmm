#!/usr/bin/env bash

url='https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz'
wget "$url"
gunzip hs37d5.fa.gz
samtools faidx hs37d5.fa
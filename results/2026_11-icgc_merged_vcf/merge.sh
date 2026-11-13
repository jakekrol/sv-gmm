#!/usr/bin/env bash

# get all SVs into 1 vcf
bcftools merge -Oz -o all_dels.vcf.gz reheadered_vcfs/*.vcf.gz
tabix -p vcf all_dels.vcf.gz

# recommended
truvari collapse \
    -i all_dels.vcf.gz \
    -o merged_dels-recommended.vcf \
    -c collapsed_dels-recommended.vcf.gz \
    --refdist 500 \
    --pctseq 0 \
    --pctsize 0.95 \
    --pctovl 0 \
    --reference hs37d5.fa

# less stringent
truvari collapse \
    -i all_dels.vcf.gz \
    -o merged_dels-loose.vcf \
    -c collapsed_dels-loose.vcf.gz \
    --refdist 1000 \
    --pctseq 0 \
    --pctsize 0.7 \
    --pctovl 0 \
    --reference hs37d5.fa
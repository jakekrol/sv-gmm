#!/usr/bin/env bash

# get all SVs into 1 vcf
bcftools merge -Oz -o all_dels.vcf.gz reheadered_vcfs/*.vcf.gz
tabix -p vcf all_dels.vcf.gz

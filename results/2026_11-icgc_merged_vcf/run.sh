#!/usr/bin/env bash

# map sample-wise vcfs to pcawg donor ids
./vcf2donor.py

# add donor IDs to VCF sample names
# format header an index to prepare for bcftools merge
# also filters for DEL SVs
./reheader_vcfs.py

# download hs37d5 reference
./download_reference.sh

# combine all sample vcfs into one
./combine_vcf.sh

# filter combined vcf for SVs in STIX indexed samples
./subset_combined_vcf.py

# merge svs
./truvari_merge.sh

# get merged svs (>=2 samples)
./get_merged_svs.py

# convert to csv format for svgmm
./vcf2query.py


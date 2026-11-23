#!/usr/bin/env bash
# recommended

SIZEMAX=10000000
SIZEMIN=0
input=filtered_dels.vcf.gz

truvari collapse \
    -i $input \
    -o merged_dels-recommended.vcf \
    -c collapsed_dels-recommended.vcf.gz \
    --refdist 500 \
    --pctseq 0 \
    --pctsize 0.95 \
    --pctovl 0 \
    --sizemin $SIZEMIN \
    --sizemax $SIZEMAX \
    --reference hs37d5.fa

# less stringent
truvari collapse \
    -i $input \
    -o merged_dels-loose.vcf \
    -c collapsed_dels-loose.vcf.gz \
    --refdist 1000 \
    --pctseq 0 \
    --pctsize 0.7 \
    --pctovl 0 \
    --sizemin $SIZEMIN \
    --sizemax $SIZEMAX \
    --reference hs37d5.fa

# even less stringent
truvari collapse \
    -i $input \
    -o merged_dels-loosest.vcf \
    -c collapsed_dels-loosest.vcf.gz \
    --refdist 10000 \
    --pctseq 0 \
    --pctsize 0.5 \
    --pctovl 0 \
    --sizemin $SIZEMIN \
    --sizemax $SIZEMAX \
    --reference hs37d5.fa
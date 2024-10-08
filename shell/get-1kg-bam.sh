#!/usr/bin/env bash
# get bam regions from 1kg
date

idx=${1:-20130502.phase3.low_coverage.alignment.index}
sample=${2:-HG01125}
chr=${3:-19}
padding=${4:-1000}
l=${5:-$((54887338 - $padding))}
r=${6:-$((54888354 + $padding))}
out=${7:-"${sample}.${chr}.${l}.${r}.bam"}

region="${chr}:${l}-${r}"
prefix="s3://1000genomes/phase3/"

fname=$(cut -f1 $idx | grep "${sample}.mapped.*bam$")
fname="${prefix}${fname}"
echo "getting BAM: $fname $region"
samtools view -b \
    $fname $region > $out
samtools sort $out -o $out
samtools index $out
date

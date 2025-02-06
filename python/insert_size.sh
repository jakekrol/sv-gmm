#!/usr/bin/env bash
date
bamfile=$1
dout='/data/jake/sv-gmm/data/insert_sizes2'
bamfile="s3://1000genomes/phase3/$bamfile"
sample=$(basename $bamfile | cut -d'.' -f1)
out="$dout/$sample.isize"
echo $bamfile
echo $sample
echo $out
samtools stats $bamfile | grep "^IS" > $out
date

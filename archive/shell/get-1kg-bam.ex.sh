#!/usr/bin/env bash

l=54887338
r=54888354
padding=400
l=$((l + padding))
r=$((r + padding))

samtools view -b s3://1000genomes/phase3/data/HG01125/alignment/HG01125.mapped.ILLUMINA.bwa.CLM.low_coverage.20120522.bam 19:$l-$r > test2.bam
samtools index test2.bam

#sample=${1:-HG01125}
#chr=${2:-19}
#start=${3:-54887338}
#stop=${4:-54888354}
#date=20120522
#samtools view -b \
#  s3://1000genomes/phase3/data/$sample/alignment/$sample.mapped.ILLUMINA.bwa.CLM.low_coverage.$date.bam $chr:$start-$stop \
#  "$chr:$start-$stop" \
#  > $sample.$chr.$start.$stop.bam
#samtools index $sample.$chr.$start.$stop.bam
#
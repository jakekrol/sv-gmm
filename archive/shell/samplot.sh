#!/usr/bin/env bash
# the s3 index seems correct
#samplot plot -n HG01125 -b 's3://1000genomes/phase3/data/HG01125/alignment/HG01125.mapped.ILLUMINA.bwa.CLM.low_coverage.20120522.bam 19:54886338-54889354' -t DEL -s 54887338 -e 54888354 -c chr19 -o test2.png -r grch37.fa
#full bam
#samplot plot -n HG01125 -b HG01125.mapped.ILLUMINA.bwa.CLM.low_coverage.20120522.bam -t DEL -s 54887338 -e 54888354 -c chr19 -o full-bam.png -r grch37.fa
# get region of full bam
#samtools view -b HG01125.mapped.ILLUMINA.bwa.CLM.low_coverage.20120522.bam 19:54887338-54888354 > region.bam
samtools index region.bam
samplot -n HG01125 -b region.bam -t DEL -s 54887338 -e 54888354 -c chr19 -o full-bam.png

#pad 1000
samtools view -b HG01125.mapped.ILLUMINA.bwa.CLM.low_coverage.20120522.bam 19:54886338-54889354 > region-pad.bam
samtools index region-pad.bam
samplot plot -n HG01125 -b region-pad.bam -t DEL -s 54887338 -e 54888354 -c chr19 -o region-pad.png -r grch37.fa


#!/usr/bin/env bash

dout=$(pwd)
bams=../../data/2025_10-long_read_plot/HGSV_54541
# sv region
left="173522965"
right="173524108"
chr="3"
zoom_mult=1
cd $bams
len=$(python -c "print(${right}-${left})")
zoom=$(python -c "print(int(${len}*${zoom_mult}))")

samplot plot \
    -b $(ls *.bam) \
    -c ${chr} -s ${left} -e ${right} \
    -t DEL --zoom ${zoom} \
    -o $dout/lr_sv.png

samplot plot \
    -b HG00103.bam HG00149.bam HG03548.bam HG03085.bam \
    -c ${chr} -s ${left} -e ${right} \
    -t DEL --zoom ${zoom} \
    -o $dout/lr_sv_4_samples.png
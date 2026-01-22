#!/usr/bin/env bash

dout=$(pwd)
crams=(HG00149.hg38.cram HG03548.hg38.cram)
# crams=(HG00149.hg38.cram)
# sv region
left="173522965"
right="173524108"
chr="3"
zoom_mult=1
len=$(python -c "print(${right}-${left})")
zoom=$(python -c "print(int(${len}*${zoom_mult}))")

samplot plot \
    -b "${crams[@]}" \
    -r GCA_000001405.15_GRCh38_no_alt_analysis_set.fna \
    -c ${chr} -s ${left} -e ${right} \
    -t DEL --zoom ${zoom} \
    -o $dout/lr.png
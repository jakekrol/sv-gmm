#!/usr/bin/env bash
idx='../data/20130502.phase3.low_coverage.alignment.index'
padding=1000
indir="../data/variant-sample-modes"
outdir="../data/bams1000"
mapfile -t variant_modes < <(ls $indir)
for file in "${variant_modes[@]}"; do
    echo "file: $file"
    IFS='.' read -r variant chr start end ext <<< "${file}"
    echo "variant: $variant chr: $chr start: $start end: $end ext: $ext"
    while read -r line; do
        read -r sample mode <<< "$line"
        echo "sample: $sample mode: $mode"
        outfile="${outdir}/${variant}.${mode}.${sample}.${chr}.$(($start - $padding)).$(($end + $padding)).bam"
        echo "outfile: $outfile"
        ./get-1kg-bam.sh $idx $sample $chr $padding $start $end $outfile
    done < ${indir}/${file}
done

#!/usr/bin/env bash
# conda activate /data/jake/conda-py3.7
# bam file pattern: SV_NAME.MODE_#.SAMPLE_NAME.CHR.START.END.bam
date
set -u
sv=${1:-DEL_pindel_24042}
mode=${2:-all}
dir_bam=${3:-/data/jake/sv-gmm/data/bams1000}
out=${4:-/data/jake/sv-gmm/fig2/${sv}-mode_${mode}.png}

# optionally subset by mode
if [ "$mode" != "all" ]; then
    echo "Subsetting by mode: $mode"
    pattern="${sv}\.mode_${mode}.*\.bam$"
else
    pattern="${sv}.*\.bam$"
fi

# gather bams
mapfile -t bams < <(echo "$(ls $dir_bam)" | grep "$pattern")

# add dir prefix
for i in ${!bams[@]}; do
    bams[$i]="${dir_bam}/${bams[$i]}"
done
echo "length: ${#bams[@]}"

# gather samples
samples=()
for bam in ${bams[@]}; do
    sample=$(echo "$bam" | cut -d '.' -f 3)
    samples+=("$sample")
done

# preview
echo "${samples[@]:0:5}"
echo "${bams[@]:0:5}"

# extract params from filename
chr=$(echo "${bams[@]:0:1}" | cut -d '.' -f 4)
start=$(echo "${bams[@]:0:1}" | cut -d '.' -f 5)
end=$(echo "${bams[@]:0:1}" | cut -d '.' -f 6)

# plot
samplot plot -n "${samples[*]}" \
    -b $(echo "${bams[*]}") \
    -t DEL \
    -s $(($start - 1000)) \
    -e $((end + 1000)) \
    -c "chr$chr" \
    -o $out 

date


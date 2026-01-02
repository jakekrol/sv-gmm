#!/usr/bin/env bash
set -euo pipefail
t_0=$(date +%s)

echo "# finding unique icgc sv types"
indir=../../data/2025_12_3-pcawg_sv_callset/icgc_sv_public_passonly/icgc/open
[ -d "${indir}" ] || { echo "Input directory ${indir} does not exist. Exiting."; exit 1; }
mapfile -t files < <(ls "${indir}"/*.bedpe.gz)
zcat "${files[@]}" | cut -f 11 | sort | uniq > icgc_sv_types.txt
echo "# unique icgc sv types"
cat icgc_sv_types.txt | grep -v "svclass"
echo "# parsing svs"

# convert icgc sv to stix sv format
icgc_sv2stix_sv () {
    local file_icgc="$1"
    local outfile="$2"
    zcat "${file_icgc}" | \
        tail -n +2 | \
        cut -f 1-6,11 | \
        sed 's|h2hINV|INV|g' | \
        sed 's|t2tINV|INV|g' | \
        sed 's|TRA|BND|g' > \
        "${outfile}"
}

outdir='all'
mkdir -p "${outdir}"
n=${#files[@]}
i=1
echo "# parsing icgc svs into stix query format"
for f in "${files[@]}"; do
    fbase=$(basename "${f}")
    fout="${outdir}/${fbase%.bedpe.gz}.bedpe"
    echo "# processing sample ${fbase} -> ${fout}"
    icgc_sv2stix_sv "${f}" "${fout}"
    echo "# completed ${i} of ${n} samples"
    i=$((i+1))
done

echo "# subsetting for DELs only"
mapfile -t files < <(ls "${outdir}"/*.bedpe)
outdir_del='del'
mkdir -p "${outdir_del}"
i=1
echo "# subsetting icgc svs for deletions only"
for f in "${files[@]}"; do
    fbase=$(basename "${f}")
    fout="${outdir_del}/${fbase}"
    echo "# processing sample ${fbase} -> ${fout}"
    grep -P "\tDEL" "${f}" > "${fout}" || rm "${fout}" # remove files with no DELs
    echo "# completed ${i} of ${n} samples"
    i=$((i+1))
done

echo "# completed in $(($(date +%s) - t_0)) seconds"



#!/usr/bin/env bash
set -euo pipefail
t_0=$(date +%s)

# indir=../2026_01-icgc_svs/del
infile=$(realpath "../2026_01-icgc_svs/icgc_stix_del.bedpe")
outdir=$(realpath './out-min_read_5')
min_read=5
mkdir -p "${outdir}"
outdir=$(realpath "${outdir}")
index=/data/jake/stix-pcawg-dna
shardfile="${index}/shardfiles/shardfile.tumor.tsv"
procs=15
logfile=$(realpath "./stix-min_read_${min_read}.log")
echo "# input bedpe file: ${infile}"
echo "# output directory: ${outdir}"
echo "# stix index: ${index}"
echo "# stix shardfile: ${shardfile}"
echo "# min read: ${min_read}"
echo "# processes: ${procs}"
echo "# logfile: ${logfile}"

# echo "# setting up input icgc svs and output files for stix queries"
# if [ -f bedpe_files.input ]; then
#     rm bedpe_files.input
# fi
# if [ -f x ]; then
#     rm x
# fi
# if [ -f y ]; then
#     rm y
# fi
# mapfile -t files < <(ls "${indir}"/*.bedpe)
# # ls "${indir}"/*.bedpe > "x"
# for f in "${files[@]}"; do
#     realpath ${f} >> x
#     base=$(basename "${f}")
#     outfile="${outdir}/${base%.*}.stix.min_read_${min_read}.tsv"
#     echo "${outfile}" >> y
# done
# paste x y > bedpe_files.input
# exit 0

# file2stix () {
#     local bedpe_file=$1
#     local index=$2
#     local shardfile=$3
#     local min_read=$4
#     local outfile=$5
#     cd ${index} || { echo "# could not change to index directory ${index}"; exit 1; }
#     while IFS=$'\t' read -r l_chrom l_start l_end r_chrom r_start r_end svtype id; do
#         echo "# querying stix for sv: ${l_chrom}:${l_start}-${l_end} ${r_chrom}:${r_start}-${r_end} ${svtype} with min_read ${min_read} and writing to ${outfile} and shardfile ${shardfile}"
#         stix \
#             -B "$shardfile" \
#             -l "${l_chrom}:${l_start}-${l_end}" \
#             -r "${r_chrom}:${r_start}-${r_end}" \
#             -t "${svtype}" \
#             -T "${min_read}" \
#             >> "${outfile}"
#     done < "${bedpe_file}"
# }

# export -f file2stix

echo "# running stix queries for icgc svs with min_read ${min_read} and ${procs} processes"
echo "# gargs log file: ${logfile}"
# cat "bedpe_files.input" | 
#     gargs -p "${procs}" \
#         --log="${logfile}" \
#         "file2stix {0} $index $shardfile $min_read {1}"

cd $index || { echo "# could not change to index directory ${index}"; exit 1; }
cat "${infile}" | \
    gargs -p "${procs}" \
        --log="${logfile}" \
        "stix -B $shardfile -l {0}:{1}-{2} -r {3}:{4}-{5} -t {6} -T ${min_read} > ${outdir}/{7}.{6}.{0}.{1}.{2}.{3}.{4}.{5}.stix.out"
t_1=$(date +%s)
echo "# completed in $((t_1-t_0)) seconds"




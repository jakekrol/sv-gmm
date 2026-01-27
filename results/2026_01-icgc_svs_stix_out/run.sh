#!/usr/bin/env bash
# set -euo pipefail
t_0=$(date +%s)

indir=../2026_01-icgc_svs/del
outdir='./out'
mkdir -p "${outdir}"
outdir=$(realpath "${outdir}")
index=/data/jake/stix-pcawg-dna
procs=30
echo "# input directory: ${indir}"
echo "# output directory: ${outdir}"
echo "# root dir of stix indices: ${index}"
echo "# processes: ${procs}"

# get shards
shardfile=/data/jake/stix-pcawg-dna/shardfiles/shardfile.tumor.tsv
mapfile -t shards < <(sed 's|\t|:|' $shardfile)

# get input files
mapfile -t input_files < <(ls ${indir}/*.bedpe)
for i in "${!input_files[@]}"; do
    input_files[$i]=$(realpath "${input_files[$i]}")
done

# run stix queries
cd $index || { echo "# could not change to index directory ${index}"; exit 1; }
for shard in ${shards[@]}; do
    echo "# shard: ${shard}"
    idx=$(echo ${shard} | cut -d':' -f1)
    idx_base=$(basename ${idx})
    ped_db=$(echo ${shard} | cut -d':' -f2)
    ped_db_base=$(basename ${ped_db})
    echo "# index: ${idx_base}"
    echo "# ped db: ${ped_db_base}"
    shard_outdir="${outdir}/${idx_base}"
    mkdir -p "${shard_outdir}"
    for input in ${input_files[@]}; do
        cat $input | gargs -p "${procs}" \
            "stix -s 500 -i ${idx_base} -d ${ped_db_base} -g -l {0}:{1}-{2} -r {3}:{4}-{5} -t {6} > ${shard_outdir}/{7}.{0}.{1}.{2}.{3}.{4}.{5}.stix.out"
    done
done

t_1=$(date +%s)
echo "# completed in $((t_1-t_0)) seconds"





# echo "# running stix queries for icgc svs with and ${procs} processes"
# echo "# gargs log file: ${logfile}"
# # cat "bedpe_files.input" | 
# #     gargs -p "${procs}" \
# #         --log="${logfile}" \
# #         "file2stix {0} $index $shardfile $min_read {1}"

# cat "${infile}" | \
#     gargs -p "${procs}" \
#         --log="${logfile}" \
#         "stix -g -l {0}:{1}-{2} -r {3}:{4}-{5} -t {6} > ${outdir}/{7}.{6}.{0}.{1}.{2}.{3}.{4}.{5}.stix.out"
# t_1=$(date +%s)
# echo "# completed in $((t_1-t_0)) seconds"


# # echo "# setting up input icgc svs and output files for stix queries"
# # if [ -f bedpe_files.input ]; then
# #     rm bedpe_files.input
# # fi
# # if [ -f x ]; then
# #     rm x
# # fi
# # if [ -f y ]; then
# #     rm y
# # fi
# # mapfile -t files < <(ls "${indir}"/*.bedpe)
# # # ls "${indir}"/*.bedpe > "x"
# # for f in "${files[@]}"; do
# #     realpath ${f} >> x
# #     base=$(basename "${f}")
# #     outfile="${outdir}/${base%.*}.stix.tsv"
# #     echo "${outfile}" >> y
# # done
# # paste x y > bedpe_files.input
# # exit 0



# # file2stix () {
# #     local bedpe_file=$1
# #     local index=$2
# #     local shardfile=$3
# #     local min_read=$4
# #     local outfile=$5
# #     cd ${index} || { echo "# could not change to index directory ${index}"; exit 1; }
# #     while IFS=$'\t' read -r l_chrom l_start l_end r_chrom r_start r_end svtype id; do
# #         echo "# querying stix for sv: ${l_chrom}:${l_start}-${l_end} ${r_chrom}:${r_start}-${r_end} ${svtype} with min_read ${min_read} and writing to ${outfile} and shardfile ${shardfile}"
# #         stix \
# #             -B "$shardfile" \
# #             -l "${l_chrom}:${l_start}-${l_end}" \
# #             -r "${r_chrom}:${r_start}-${r_end}" \
# #             -t "${svtype}" \
# #             -T "${min_read}" \
# #             >> "${outfile}"
# #     done < "${bedpe_file}"
# # }

# # export -f file2stix
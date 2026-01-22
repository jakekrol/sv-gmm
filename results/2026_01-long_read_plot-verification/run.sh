#!/usr/bin/env bash

set -euo pipefail
# download grch38 ref
if [ ! -f GCA_000001405.15_GRCh38_no_alt_analysis_set.fna ]; then
    echo "# downloading grch38 reference"
    wget 'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz'
    gunzip -k GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz
fi
ref=GCA_000001405.15_GRCh38_no_alt_analysis_set.fna
samples=("HG00149" "HG03548")
# cram_hg03085=https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1KG_ONT_VIENNA/hg38/HG03085.hg38.cram
# cram_hg03548=https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1KG_ONT_VIENNA/hg38/HG03548.hg38.cram
echo "# downloading 1kg ont vienna indices for ${samples[*]}"
for s in "${samples[@]}"; do
    # avoid creating .1, .2, ... on repeated runs
    wget -nc "ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1KG_ONT_VIENNA/hg38/${s}.hg38.cram.crai"
done

base_url="https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1KG_ONT_VIENNA/hg38"

echo "# downloading 1kg ont vienna crams for ${samples[*]}"
for s in "${samples[@]}"; do
    if [ ! -f "${s}.hg38.cram" ]; then
        wget -c "${base_url}/${s}.hg38.cram"
    fi
done

region=chr3:173472965-173574108
echo "# extracting region ${region} 1kg ont vienna bams for ${samples[*]} from local crams"
for s in "${samples[@]}"; do
    samtools view -C -T "${ref}" "${s}.hg38.cram" "${region}" -o "${s}.cram"
    samtools index "${s}.cram"
done

./plot.sh
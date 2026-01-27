#!/usr/bin/env bash
t_0=$(date +%s)
dirinput="../2026_01-icgc_svs_stix_out/out_agg"
outcounts='sample_counts.tsv'
# remove output file if it exists
if [ -f "$outcounts" ]; then
    rm "$outcounts"
fi

echo "# counting number of samples per sv"
for file in $(ls $dirinput); do
    if [ ! -s "$dirinput/$file" ]; then
            count=0
            printf "${file}\t${count}\n" >> "$outcounts"
    else
        count=$(cut -f 2 "$dirinput/$file" | sort | uniq | wc -l)
        printf "${file}\t${count}\n" >> "$outcounts"
    fi
done

echo "# plotting histogram of sample counts"
cut -f 2 $outcounts | hist.py --xlabel "Num. samples with SV read support" \
    --ylabel "Frequency (Num. SVs)" \
    --title "Sample counts per ICGC SV" \
    --output "hist_sample_counts_per_sv.png" \
    --bins 30 \
    --ylog


t_1=$(date +%s)
echo "# done in $(($t_1 - $t_0)) seconds"


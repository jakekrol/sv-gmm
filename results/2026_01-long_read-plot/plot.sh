#!/usr/bin/env bash

input=combined_variants.tsv
dirbams=./long_read_bams
zoom_mult=1

row=1
while read -r line; do
    # Parse the line
    chr=$(echo "$line" | cut -f1)
    left=$(echo "$line" | cut -f2)
    right=$(echo "$line" | cut -f3)
    
    # Get all samples (fields 4 onwards)
    samples=$(echo "$line" | cut -f4- | tr '\t' ' ')
    
    # Build list of existing BAM files
    bam_files=""
    for sample in $samples; do
        bam_file="${dirbams}/${sample}_${chr}_${left}_${right}.bam"
        if [ -f "$bam_file" ]; then
            bam_files="$bam_files $bam_file"
        else
            echo "Missing: $bam_file"
        fi
    done
    
    # Skip if no BAM files found
    if [ -z "$bam_files" ]; then
        echo "No BAM files found for row $row, skipping"
        ((row++))
        continue
    fi
    
    # Calculate zoom
    len=$((right - left))
    zoom=$((len * zoom_mult))
    
    # Plot
    echo "Plotting row $row: $chr:$left-$right with $(echo $bam_files | wc -w) samples"
    samplot plot \
        -b $bam_files \
        -c $chr -s $left -e $right \
        -t DEL \
        -o "lr_sv_row${row}.png"
        # -t DEL --zoom $zoom \
    
    ((row++))
done < "$input"
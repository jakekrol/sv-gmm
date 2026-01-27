#!/usr/bin/env bash

# combine files
mapfile -t files < <(ls ../../data/2026_01-variants-plotting-data/ | grep -v "README")
for f in "${files[@]}"; do
    cat "../../data/2026_01-variants-plotting-data/${f}" >> combined_variants.tsv
done


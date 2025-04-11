#!/usr/bin/env python3
import json
import os,sys
import pandas as pd

# PADDING=20000

# data = 'high_cov.tsv'
data='2025_04_08-high_cov.tsv'
df = pd.read_csv(data, sep='\t')
df.columns = ["sv_id", "num_modes_predicted", "chr", "start", "stop", "allele_frequency", "length", "mode_1", "mode_2", "mode_3"]
print(df)
d = {}

for i,row in df.iterrows():
    # sv data
    svid = row['sv_id'].strip()
    d[svid] = {}
    chrm = row['chr']
    start = row['start']
    stop = row['stop']
    PADDING = max(stop-start,20000) # 20kbp or more if sv is large
    pstart = start - PADDING
    pend = stop + PADDING
    d[svid]['chr'] = chrm
    d[svid]['start'] = start
    d[svid]['stop'] = stop
    d[svid]['pstart'] = pstart
    d[svid]['pstop'] = pend
    d[svid]['length'] = row['length']
    # d[svid]['allele_frequency'] = row['allele_frequency']
    d[svid]['num_modes_predicted'] = row['num_modes_predicted']
    # mode data
    mode1 = row['mode_1']
    mode2 = row['mode_2']
    mode3 = row['mode_3']
    modes = []
    # test for nan
    for i,m in enumerate([mode1, mode2, mode3]):
        if pd.isna(m):
            continue
        modes.append(f'mode_{i+1}')
    for m in modes:
        d[svid][m] = []
    for m in modes:
        samples = row[m]
        samples = samples.split(',')
        d[svid][m] = samples
        

# write to json
with open('2025_04_08-highcov_svdata.json', 'w') as f:
    json.dump(d, f, indent=4)
    

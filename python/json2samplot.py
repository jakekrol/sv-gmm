#!/usr/bin/env python3
import pandas as pd
import json
import os,sys
import subprocess

PADDING=20000
REFPATH='/data/jake/examples/data/grch38/GRCh38_full_analysis_set_plus_decoy_hla.fa'
logfile='json2samplot.log'

index='/data/jake/sv-gmm/data/1000G_2504_high_coverage.sequence.index'
dbam='/data/jake/sv-gmm/data/2025_03_21-highcov_bams'
svdata='/data/jake/sv-gmm/data/svdata.json'
dfindex=pd.read_csv(index, sep='\t', comment='#', header=None,usecols=[0])
dfindex.columns=['url']
dfindex['sample'] = dfindex['url'].apply(lambda x: os.path.basename(x).split('.')[0])
print(dfindex.head())

def dlcram(url, refpath, chrm , start, end, out):
    cmd = f'samtools view -b -T {refpath} -h {url} chr{chrm}:{start}-{end} -o {out}'
    result = subprocess.run(cmd, shell=True, check=True)
    print(result)
    # cmd = f'samtools index {out}'
    # result = subprocess.run(cmd, shell=True, check=True)
    return out
# # example
# url='ftp://ftp.sra.ebi.ac.uk/vol1/run/ERR323/ERR3239931/NA19731.final.cram'
# refpath='/data/jake/examples/data/grch38/GRCh38_full_analysis_set_plus_decoy_hla.fa'
# chrm=16
# start=33943172
# end=35303240
# out='test.bam'
# dlcram(url, refpath, chrm, start, end, out)
# sys.exit()


with open(svdata) as f:
    svd = json.load(f)

for k,v in svd.items():
    svid = k
    chrm=v['chr']
    start=v['start']
    pstart = start - PADDING
    end=v['stop']
    pend=end+PADDING
    V = set(v.keys())
    if "mode_1" in v.keys():
        for sample in v['mode_1']:
            if sample not in dfindex['sample'].values:
                # write to logfile
                with open(logfile, 'a') as f:
                    f.write(f'{sample} not found in index\n')
                continue
            url = dfindex[dfindex['sample']==sample]['url'].values[0]
            out = os.path.join(dbam,f'{sample}_{svid}.bam')
            dlcram(url, REFPATH, chrm, pstart, pend, out)
            print(f'wrote {out}')
    if "mode_2" in v.keys():
        for sample in v['mode_2']:
            if sample not in dfindex['sample'].values:
                # write to logfile
                with open(logfile, 'a') as f:
                    f.write(f'{sample} not found in index\n')
                continue
            url = dfindex[dfindex['sample']==sample]['url'].values[0]
            out = os.path.join(dbam,f'{sample}_{svid}.bam')
            dlcram(url, REFPATH, chrm, pstart, pend, out)
            print(f'wrote {out}')
    if "mode_3" in v.keys():
        for sample in v['mode_3']:
            if sample not in dfindex['sample'].values:
                # write to logfile
                with open(logfile, 'a') as f:
                    f.write(f'{sample} not found in index\n')
                continue



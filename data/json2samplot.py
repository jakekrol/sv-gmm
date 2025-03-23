#!/usr/bin/env python3
import pandas as pd
import json
import os,sys
import subprocess
import time

PADDING=20000
REFPATH='/data/jake/examples/data/grch38/GRCh38_full_analysis_set_plus_decoy_hla.fa'
logfile='json2samplot.log'
with open(logfile, 'w') as f:
    # write the time
    f.write(f'{time.ctime()}\n')

index='/data/jake/sv-gmm/data/1000G_2504_high_coverage.sequence.index'
dbam='/data/jake/sv-gmm/data/2025_03_22-highcov_bams_retry'
svdata='/data/jake/sv-gmm/data/svdata2.json'
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

# # 03/21/2025
# for k,v in svd.items():
#     svid = k
#     chrm=v['chr']
#     start=v['start']
#     pstart = start - PADDING
#     end=v['stop']
#     pend=end+PADDING
#     V = set(v.keys())
#     if "mode_1" in v.keys():
#         for sample in v['mode_1']:
#             if sample not in dfindex['sample'].values:
#                 # write to logfile
#                 with open(logfile, 'a') as f:
#                     f.write(f'{sample} not found in index\n')
#                 continue
#             url = dfindex[dfindex['sample']==sample]['url'].values[0]
#             out = os.path.join(dbam,f'{svid}.mode_1.{sample}.{chrm}.{start}.{end}.bam')
#             try:
#                 dlcram(url, REFPATH, chrm, pstart, pend, out)
#                 print(f'wrote {out}')
#             except:
#                 # write to logfile
#                 with open(logfile, 'a') as f:
#                     f.write(f'failed to download {out}\n')
#     if "mode_2" in v.keys():
#         for sample in v['mode_2']:
#             if sample not in dfindex['sample'].values:
#                 # write to logfile
#                 with open(logfile, 'a') as f:
#                     f.write(f'{sample} not found in index\n')
#                 continue
#             url = dfindex[dfindex['sample']==sample]['url'].values[0]
#             out = os.path.join(dbam,f'{svid}.mode_2.{sample}.{chrm}.{start}.{end}.bam')
#             try:
#                 dlcram(url, REFPATH, chrm, pstart, pend, out)
#                 print(f'wrote {out}')
#             except:
#                 # write to logfile
#                 with open(logfile, 'a') as f:
#                     f.write(f'failed to download {out}\n')
#     if "mode_3" in v.keys():
#         for sample in v['mode_3']:
#             if sample not in dfindex['sample'].values:
#                 # write to logfile
#                 with open(logfile, 'a') as f:
#                     f.write(f'{sample} not found in index\n')
#                 continue
#             url = dfindex[dfindex['sample']==sample]['url'].values[0]
#             out = os.path.join(dbam,f'{svid}.mode_3.{sample}.{chrm}.{start}.{end}.bam')
#             try:
#                 dlcram(url, REFPATH, chrm, pstart, pend, out)
#                 print(f'wrote {out}')
#             except:
#                 # write to logfile
#                 with open(logfile, 'a') as f:
#                     f.write(f'failed to download {out}\n')

#03/22/2025
# retry 

# retry samples
# samples = {
# "NA19102",
# "HG02666",
# "NA12383",
# "HG00245",
# "NA11893",
# "NA12842",
# "NA18536",
# "NA18610",
# "NA18614",
# "NA18978",
# "NA18548",
# "NA18647",
# "NA18934",
# "NA19023",
# "NA20351",
# "NA20889",
# "NA21135",
# "NA18611",
# "HG01988"
# }

# redo for this id only
id = "HGSV_183778"

for k,v in svd.items():
    svid = k
    if svid != id:
        continue
    print(svid)
    chrm=v['chr']
    start=v['start']
    pstart = start - PADDING
    end=v['stop']
    pend=end+PADDING
    V = set(v.keys())
    if "mode_1" in v.keys():
        for sample in v['mode_1']:
            # if sample not in samples:
            #     continue
            # print(sample)
            if sample not in dfindex['sample'].values:
                # write to logfile
                with open(logfile, 'a') as f:
                    f.write(f'{sample} not found in index\n')
                continue
            url = dfindex[dfindex['sample']==sample]['url'].values[0]
            out = os.path.join(dbam,f'{svid}.mode_1.{sample}.{chrm}.{start}.{end}.bam')
            try:
                dlcram(url, REFPATH, chrm, pstart, pend, out)
                print(f'wrote {out}')
            except:
                # write to logfile
                with open(logfile, 'a') as f:
                    f.write(f'failed to download {out}\n')
    if "mode_2" in v.keys():
        for sample in v['mode_2']:
            # if sample not in samples:
            #     continue
            # print(sample)
            if sample not in dfindex['sample'].values:
                # write to logfile
                with open(logfile, 'a') as f:
                    f.write(f'{sample} not found in index\n')
                continue
            url = dfindex[dfindex['sample']==sample]['url'].values[0]
            out = os.path.join(dbam,f'{svid}.mode_2.{sample}.{chrm}.{start}.{end}.bam')
            try:
                dlcram(url, REFPATH, chrm, pstart, pend, out)
                print(f'wrote {out}')
            except:
                # write to logfile
                with open(logfile, 'a') as f:
                    f.write(f'failed to download {out}\n')
    if "mode_3" in v.keys():
        for sample in v['mode_3']:
            # if sample not in samples:
            #     continue
            # print(sample)
            if sample not in dfindex['sample'].values:
                # write to logfile
                with open(logfile, 'a') as f:
                    f.write(f'{sample} not found in index\n')
                continue
            url = dfindex[dfindex['sample']==sample]['url'].values[0]
            out = os.path.join(dbam,f'{svid}.mode_3.{sample}.{chrm}.{start}.{end}.bam')
            try:
                dlcram(url, REFPATH, chrm, pstart, pend, out)
                print(f'wrote {out}')
            except:
                # write to logfile
                with open(logfile, 'a') as f:
                    f.write(f'failed to download {out}\n')

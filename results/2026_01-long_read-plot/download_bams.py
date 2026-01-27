#!/usr/bin/env python3
import os,sys
import subprocess
import time
import glob

t_0=time.time()

variants='combined_variants.tsv'
samtools='/data/jake/miniconda3/bin/samtools'
outdir='long_read_bams'
REFERENCE='GCA_000001405.15_GRCh38_no_alt_analysis_set.fna'
LOGFILE='download_bams.log'
if not os.path.exists(outdir):
    os.makedirs(outdir)

chrms=[]
lefts=[]
rights=[]
samples=[]
url_base='https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1KG_ONT_VIENNA/hg38'

def sample2url(sample):
    return os.path.join(url_base, f'{sample}.hg38.cram')
def make_outfile_name(sample,chrom,left,right):
    return f'{sample}_{chrom}_{left}_{right}.bam'

i=1
FAILED_DOWNLOADS=[]
with open(variants, 'r') as f:
    # count num lines in file
    nlines = sum(1 for line in f)
    f.seek(0)
    for line in f:
        fields=line.strip().split('\t')
        chrom=fields[0]
        left=int(fields[1])
        right=int(fields[2])
        samples=fields[3:]
        nsamples=len(samples)
        for j,s in enumerate(samples):
            url=sample2url(s)
            out_bam=os.path.join(outdir, make_outfile_name(s,chrom,left,right))
            cmd = f'{samtools} view -h -b -T {REFERENCE} ' + \
                f'"{url}" "{chrom}:{left}-{right}" ' + \
                f'-o "{out_bam}"'
            print(f" running {cmd}")
            subprocess.run(cmd, shell=True, check=False) # false bc libcurl error always occurs even though file downloads
            time.sleep(1)
            # check if file was downloaded
            if not os.path.exists(out_bam):
                print(f" error: file {out_bam} was not created. skipping indexing ")
                FAILED_DOWNLOADS.append((out_bam, cmd))
            # index
            cmd = f'cd {outdir} && {samtools} index "{os.path.basename(out_bam)}"'
            print(f" running {cmd}")
            subprocess.run(cmd, shell=True, check=False)
            print(f" line progress ({i}/{nlines}). sample {j+1} of {nsamples}")
        i+=1
        print(f" completed {line.strip()} ")
        
with open(LOGFILE, 'w') as logf:
    if len(FAILED_DOWNLOADS)==0:
        logf.write(" all downloads succeeded \n")
    else:
        # write tsv of failed downloads
        logf.write("failed_downloads\tcommand\n")
        for out_bam, cmd in FAILED_DOWNLOADS:
            logf.write(f"{out_bam}\t{cmd}\n")
# cleanup, rm all *.crai files
crai_files=glob.glob(os.path.join(outdir, '*.crai'))
for cf in crai_files:
    os.remove(cf)

print(f" total time: {time.time()-t_0} seconds ")


    




#!/usr/bin/env python3

import argparse
import os
import glob
import pandas as pd
import subprocess

parser=argparse.ArgumentParser()
parser.add_argument("--indir", default='../../data/2026_10-icgc_sv_vcf/icgc/controlled')
parser.add_argument('--outdir', default='reheadered_vcfs')
parser.add_argument('--vcf2donor', default='vcf2donor.tsv')
parser.add_argument('--vcf_suffix', default='.vcf.gz')
args = parser.parse_args()

os.makedirs(args.outdir,exist_ok=True)

def reheader(in_vcf: str, donorid: str, out_vcf: str):
    cmd = "printf '##INFO=<ID=BLACKLIST,Number=.,Type=String,Description=\"Temporary definition\">\\n' > tmp.hdr && "
    cmd += f"bcftools view -i 'INFO/SVCLASS=\"DEL\"' {in_vcf} | "
    cmd += "bcftools annotate -h tmp.hdr -x INFO/BLACKLIST | "
    cmd += f'bcftools reheader -s <(printf "{donorid}_NORMAL\\n{donorid}_TUMOR\\n") | '
    cmd += f'bgzip -c > {out_vcf} && bcftools index {out_vcf}'
    print(f"# running cmd: {cmd}")
    result = subprocess.run(cmd,shell=True,check=True,executable="/bin/bash")
    return result.returncode

#NORMAL\TTUMOUR
def main():
    vcfs = glob.glob(f"{args.indir}/*{args.vcf_suffix}")
    s = pd.read_csv(args.vcf2donor,sep='\t').set_index('vcf_file').squeeze()
    return_codes = []
    for vcf in vcfs:
        base = os.path.basename(vcf)
        donorid=s[base]
        out = '.'.join(base.split('.')[1:])
        out = '.'.join([donorid, out])
        out = os.path.join(args.outdir,out)
        return_code = reheader(vcf, donorid, out)
        return_codes.append(return_code)
    assert all([x == 0 for x in return_codes])

if __name__ == "__main__":
    main()

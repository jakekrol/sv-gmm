#!/usr/bin/env python3

import argparse
import cyvcf2
import matplotlib.pyplot as plt
import numpy as np

parser=argparse.ArgumentParser()
parser.add_argument("--input",default="merged_dels-recommended-multi_sample.vcf")
parser.add_argument("--output", default="hist_del_sample_count.png")
parser.add_argument("--bins", default=10)
parser.add_argument("--title", default="PCAWG DELs")
args = parser.parse_args()
args.bins=int(args.bins)


def main():
    vcf=cyvcf2.VCF(args.input)
    samples=[]
    for v in vcf:
        # 0 -> hom. ref, 1 -> het. alt, 2 -> unknown, 3 -> hom. alt
        num_alt = np.sum((v.gt_types == 1) | (v.gt_types == 3))
        samples.append(num_alt)
    fig,ax = plt.subplots(nrows=1,ncols=1,figsize=(6,4))
    ax.hist(samples,bins=args.bins, color='black')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.set_title(args.title,loc='left')
    ax.set_xlabel('Num. carriers')
    ax.set_ylabel('Count')
    plt.savefig(args.output)

if __name__=="__main__":
    main()


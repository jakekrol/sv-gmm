#!/usr/bin/env python3
import argparse
import csv
from cyvcf2 import VCF
import re

parser=argparse.ArgumentParser()
parser.add_argument("--input",default="merged_dels-recommended-multi_sample.vcf")
parser.add_argument("--output",default="merged_dels-recommended-multi_sample.csv")
args=parser.parse_args()

def main():
    vcf = VCF(args.input)
    samples = vcf.samples
    allele_number = 2 * len(samples)

    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id", "chr", "start", "stop", "svlen", "ref", "alt",
            "qual", "filter", "af", "info", *samples, "num_samples"
        ])
        for v in vcf:
            genotypes = v.genotypes
            allele_count = 0
            n_het_alt=0
            n_hom_alt=0
            for genotype in genotypes:
                # fill missing (-1) genotypes with 0
                a1=max(genotype[0],0)
                a2=max(genotype[1],0)
                if a1 == 0 and a2 == 1:
                    n_het_alt+=1
                    allele_count+=1
                if a1 == 1 and a2 == 1:
                    n_hom_alt+=1
                    allele_count+=2
            af = allele_count / allele_number
            end = int(re.search(r'[\[\]]\d+:(\d+)', v.ALT[0]).group(1))
            svlen=abs(v.POS-end)
            writer.writerow([
                v.ID,
                v.CHROM,
                v.start,
                v.end,
                svlen,
                v.REF,
                "<DEL>",
                v.QUAL,
                v.FILTERS,
                af,
                dict(v.INFO),
                *[str((max(gt[0],0),max(gt[1],0))) for gt in genotypes],
                n_het_alt+n_hom_alt
            ])

if __name__=="__main__":
    main()
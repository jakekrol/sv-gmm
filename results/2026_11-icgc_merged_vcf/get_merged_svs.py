#!/usr/bin/env python3

import argparse
import cyvcf2
parser=argparse.ArgumentParser()
parser.add_argument('--input', default='merged_dels-recommended.vcf')
parser.add_argument('--output', default='merged_dels-recommended-multi_sample.vcf')
args=parser.parse_args()

def main():
    vcf = cyvcf2.VCF(args.input)
    writer = cyvcf2.Writer(args.output, vcf)
    for variant in vcf:
        n = variant.INFO.get('NumConsolidated')
        if n:
            if n >=1:
                writer.write_record(variant)

if __name__=="__main__":
    main()
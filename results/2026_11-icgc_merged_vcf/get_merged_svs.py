#!/usr/bin/env python3

import argparse
import cyvcf2

parser=argparse.ArgumentParser()
parser.add_argument('--input', nargs='+', default=[
    'merged_dels-recommended.vcf',
    'merged_dels-loose.vcf',
    'merged_dels-loosest.vcf'
])
args=parser.parse_args()

def main():
    for path in args.input:
        name=path.removesuffix('.vcf')
        vcf=cyvcf2.VCF(path)
        writer=cyvcf2.Writer(f'{name}-multi_sample.vcf',vcf)

        n_merged=0
        for variant in vcf:
            n=variant.INFO.get('NumConsolidated')
            if n is not None and n >= 1:
                writer.write_record(variant)
                n_merged+=1

        writer.close()
        vcf.close()
        print(f'{path}: {n_merged} merged variants')

if __name__=="__main__":
    main()

# #!/usr/bin/env python3

# import argparse
# import cyvcf2
# parser=argparse.ArgumentParser()
# parser.add_argument('--input', default='merged_dels-recommended.vcf')
# parser.add_argument('--output', default='merged_dels-recommended-multi_sample.vcf')
# # parser.add_argument('--input', default='merged_dels-loosest.vcf')
# # parser.add_argument('--output', default='merged_dels-loosest-multi_sample.vcf')
# args=parser.parse_args()

# def main():
#     vcf = cyvcf2.VCF(args.input)
#     writer = cyvcf2.Writer(args.output, vcf)
#     for variant in vcf:
#         n = variant.INFO.get('NumConsolidated')
#         if n:
#             if n >=1:
#                 writer.write_record(variant)

# if __name__=="__main__":
#     main()
#!/usr/bin/env python3

# subset vcf to include SVs that
# have AC>=1 for >=1 samples in stix indices

import argparse
import cyvcf2
import glob
import os
import numpy as np
import pandas as pd
import subprocess
import yaml

parser=argparse.ArgumentParser()
parser.add_argument("--metadata", default="../../data/2026_11-icgc_metadata/pcawg-ega-metadata-map.tsv.gz")
parser.add_argument("--vcf", default="all_dels.vcf.gz")
parser.add_argument("--dir_index", default="/data/jake/stix-pcawg-dna")
parser.add_argument("--index_yaml_suffix", default="shard_metadata.yaml")
parser.add_argument("--output", default="filtered_dels.vcf.gz")
args = parser.parse_args()

def main():
    df = pd.read_csv(args.metadata,sep="\t").set_index('File_ID')
    vcf = cyvcf2.VCF(args.vcf)
    # get indexed samples
    samples_indexed = set()
    donors_indexed = set()
    yamls=glob.glob(f"{args.dir_index}/*{args.index_yaml_suffix}")
    for yml in yamls:
        with open(yml, "r") as f:
            data = yaml.safe_load(f)
            for shard, excord_files in data.items():
                for file in excord_files:
                    sample_fileid = os.path.basename(file).split('.')[0]
                    samples_indexed.add(sample_fileid)
                    donor_id = df.loc[sample_fileid, 'ICGC_Donor']
                    donors_indexed.add(donor_id)
    writer = cyvcf2.Writer(args.output, vcf)
    for variant in vcf:
        # 0 = HOM_REF, 1 = HET, 2 = UNKNOWN, 3 = HOM_ALT
        sample_idxs = np.where((variant.gt_types == 1) | (variant.gt_types == 3))[0]
        for idx in sample_idxs:
            donor_id = vcf.samples[idx].split('_')[0]
            if donor_id in donors_indexed:
                writer.write_record(variant)
    cmd = f'tabix -p vcf {args.output}'
    result = subprocess.run(cmd,shell=True,check=True)

if __name__=="__main__":
    main()
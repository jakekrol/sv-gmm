#!/usr/bin/env python3

import argparse
import glob
import os
import pandas as pd

parser=argparse.ArgumentParser()
parser.add_argument("--dir_vcf", default="../../data/2026_10-icgc_sv_vcf/icgc/controlled")
parser.add_argument("--vcf_suffix", default=".vcf.gz")
parser.add_argument("--icgc_metadata", default="../../data/2026_11-icgc_metadata/icgc25k-legacy-data-locations.no_index.tsv")
parser.add_argument("--icgc_metadata_sub", default="../../data/2026_11-icgc_metadata/pcawg-ega-metadata-map.tsv.gz")
parser.add_argument("--output",default="vcf2donor.tsv")
args = parser.parse_args()

COL_ICGC_META_FILE_NAME='File_Name'
COL_ICGC_META_FILE_ID='File_ID'
COL_ICGC_META_FILE_FORMAT='Format'
COL_ICGC_DONOR='ICGC_Donor'

def main():
    df_meta_full=pd.read_csv(args.icgc_metadata,sep="\t")
    mask = df_meta_full[COL_ICGC_META_FILE_FORMAT] == 'VCF'
    df_meta_full = df_meta_full[mask].reset_index(drop=True)
    df_meta_sub=pd.read_csv(args.icgc_metadata_sub,sep="\t")
    df_meta_full['file_name_prefix'] = df_meta_full[COL_ICGC_META_FILE_NAME].apply(lambda x: x.split('.')[0])
    df_meta_full.set_index('file_name_prefix',inplace=True)
    vcf_prefix2donor_id = df_meta_full[COL_ICGC_DONOR].to_dict()
    files = glob.glob(f"{args.dir_vcf}/*{args.vcf_suffix}")
    files = [os.path.basename(f) for f in files]
    vcf2donorid = []
    for f in files:
        donor_id = vcf_prefix2donor_id[f.split('.')[0]]
        vcf2donorid.append((donor_id,f))
    df_out=pd.DataFrame(vcf2donorid, columns=[COL_ICGC_DONOR, 'vcf_file'])
    assert df_out.isna().sum().sum() == 0
    df_out.to_csv(args.output,sep="\t",index=False)

if __name__ == "__main__":
    main()
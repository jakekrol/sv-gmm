#!/usr/bin/env python3
import pysam
import numpy as np
import sys
import os
import time
import datetime

# bams located here
# index = '/data/jake/sv-gmm/data/1kg_phase3_mapped.index'

args = sys.argv[1:]
print(args)
bamfile = args[0]
bamfile = 's3://1000genomes/phase3/' + bamfile
sample = os.path.basename(bamfile).split('.')[0]
print('sample:',sample)
dout = '/data/jake/sv-gmm/data/insert_sizes'
out = sample + '.isize'
out = os.path.join(dout,out)
print('out:',out)

def main():
    insert_sizes = []
    print(datetime.datetime.now())
    t_0 = time.time()
    with pysam.AlignmentFile(bamfile, "rb") as bam:
        for read in bam:
            if read.flag & 66 == 66:  # f66 -> properly paired, first in pair
                insert_sizes.append(abs(read.template_length))  # take absolute value for reverse strand reads

    mean_insert_size = np.mean(insert_sizes)
    print(f"Mean insert size: {mean_insert_size}")
    print(datetime.datetime.now())
    print(f"Time elapsed: {time.time() - t_0}")
    # write to outfile
    with open(os.path.join(dout,out), 'w') as f:
        f.write(str(mean_insert_size))
main()

# example small bam region
# bam_url = "s3://1000genomes/phase3/data/HG00105/alignment/HG00105.mapped.ILLUMINA.bwa.GBR.low_coverage.20130415.bam"
# start = 101347966
# end = 101348322
# chrm = str(9)

# insert_sizes = []

# with pysam.AlignmentFile(bam_url, "rb") as f_in:
#     for read in f_in.fetch(chrm, start, end):
#         if read.flag & 66 == 66:  # Properly paired, first in pair
#             print(read.template_length)
#             insert_sizes.append(abs(read.template_length))  # Take absolute value

# # Compute mean insert size
# mean_insert_size = np.mean(insert_sizes) if insert_sizes else 0
# print(f"Mean insert size: {mean_insert_size}")



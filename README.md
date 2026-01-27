# SV GMM

## Samplot

Visualizing sample-wise alignment evidence for variants across different modes from GMM.

### Updates

#### 04/11/2025
  - plots: data/2025_04_09-highcov-bams/merged

#### 03/23/2025

- Plotted high coverage sample SVs
  - data: data/high_cov.tsv
  - plots: data/2025_03_22-highcov-samplots/samplots.zip

#### 11/6/2024

- Add more read context (1000x sv length from each breakpoint) and set samplot start and end to the breakpoints. 

#### 11/5/2024

- Sample BAMs were downloaded from 1000 genomes (phase 3, low coverage) aws s3 
- For a given variant, samples (individuals) were randomly selected from different modes and samplot'ed adjacently for comparison.
    - This was repeated 5 times for each variant.

### Results

- [Summary PDF](summary.pdf)
    - Download or select `More pages` on GitHub interface to see full results.

- [Standalone figures](fig)

### GMM data

- [Variant modes in 1000 genomes](https://docs.google.com/spreadsheets/d/1klhSv6MtDizEIdVmCpj_MVYo6-WX41xfvY3Nto_tLz8/edit?usp=sharing)

### Code

- [Notebook for data collection and plotting](python/samplot.ipynb)

# SV GMM

## Samplot

Visualizing sample-wise alignment evidence for variants across different modes from GMM.

### Updates

#### 11/5/2024

- Sample BAMs were downloaded from 1000 genomes (phase 3, low coverage) aws s3 
- For a given variant, samples (individuals) were randomly selected from different modes and samplot'ed adjacently for comparison.
    - This was repeated 5 times for each variant

### Results

- [Summary PDF](summary.pdf)
    - Download or select `More pages` on GitHub interface to see full results 

- [Standalone figures](fig)

### GMM data

- [Variant modes in 1000 genomes](https://docs.google.com/spreadsheets/d/1klhSv6MtDizEIdVmCpj_MVYo6-WX41xfvY3Nto_tLz8/edit?usp=sharing)

### Code

- [Notebook for data collection and plotting](python/samplot.ipynb)

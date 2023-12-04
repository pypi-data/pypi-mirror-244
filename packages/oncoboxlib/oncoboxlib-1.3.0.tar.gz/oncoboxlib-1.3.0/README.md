# oncoboxlib

Oncobox library calculates Pathways Activation Levels (PAL) according to
Sorokin et al.(doi: 10.3389/fgene.2021.617059).
It takes a file that contains gene symbols in HGNC format (see genenames.org),
their expression levels for one or more samples (cases and/or controls)
and calculates PAL values for each pathway in each sample.

Online service is available at https://open.oncobox.com


## Installation

```sh
pip install oncoboxlib
```

## How to run the example

1. Create any directory that will be used as a sandbox. Let's assume it is named `sandbox`.


2. Extract `resources/databases.zip` into `sandbox/databases/`.
  <br> (You may download the archive from 
  `https://gitlab.com/oncobox/oncoboxlib/-/blob/master/resources/databases.zip`)
  

3. Extract example data `resources/cyramza_normalized_counts.txt.zip` into `sandbox`.
  <br> (You may download the archive from 
  `https://gitlab.com/oncobox/oncoboxlib/-/blob/master/resources/cyramza_normalized_counts.txt.zip`)
  

What it looks like now:
```
   - sandbox
       - databases
           - Balanced 1.123
           - KEGG Adjusted 1.123
           ...
       - cyramza_normalized_counts.txt  
```

4. Change directory to `sandbox` and execute the command:
```sh
oncoboxlib_calculate_scores --databases-dir=databases/ --samples-file=cyramza_normalized_counts.txt
```
It will create a result file `sandbox\pal.csv`.


Alternatively, you can use it as a library in your source code.
For details please see `examples` directory.


## Input file format

Table that contains gene expression.
Allowed separators: comma, semicolon, tab, space.
Compressed (zipped) files are supported as well.

- First column - gene symbol in HGNC format, see genenames.org.
- Others columns - gene expression data for cases or controls.
- Names of case columns should contain "Case", "Tumour", or "Tumor", case insensitive.
- Names of control columns should contain "Control" or "Norm", case insensitive.

It is supposed that data is already normalized by DESeq2, quantile normalization or other methods.


## Command line tool help

To read the complete help, run the tool with the `-help` argument:
```sh
oncoboxlib_calculate_scores --help
```

Here is the output (for convenience):
```
usage: calculate_scores.py [-h] --samples-file SAMPLES_FILE
                           [--controls-file CONTROLS_FILE] [--ttest]
                           [--fdr-bh] --databases-dir DATABASES_DIR
                           [--databases-names DATABASES_NAMES]
                           [--results-file RESULTS_FILE]

Command line tool for calculation of pathway activation level according to
doi: 10.3389/fgene.2021.617059

optional arguments:
  -h, --help            show this help message and exit
                        
  --samples-file SAMPLES_FILE
                        Table that contains gene expression for cases (or
                        cases and controls). Allowed separators: comma,
                        semicolon, tab, space. Compressed (zipped) files are
                        supported as well. First column - gene symbol in HGNC
                        format, see genenames.org. Others columns - gene
                        expression data for cases or controls. Names of case
                        columns should contain "Case", "Tumour", or "Tumor",
                        case insensitive. Names of control columns should
                        contain "Control" or "Norm", case insensitive. It is
                        supposed that data is already normalized by DESeq2,
                        quantile normalization or other methods.
                        
  --controls-file CONTROLS_FILE
                        Optional file that contains controls. If provided,
                        cases and controls will be increased by one and
                        normalized by quantile normalization.
                        
  --ttest               Include to result a column for unequal variance t-test
                        two-tailed p-values (aka Welch's t-test). It is
                        assumed that cases and norms are independent. t-test
                        will be performed between all cases and all controls.
                        
  --fdr-bh              Include to result a column for p-values corrected for
                        FDR using Benjamini/Hochberg method
                        
  --databases-dir DATABASES_DIR
                        Directory that contains pathway databases. Databases
                        can be downloaded from https://gitlab.com/oncobox/onco
                        boxlib/-/blob/master/resources/databases.zip (Biocarta
                        1.123, KEGG Adjusted 1.123, Metabolism 1.123, NCI
                        1.123, Qiagen 1.123, Reactome 1.123)
                        
  --databases-names DATABASES_NAMES
                        Names of databases that are used to calculate PALs.
                        "all" means that all database from --databases-dir
                        will be used.
                        
  --results-file RESULTS_FILE
                        Output file that will contain results, "pal.csv" by
                        default            
```

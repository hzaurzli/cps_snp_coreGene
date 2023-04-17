# cps_snp_coreGene
Look for the CPS backbone as well as call different strains CPS CNP and Indel

# Usage
## Install
```
# install env
conda env create -f cps_snp_coreGene.yaml

# activate env
source activate cps_snp_coreGene
```

## snp/indel
```
python cps_snp.py -fq1 xxx_1.clean.fq.gz -fq2 xxx_2.clean.fq.gz -rg cps2.fasta
## -fq1: fastq1
## -fq2: fastq2
## -rg: cps reference sequence(fa)
```
Result: VCF file

## Different strains cps
```
python cps_core.py -fq1 xxx_1.clean.fq.gz -fq2 xxx_2.clean.fq.gz -rg cps2.fasta
## -fq1: fastq1
## -fq2: fastq2
## -rg: cps reference sequence(fa)
```
Result:  Different strains cps fa file

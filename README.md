# Genome-wide association study(GWAS) using GEMMA

#GWAS is an statistical genetic approach to identified SNPs(marker in genome) associated with traits. Here, I am learning GWAS through repeating the analysis in: A new regulator of seed size control in Arabidopsis identified by a genome-wide association study. In this study, authors identified SNPs significantly associated to size of seed in 191 Arabidopsis inbred lines.

wget http://1001genomes.org/data/GMI-MPI/releases/v3.1/1001genomes_snp-short-indel_only_ACGTN.vcf.gz
#Download markers from 1001genome project.

vcftools --gzvcf 1001genomes_snp-short-indel_only_ACGTN.vcf.gz \
--remove-indels --min-alleles 2 --max-alleles 2 --recode --keep sample.txt --out 172sample
#Unzip the file and filter markers. Parameter --recode menas that markers passing the filteration were output. sample.txt includes the ID of inbred lines in this research, markers of which would be keep in output file in VCF format

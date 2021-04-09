# Genome-wide association study(GWAS) using GEMMA

#GWAS is an statistical genetic approach to identified SNPs(marker in genome) associated with traits. Here, I am learning GWAS through repeating the analysis in: A new regulator of seed size control in Arabidopsis identified by a genome-wide association study. In this study, authors identified SNPs significantly associated to size of seed in 191 Arabidopsis inbred lines.

wget http://1001genomes.org/data/GMI-MPI/releases/v3.1/1001genomes_snp-short-indel_only_ACGTN.vcf.gz
#Download markers from 1001genome project.


vcftools --gzvcf 1001genomes_snp-short-indel_only_ACGTN.vcf.gz \
--remove-indels --min-alleles 2 --max-alleles 2 --recode --keep sample.txt --out 172sample
#Unzip the file and filter markers. Parameter --recode menas that markers passing the filteration were output. sample.txt includes the ID of inbred lines in this research, markers of which would be keep in output file in VCF format


java -Xss5m -Xmx100g -jar $EBROOTBEAGLE/beagle.jar nthreads=20 gt=172sample.recode.vcf out=172sample_out ne=172
#Genotype imputation using beagle. A marker, genotyped in part of inbred lines, could not be genotyped in others  because of sequencing deepth and so on. Therefore, based on Linkage disequilibrium, imputation of the ungenotyped markers is necessary.


vcftools --gzvcf 172sample_out.vcf.gz --maf 0.05 --recode --out 172sample_maf_filter
#Filter SNP markers through the criterion of minnor allele frenquency > 0.05


awk '{FS="\t";OFS="\t"}{if($0~"#"){print $0}else{$3=$1"_"$2;print $0}}' 172sample_maf_filter.recode.vcf > 172sample_maf_filter_snpID.vcf
#Add ID in format of chr_position to the vcf file


plink --vcf 172sample_maf_filter_snpID.vcf --recode --out 172sample
#Transform vcf to binary format which could be recognized by PLINK


plink --file 172sample --indep 50 5 2;plink --file 172sample --extract plink.prune.in --recode --out 172sample_maf_filter_snpID_LD_filter
#Prune and extracting SNPs passing filteration



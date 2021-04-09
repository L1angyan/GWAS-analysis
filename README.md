# Genome-wide association study(GWAS) using GEMMA

#GWAS is an statistical genetic approach to identified SNPs(marker in genome) associated with traits. Here, I am learning GWAS through repeating the analysis in: A new regulator of seed size control in Arabidopsis identified by a genome-wide association study. In this study, authors identified SNPs significantly associated to size of seed in 191 Arabidopsis inbred lines.

# Clean data preparation
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
#Prune and extracting SNPs passing filteration. The first command would generate plink.prune.in including markers roughly linkage disdisequilibrium，prune.out including makers filtered. Here, marker filteration is completed.


plink --file 172sample_maf_filter_snpID_LD_filter --make-bed --out clean_snp
#--make-bed would genetated binary bed, bim and fam file. bed as well as bim file including SNPs infomation and fam is used to save phenotype data. Thus, I need to add the seed size of 172 Arabidopsis inbred lines.


python3 mergefam_sample.py
#Python scripts is used to add phenotype data to fam file. Phenotype data is avaiavle in supplement of the paper.


# Perform association analysis
gemma-0.98.1-linux-static -bfile clean_snp -gk 1 -o kinship                                                                                                                   #calculate kinship matrix as covariate. -gk parameter assign different method to calculate kinship default 1. If the SNPs are with small MAF but large effect, -gk 2 is more suitable.


gemma-0.98.1-linux-static -bfile clean_snp -lmm -k ./output/kinship.cXX.txt -o GWAS                                                                                             #Association analysis. The GWAS.assoc.txt is the result we need.
![QQ图片20210409104920](https://user-images.githubusercontent.com/46277338/114121762-8c322880-9921-11eb-8608-bc2b8ae841a6.png)


# Plot
rawdf<-read.table("GWAS_results.assoc.txt",header=T,sep="\t")

df<-data.frame(rs=rawdf$rs,chr=rawdf$chr,pos=rawdf$ps,pvalue=rawdf$p_wald)

install.packages("rMVP")

library(rMVP)

MVP.Report(df)                                                                                                                                                                #Generate 4 graphes, including qq plot, manhattan plot and SNP density.
![pvalue SNP-Density](https://user-images.githubusercontent.com/46277338/114122031-0d89bb00-9922-11eb-8d25-9f5acd6124b3.jpg)
![pvalue Rectangular-Manhattan](https://user-images.githubusercontent.com/46277338/114122042-111d4200-9922-11eb-91ab-8d4cb63b9e0e.jpg)
![pvalue QQplot](https://user-images.githubusercontent.com/46277338/114122045-12e70580-9922-11eb-82c7-a859b1266251.jpg)
![pvalue Circular-Manhattan](https://user-images.githubusercontent.com/46277338/114122048-137f9c00-9922-11eb-9c06-7a5e792f1c02.jpg)

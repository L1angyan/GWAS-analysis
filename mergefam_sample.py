import pandas as pd

sample = pd.read_table("../../sample/sample_list.csv",sep=",")
sample = sample.iloc[:,[1,5]]
#sample有191个样本，easyGWAS这一列为字符

fam = pd.read_table("clean_snp.fam",sep=" ",header=None)
fam.columns = ["ID1","ID2","parent1","parent2","sex","phenotype"]
fam["ID1"] = fam["ID1"].apply(str)
#fam有172个样本，前两列为数字

new_fam = pd.merge(fam,sample,how="inner",left_on="ID1",right_on="easyGWAS ID")
new_fam.phenotype = new_fam["Seed size (mm2)"]
new_fam = new_fam.iloc[:,range(0,6)]
new_fam = new_fam.round(decimals=9)
new_fam.to_csv("clean_snp.fam1",sep=" ",header=False,index=False)

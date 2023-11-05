import pandas as pd
import os

from tools_SONaa import *


# def import_raw_article_list(source =  "../data/publications/orcid"):
source =  "../data/publications/orcid"
files = os.listdir(source)

df = pd.DataFrame()

for file in files:
    # skip certain files
    if file in ['export_to_automated', 'export_to_manual', 'failed.csv']:
        continue
    
    # read file with articles
    uni_authors = pd.read_csv(source+"/"+file)
    
    df = pd.concat([df, uni_authors])
    
    df2 = df[['link', 'title']]
    
df.to_csv("t1.csv")

stor = []
for i, row in df2.iterrows():
    y = create_identificator(row)
    
    stor += [y]
    continue

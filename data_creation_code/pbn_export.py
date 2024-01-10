import json
import pandas as pd
from tools_SONaa import *
json_file = open(r'..\data\publications\pbn\updated_scientists.json', encoding="utf8")
test = json.load(json_file)

n = 0
j=0
dois = []
ID = []
for scientist in test:
    for article in scientist['results']:
        if article['type'] == 'ARTICLE':
            if isinstance(article['doi'], str):
                dois.append(article['doi'])
                ID.append(short_DOI(article['doi']))



orcid = pd.read_csv('../data/Orcid_raw_article_list.csv')
oID = orcid['Article_ID'].values.tolist()
new = [doi for doi in ID if doi not in oID]
doi_link = []
for n in new:
    doi_link.append(long_DOI(n))
pbn_nowe = pd.DataFrame()
pbn_nowe['DOI'] = new
pbn_nowe['link'] = doi_link


pbn_nowe.to_csv('../nowe_doi_do_sciagniecia.csv')
from statcheck.checkdir import checkPDFdir
import pandas as pd
import os

destination_dir = r'D:\data\ranking\statcheck_results'
dirs = [r'D:\data\ranking\pdfs\v1-1', r'D:\data\ranking\pdfs\v1-2', r'D:\data\ranking\pdfs\v1']


files = os.listdir(dirs[2])

for dir in dirs:
    Res, pRes = checkPDFdir(dir, subdir = False)
    Res.to_csv(os.path.join(destination_dir, os.path.basename(dir) + '_Res.csv'), index = False)
    pRes.to_csv(os.path.join(destination_dir, os.path.basename(dir) + '_pRes.csv'), index = False)

#########################################################
from statcheck.checkdir import checkPDF
from tqdm import tqdm
import os
dirs = [r'D:\data\ranking\pdfs\v1-1', r'D:\data\ranking\pdfs\v1-2', r'D:\data\ranking\pdfs\v1']


files = os.listdir(dirs[2])

file = r'D:\data\ranking\pdfs\v1-1\10-1002_job-2512.pdf'
base = r'D:\data\ranking\pdfs\v1'

res_list = []
pres_list = []
for file in tqdm(files):
    Res, pRes = checkPDF(os.path.join(base, file), messages= False)
    Res['Source'] = os.path.basename(file).replace('.pdf', '')
    pRes['Source'] = os.path.basename(file).replace('.pdf', '')
    res_list.append(Res)
    pres_list.append(pRes)

# concat
Res = pd.concat(res_list)
pRes = pd.concat(pres_list)

# save
Res.to_csv(os.path.join(destination_dir, 'v1_Res.csv'), index = False)
pRes.to_csv(os.path.join(destination_dir, 'v1_pRes.csv'), index = False)


# load all options
import pandas as pd
import os
destination_dir = r'D:\data\ranking\statcheck_results'
v1 = pd.read_csv(os.path.join(destination_dir, 'v1_pRes.csv'))
v11 = pd.read_csv(os.path.join(destination_dir, 'v1-1_pRes.csv'))
v2 = pd.read_csv(os.path.join(destination_dir, 'v1-2_pRes.csv'))

# cat
v = pd.concat([v1, v11, v2])
# nonna Reeported_P_Value
v = v[~v['Reported_P_Value'].isna()]
v = v.sort_values(by = ['Reported_P_Value'])

a = v[v['Reported_P_Comparison'] == '=']

a = a[['Source', 'Reported_P_Value']]
a.columns = ['Source', 'Value']

a = a[a['Value'] != 0.0]
a = a[a['Value'] < 1.0]

a.to_csv('D:/data/ranking/statcheck_results/eq.csv', index = False)
# load
a = pd.read_csv('D:/data/ranking/statcheck_results/eq.csv')

# to excel
a.to_excel('D:/data/ranking/statcheck_results/eq.xlsx', index = False)


# sort
a = a.sort_values(by = ['Value'])


r1 = pd.read_csv(os.path.join(destination_dir, 'v1_Res.csv'))
r11 = pd.read_csv(os.path.join(destination_dir, 'v1-1_Res.csv'))
r2 = pd.read_csv(os.path.join(destination_dir, 'v1-2_Res.csv'))
r = pd.concat([r1, r11, r2])

r = r[['Computed_P_Value', 'Source']]
r.columns = ['Value', 'Source']
r.to_csv('D:/data/ranking/statcheck_results/computed.csv', index = False)

import PyPDF2
import re
file = r'D:\data\ranking\pdfs\v1\10-1177_1368430220967975.pdf'

pdfFileObj = open(file, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
text = ""
for page in range(pdfReader.numPages):
    text += pdfReader.getPage(page).extractText()

# this code gets rid of XML artifacts
raw_text = text.encode('unicode_escape').decode('utf-8')
regex = r'\\x[0-9]{2}'
modified_text = re.sub(regex, ' ', raw_text)
modified_text = modified_text.encode('utf-8').decode('unicode_escape')

Res, pRes = checkPDF(file, messages=False)

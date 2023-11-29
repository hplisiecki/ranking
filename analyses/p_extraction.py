from statcheck.checkdir import checkPDFdir
import pandas as pd
import os

destination_dir = r'D:\data\ranking\statcheck_results'
dirs = [r'D:\data\ranking\pdfs\v1-1', r'D:\data\ranking\pdfs\v1-2', r'D:\data\ranking\pdfs\v1']


files = os.listdir(dirs[0])

for dir in dirs:
    Res, pRes = checkPDFdir(dir, subdir = False)
    Res.to_csv(os.path.join(destination_dir, os.path.basename(dir) + '_Res.csv'), index = False)
    pRes.to_csv(os.path.join(destination_dir, os.path.basename(dir) + '_pRes.csv'), index = False)


from statcheck.checkdir import checkPDF
from tqdm import tqdm
import os
dirs = [r'D:\data\ranking\pdfs\v1-1', r'D:\data\ranking\pdfs\v1-2', r'D:\data\ranking\pdfs\v1']


files = os.listdir(dirs[2])
selected_files = files[1250: 1350]

file = r'D:\data\ranking\pdfs\v1-1\4287931713577205598.pdf'
base = r'D:\data\ranking\pdfs\v1'

res_list = []
pres_list = []
for file in tqdm(files):
    Res, pRes = checkPDF(r'D:/data/ranking/pdfs/v1-1/5267354650028915100.pdf')
    Res['Source'] = os.path.basename(file).replace('.pdf', '')
    pRes['Source'] = os.path.basename(file).replace('.pdf', '')
    res_list.append(Res)
    pres_list.append(pRes)

    '5267354650028915100.pdf'





import PyPDF2

pdfFileObj = open(r'D:/data/ranking/pdfs/v1-1/5267354650028915100.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
text = ""
for page in range(pdfReader.numPages):
    text += pdfReader.getPage(page).extractText()

# this code gets rid of XML artifacts
raw_text = text.encode('unicode_escape').decode('utf-8')
regex = r'\\x[0-9]{2}'
modified_text = re.sub(regex, ' ', raw_text)
modified_text = modified_text.encode('utf-8').decode('unicode_escape')
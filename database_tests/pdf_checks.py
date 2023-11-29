import pandas as pd
import os
from tqdm import tqdm
import PyPDF2
import glob
import re

dir_automated = r'D:\PycharmProjects\ranking\data\publications\orcid\export_to_automated'
dir_manual = r'D:\PycharmProjects\ranking\data\publications\orcid\export_to_manual'
dir_pdfs_automated = r'D:\data\ranking\pdfs'

specific_pdf_dirs = ['v1', 'v1-1', 'v1-2']

all_pdfs_paths = []
for dir in specific_pdf_dirs:
    full_paths = glob.glob(os.path.join(dir_pdfs_automated, dir, "*.pdf"))
    all_pdfs_paths.extend(full_paths)

def pdf_to_text(url):
    pdfFileObj = open(url, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict = False)
    number = pdfReader.numPages
    text = ''
    for page in range(number):
        pageObj = pdfReader.getPage(page)
        # text.append(pageObj.extractText())
        text += pageObj.extractText()
        if page == 2:
            break
    return text, number

def contains_doi(text):
    pattern = r'\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b'
    return re.search(pattern, text) is not None

all_ids = [path.split('\\')[-1].replace('.pdf', '') for path in all_pdfs_paths]

articles = pd.read_csv(r'D:\PycharmProjects\ranking\export_dataset\raw_article_list.csv')

articles = articles[articles['Article_ID'].isin(all_ids)]

# sort the whole dataframe according to the order of the all_ids list

# unique
articles = articles.drop_duplicates(subset=['Article_ID'])
articles = articles.set_index('Article_ID').loc[all_ids].reset_index()

###################
# CHECKING TITLES #
###################

# just load
failed = []
length_list = []
correct_doi_list = []
contains_doi_list = []
for idx, path in tqdm(enumerate(all_pdfs_paths)):
    try:
        text, number = pdf_to_text(path)
        doi_value = articles['doi'][idx].replace('https://doi.org/', '')
        text_modified = ''.join(text.split(' ')).lower().replace('\n', '')
        if doi_value != 'empty' and doi_value in text_modified:
            correct_doi_list.append(True)
        elif doi_value == 'empty' and ''.join(articles['title'][idx].split(' ')).lower() in text_modified:
            correct_doi_list.append(True)
        else:
            correct_doi_list.append(False)
        length_list.append(number)
        contains_doi_list.append(contains_doi(text))
    except:
        failed.append(path)
        length_list.append(None)
        correct_doi_list.append(None)
        contains_doi_list.append(None)

articles['correct_doi'] = correct_doi_list
articles['length'] = length_list
articles['contains_doi'] = contains_doi_list

# save
articles.to_csv('data/checks/pdf_metadata_articles.csv', index=False)


###################

# load
articles = pd.read_csv('data/checks/pdf_metadata_articles.csv')

articles['path'] = all_pdfs_paths

correct_doi_articles = articles[articles['correct_doi'] == True]

# save to excel
correct_doi_articles.to_excel('data/checks/correct_doi_articles.xlsx', index=False)

incorrect_doi_articles = articles[articles['correct_doi'] == False] # 1092

title_based = incorrect_doi_articles[incorrect_doi_articles['doi'] == 'empty']

title_based.to_csv('data/checks/title_based_errors.csv')


doi_based = incorrect_doi_articles[incorrect_doi_articles['doi'] != 'empty']

doi_based.to_csv('data/checks/doi_based_errors.csv')

without_doi = doi_based[doi_based['contains_doi'] == False] # 583

with_doi = doi_based[doi_based['contains_doi'] == True]

# reset index
without_doi = without_doi.reset_index(drop=True)

idx = 0
print(with_doi['path'].iloc[idx])
print(with_doi['doi'].iloc[idx].replace('https://doi.org/', ''))
text, number = pdf_to_text(with_doi['path'].iloc[idx])

text_modified = ''.join(text.split(' ')).lower().replace('\n', '')















#####################
for idx, path in tqdm(enumerate(incorrect_paths)):
    try:
        text, number = pdf_to_text(path)
        doi_value = incorrect_doi_articles['Article_ID'][idx].replace('_', '/').replace('-', '.')
        print(doi_value)
        print(path)
        if doi_value != 'empty' and doi_value in text.lower():
            correct_doi_list.append(True)
        elif doi_value == 'empty' and ''.join(incorrect_doi_articles['title'][idx].split(' ')).lower() in ''.join(
                text.split(' ')).lower():
            correct_doi_list.append(True)
        else:
            correct_doi_list.append(False)
        length_list.append(number)
    except:
        failed.append(path)
        length_list.append(None)
        correct_doi_list.append(None)

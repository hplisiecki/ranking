import pandas as pd
import os
from tqdm import tqdm
import PyPDF2
import glob

dir_automated = r'D:\PycharmProjects\ranking\data\publications\orcid\export_to_automated'
dir_manual = r'D:\PycharmProjects\ranking\data\publications\orcid\export_to_manual'
dir_pdfs_automated = r'D:\data\ranking\pdfs'

specific_pdf_dirs = ['v1', 'v1-1', 'v1-2']

all_pdfs_paths = []
for dir in specific_pdf_dirs:
    full_paths = glob.glob(os.path.join(dir_pdfs_automated, dir, "*.pdf"))
    all_pdfs_paths.extend(full_paths)

###################
# CHECKING TITLES #
###################


def pdf_to_text(url):
    pdfFileObj = open(url, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict = False)
    # print(pdfReader.numPages)
    # text = []
    text = ''
    for page in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(page)
        # text.append(pageObj.extractText())
        text += pageObj.extractText()
    # if idx == 8:
    return text


# just load
failed = []
for path in tqdm(all_pdfs_paths):
    try:
        text = pdf_to_text(path)
    except:
        failed.append(path)
        continue


not_found_dict = {}
stats_dict = {}
failed_loads = {}
for uni in unis:
    print(uni)
    links = pd.read_csv(os.path.join(dir_automated, uni))
    dir_uni_pdfs = os.path.join(dir_pdfs_automated, uni.replace('.csv', ''))
    files = os.listdir(dir_uni_pdfs)
    not_found = []
    failed_load = []
    for id in tqdm(links.id.values):
        if id + '.pdf' in files:
            try:
                text = pdf_to_text(os.path.join(dir_uni_pdfs, id + '.pdf'))
            except:
                failed_load.append(id)
                continue
            title = links[links.id == id].title.values[0]
            text = ''.join(text.split()).lower()
            title = ''.join(title.split()).lower()
            if title not in text:
                not_found.append(id)

    stats_dict[uni.replace('.csv', '')] = len(not_found) / len(links.id.values)
    not_found_dict[uni.replace('.csv', '')] = not_found
    failed_loads[uni.replace('.csv', '')] = failed_load

import pandas as pd
import os
from tqdm import tqdm
import PyPDF2

dir_automated = r'D:\PycharmProjects\ranking\data\publications\orcid\export_to_automated'
dir_manual = r'D:\PycharmProjects\ranking\data\publications\orcid\export_to_manual'
dir_pdfs_automated = r'D:\data\ranking\pdfs'



#########################
# CHECKING AVAILABILITY #
#########################
not_found_dict = {}
stats_dict = {}
for uni in unis:
    links = pd.read_csv(os.path.join(dir_automated, uni))
    dir_uni_pdfs = os.path.join(dir_pdfs_automated, uni.replace('.csv', ''))
    files = os.listdir(dir_uni_pdfs)
    not_found = [id for id in links.id.values if str(id) + '.pdf' not in files]
    not_found_dict[uni.replace('.csv', '')] = not_found
    stats_dict[uni.replace('.csv', '')] = len(not_found) / len(links.id.values)
    break



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

# save all dicts
import pickle
with open('title_not_found_dict.pkl', 'wb') as f:
    pickle.dump(not_found_dict, f)

with open('title_stats_dict.pkl', 'wb') as f:
    pickle.dump(stats_dict, f)

with open('failed_loads.pkl', 'wb') as f:
    pickle.dump(failed_loads, f)
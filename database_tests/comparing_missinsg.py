import os
import pandas as pd

PDF_DIR = r'G:\My Drive\ranking_instytutow\data_completion\auto_download'

NEW_LINKS = r'../data/publications/orcid/export_to_automated'

OLD_LINKS = r'publication_links_old'

pdf_diff = {}

for file in os.listdir(NEW_LINKS):
    try:
        new_links = pd.read_csv(os.path.join(NEW_LINKS, file))
        old_links = pd.read_csv(os.path.join(OLD_LINKS, file))
        old_links = old_links[[True if 'https' in link  else False for link in old_links['link']]]
        uni_name = file.replace('.csv', '')
        existing_pdfs = os.listdir(os.path.join(PDF_DIR, uni_name))
        new_missing = [id for id in new_links['id'] if id not in existing_pdfs]
        old_missing = [id for id in old_links['id'] if id not in existing_pdfs]
        pdf_diff[uni_name] = len(new_missing) - len(old_missing)
    except:
        print("Skipping", file)
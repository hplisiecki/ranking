

def merge_and_make_ids(institute):
    orcid_df = pd.read_csv(f'data/swps_publication_links.csv')
    wos_df = pd.read_csv('data/swps_wos_links.csv')

    # drop nans from links
    wos_df = wos_df.dropna(subset=['doi'])
    wos_df['name'] = wos_df['fullname']
    wos_df['link'] = ['https://doi.org/' + l for l in wos_df['doi']]
    del wos_df['fullname']
    del wos_df['doi']

    # merge
    publications = pd.concat([orcid_df, wos_df], ignore_index=True)
    publications = publications.drop_duplicates(subset=['link'])
    # reset index
    publications = publications.reset_index(drop=True)

    ids = []
    for name in publications.name.unique():
        df_name = publications[publications.name == name]
        for i in range(len(df_name)):
            ids.append(name.replace(' ', '_') + '_' + str(i + 1))

    publications['id'] = ids

    links = [1 if 'https' in p else 0 for p in publications.link.values ]
    publications['is_a_link'] = links
    publications.to_csv(f'data/{institute}_publications_merged_ids.csv', index=False)



# def automatic_title_fill(institute):
#     publications_df = pd.read_csv(f'data/{institute}_publications_merged_ids.csv')
#
#
#     titles = publications_df[publications_df.is_a_link == 0].link.values
#
#     titles_df = publications_df[publications_df.is_a_link == 0]
#
#     browser = mechanize.Browser()
#     browser.set_handle_robots(False)
#     browser.addheaders = [('User-agent', 'Firefox')]
#
#     links = []
#     for number in tqdm(range(len(titles))):
#         title = titles[number]
#         proper = False
#         while proper == False:
#             try:
#                 browser.open('https://sci-hub.se')
#                 browser.select_form(nr=0)
#                 proper = True
#             except:
#                 print('sleep')
#                 time.sleep(60)
#         # use form
#         browser['request'] = title
#         response = browser.submit()
#         links.append(browser.geturl())
#         print(browser.geturl())
#
#     cnt = 0
#     for idx, link in enumerate(links):
#         if link != 'https://sci-hub.se/':
#             cnt += 1
#             # change the value in the dataframe
#             titles_df.iloc[idx, 2] = link
#             # get the index of the row
#             index = titles_df[titles_df['link'] == link].index[0]
#             # change the value in the dataframe
#             publications_df.iloc[index, 2] = link
#
#     publications_df.to_csv(f'data/{institute}_publications_merged_ids_after_auto_title.csv')
#
#     titles_df = publications[publications.is_a_link == 0].reset_index(drop=True)
#     titles_df.to_csv(f'data/{institute}_titles.csv', index=False)





def download_pdfs(institute):
    save_path = rf'D:\data\ranking\pdfs\'

    publications_df = pd.read_csv(rf'D:\data\ranking\publication_links\{file}')

    publications_with_links = publications_df[publications_df.is_a_link == 1].reset_index(drop=True)

    sh = SciHub()
    failed = []
    automatic_pdf_download = []
    for link, id in tqdm(zip(publications_with_links.link.values, publications_with_links.id.values)):
        try:
            name = str(id) + '.pdf'
            result = sh.download(link, path = name , destination= save_path)
            automatic_pdf_download.append(1)
        except:
            failed.append(link)
            automatic_pdf_download.append(0)

    import os
    files = os.listdir(save_path)
    files = [f.replace('.pdf', '') for f in files if '.pdf' in f]
    downloaded = [1 if i in files else 0 for i in publications_with_links.id.values]
    publications_with_links['automatic_pdf_download'] = downloaded
    # save
    publications_with_links.to_csv(f'data/{institute}_publications_with_links_after_auto_pdf.csv', index=False)


def main():
    from scihub_api import SciHub
    from tqdm import tqdm
    import mechanize
    from tqdm import tqdm
    import pandas as pd
    institute = 'swps'

    merge_and_make_ids(institute)
    automatic_title_fill(institute)
    download_pdfs(institute)

if __name__ == '__main__':
    main()



##################################################################################
# get list of files in the save_path
# load
publications_with_links = pd.read_csv('data/swps_publications_merged_ids.csv')



from selenium import webdriver
from bs4 import BeautifulSoup as bs
# geckodriver
options = webdriver.FirefoxOptions()

options.add_argument('--no-sandbox')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
driver = webdriver.Firefox(executable_path='D:/PycharmProjects/webdriver/geckodriver.exe' , options=options)

import requests
cnt = 0
for link in tqdm(links_failed):
    site = requests.get(link)
    soup = bs(site.content, 'html.parser')

pdf_link_list = []

url = 'https://doi.org/10.15611/pn.2018.512.13'
driver.get(url)
# get the new url

html = driver.page_source
# get
soup = bs(html, 'html.parser')

new_url = driver.current_url


'https://hrcak.srce.hr/clanak/276163'
'https://doi.org/10.2478/v1067-010-0159-2'
'https://doi.org/10.1515/ppb-2017-0060'
'https://doi.org/10.14691/cppj.24.1.201'
'https://doi.org/10.14656/pfp20170304'
'https://doi.org/10.7366/1896180020174007'
'https://doi.org/10.15611/pn.2018.512.13'
'https://doi.org/10.7366/1896180020174002'
'https://doi.org/10.15678/pjoep.2017.11.02'
'https://doi.org/10.15678/pjoep.2017.11.03'
'https://doi.org/10.15678/pjoep.2017.11.04'
'https://doi.org/10.7420/ak2018a'




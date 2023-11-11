import pandas as pd
from tqdm import tqdm
import time
import re
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import os
from bs4 import BeautifulSoup as bs

def get_doi_from_html(html, date_range = (2017, 2022)):
    longer = False
    soup = bs(html, 'html.parser')
    # find strong
    works = soup.find_all('div', {'class': 'clickable'})
    works = [w for w in works if 'Works' in w.text][0].text

    # get all divs with class 'panel-data-container'
    divs = soup.find_all('div', {'class': 'panel-data-container'})
    
    # get all divs containing 'Journal article
    divs = [div for div in divs if 'Journal article' in str(div)]
    
    # get all in every div with class 'general-data' and not class 'general-data ng-star-inserted'
    d_divs = [div.find_all('div', {'class': 'general-data'}) for div in divs]
    cleaned = []
    for d_div in d_divs:
        for d in d_div:
            if 'general-data ng-star-inserted' not in str(d):
                cleaned.append(d)
    dates = [find_date(str(div))[0] for div in cleaned]
    
    # check if there is a date lower than 2017
    if 'of' in works:
        if not any([date < str(date_range[0]) for date in dates]):
            longer = True

    divs_in_range = []
    limited_dates = []
    for (div, date) in zip(divs, dates):
        # check if date is within range
        if date == 'unrecovered':
            divs_in_range.append(div)
            limited_dates.append(date)
        elif int(date.split('-')[0]) in range(date_range[0], date_range[1]):
            divs_in_range.append(div)
            limited_dates.append(date)

    # find http links in every div
    titles = []
    links = []
    journals = []
    for div in divs_in_range:
        a = div.find_all('a')
        link = 'empty'
        
        # get link
        for i in a:
            if 'http' in str(i) and 'doi' in str(i):
                # extract link
                link = str(i).split('href="')[1].split('"')[0]

        
        # get title
        title_container = div.parent.parent.parent.previousSibling
        # get h2
        title = title_container.text

        # find 'ngcontent-iyt-c176=' div
        b = div.find_all('div', {'class': 'general-data ng-star-inserted'})
        journal = b[0].text.replace('\n', '').strip()

        links.append(link)
        titles.append(title)
        journals.append(journal)

    return links, titles, longer, journals, limited_dates

def find_date(string):
    pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    date = pattern.findall(string)
    # if date is not found
    if len(date) == 0:
        # try format year month
        pattern = re.compile(r'\d{4}-\d{2}')
        date = pattern.findall(string)
    if len(date) == 0:
        # try format year
        pattern = re.compile(r'\d{4}')
        date = pattern.findall(string)
    if len(date) == 0:
        date = ['unrecovered']
    return date

def scrape_orcids(links_df):

    checked = links_df[links_df['Checked'] == 1]

    name_orcid = [(fullname, orcid) for fullname, orcid in zip(checked['fullname'], checked['orcid']) if 'orcid' in str(orcid)]

    # scrape orcid website
    from selenium import webdriver
    from bs4 import BeautifulSoup as bs
    # geckodriver
    options = webdriver.FirefoxOptions()

    options.add_argument('--no-sandbox')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    links_list = []
    names_list = []
    titles_list = []
    orcids_list = []
    failed = []
    dates_list = []
    journals_list = []
    for name, orcid in tqdm(name_orcid):
        try:
            driver.get(orcid)
            time.sleep(5)
            html = driver.page_source
            links, titles, longer, journals, limited_dates = get_doi_from_html(html)

            if longer:
                try:
                    button_css_path = 'html body app-root.desktop.columns-12 div div.router-container app-my-orcid.ng-star-inserted div.container.no-padding.ng-star-inserted div.row main#main.col.l9.m8.s4 app-main app-work-stack-group#cy-works.ng-star-inserted form#cy-works-form.ng-untouched.ng-pristine.ng-valid.ng-star-inserted app-panels#cy-works-panels.row.ng-star-inserted div.col.s4.m8.l12.content.no-gutters.ng-star-inserted mat-paginator.mat-paginator.ng-star-inserted div.mat-paginator-outer-container div.mat-paginator-container div.mat-paginator-range-actions button.mat-focus-indicator.mat-tooltip-trigger.mat-paginator-navigation-next.mat-icon-button.mat-button-base span.mat-button-wrapper svg.mat-paginator-icon'
                    button = driver.find_element('css selector', button_css_path)
                    button.click()
                    time.sleep(5)
                    html = driver.page_source
                    more_links, titles, longer, journals, limited_dates = get_doi_from_html(html)
                    links.extend(more_links)

                except:
                    pass

            links_list.extend(links)
            titles_list.extend(titles)
            names_list.extend([name] * len(links))
            orcids_list.extend([orcid] * len(links))
            dates_list.extend(limited_dates)
            journals_list.extend(journals)

        except:
            failed.append(orcid)

    # save a = div.parent.parent.parent.previousSibling
    df = pd.DataFrame({'name': names_list, 'orcid': orcids_list, 'link': links_list, 'title': titles_list,'date': dates_list, 'journal': journals_list})


    return failed, df

def main(uni_name = None, data_dir = r'../anonymized/data/institutions', export_dir = r'../data/publications/orcid', format = 'names.xlsx'):

    if uni_name == None:
        directories = os.listdir(data_dir)
    else:
        directories = [uni_name]

    failed_list = []
    uni_list = []

    for uni in tqdm(directories):
        print(uni)
        try:
            links_df = pd.read_excel(os.path.join(data_dir, uni, format))
        except:
            print(f"Failed to fetch names for {uni}.")
            continue
        failed, df = scrape_orcids(links_df)

        df.to_csv(os.path.join(export_dir, rf'{uni}.csv'), index=False)
        
        uni_list.extend([uni] * len(failed))
        failed_list.extend(failed)
        print('failed', failed)
    failed_df = pd.DataFrame({'uni': uni_list, 'failed': failed_list})
    failed_df.to_csv(os.path.join(export_dir, 'failed.csv'), index=False)


if __name__ == '__main__':
    main()
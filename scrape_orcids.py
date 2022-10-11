import pandas as pd
from tqdm import tqdm
import time
import re

# re find date format in string
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


# wos = 'https://www.webofscience.com/wos/author/record/2408412'
# driver.get(wos)
# time.sleep(4)
# html = driver.page_source
# soup = bs(html, 'html.parser')

swps_links = pd.read_csv('data/swps_links.csv')

checked = swps_links[swps_links['Checked'] == True]

name_orcid = [(fullname, orcid) for fullname, orcid in zip(swps_links.fullname, swps_links.orcid) if 'orcid' in str(orcid)]


# scrape orcid website
from selenium import webdriver
from bs4 import BeautifulSoup as bs
# geckodriver
options = webdriver.FirefoxOptions()

options.add_argument('--no-sandbox')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
driver = webdriver.Firefox(executable_path='D:/PycharmProjects/webdriver/geckodriver.exe' , options=options)

# swps_publication_dir = r'D:\data\ranking\swps'

date_range = (2017, 2022)

df = pd.DataFrame()
links_list = []
names_list = []
orcids_list = []
failed = []
dates_list = []
too_long = []
for name, orcid in tqdm(name_orcid):
    try:
        driver.get(orcid)
        time.sleep(3)
        html = driver.page_source
        soup = bs(html, 'html.parser')
        # find strong
        works = soup.find_all('div', {'class': 'orc-font-body-large clickable'})
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
                too_long.append(orcid)
                continue
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
        links = []
        for div in divs_in_range:
            a = div.find_all('a')
            link = 'empty'
            for i in a:
                if 'http' in str(i) and 'doi' in str(i):
                    # extract link
                    link = str(i).split('href="')[1].split('"')[0]

            if link == 'empty':
                title_container = div.parent.parent.parent.previousSibling
                # get h2
                link = title_container.find('h2').text # get title

            links.append(link)

        links_list.extend(links)
        names_list.extend([name] * len(links))
        orcids_list.extend([orcid] * len(links))
        dates_list.extend(limited_dates)

    except:
        failed.append(orcid)

# save a = div.parent.parent.parent.previousSibling
df = pd.DataFrame({'name': names_list, 'orcid': orcids_list, 'link': links_list, 'date': dates_list})


df.to_csv('data/swps_publication_links.csv', index=False)

publications = pd.read_csv('data/swps_publication_links.csv')
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
# counts = publications.name.value_counts()
# # plot
# plt.figure(figsize=(10, 10))
# plt.barh(counts.index, counts.values)

def redo_on_one(orcid, name):
    driver.get(orcid)
    time.sleep(3)
    html = driver.page_source
    soup = bs(html, 'html.parser')
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
    links = []
    for div in divs_in_range:
        a = div.find_all('a')
        link = 'empty'
        for i in a:
            if 'http' in str(i) and 'doi' in str(i):
                # extract link
                link = str(i).split('href="')[1].split('"')[0]

        if link == 'empty':
            title_container = div.parent.parent.parent.previousSibling
            # get h2
            link = title_container.find('h2').text  # get title

        links.append(link)

    links_list.extend(links)
    names_list.extend([name] * len(links))
    orcids_list.extend([orcid] * len(links))
    dates_list.extend(limited_dates)

# soup beautify html
# soup = bs(html, 'html.parser')
# # get all http links
# links = [link.get('href') for link in soup.find_all('a') if 'http' in str(link.get('href'))]
# links  [link for link in links if 'doi' in link]


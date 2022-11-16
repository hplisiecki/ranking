import time
from tqdm import tqdm
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
# geckodriver
options = webdriver.FirefoxOptions()

options.add_argument('--no-sandbox')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))


publications_with_links = pd.read_csv('data/swps_publications_with_links_after_auto_pdf.csv')
links_failed = publications_with_links[publications_with_links.automatic_pdf_download == 0]


type = []
direct_link = []
for link in links_failed.link.values:
    try:

        driver.get(link)
        time.sleep(8)
        html = driver.page_source
        soup = bs(html, 'html.parser')
        caught = False

        ###############################
        ###############################
        # pdf site links
        ###############################
        ###############################

        if 'journals.pan.pl' in driver.current_url:
            type.append('pdf_site')
            direct_link.append(driver.current_url)
            continue

        if 'Psychiatria Polska' in soup.text:
            pdf = [a for a in soup.find_all('a') if '.pdf' in str(a)]
            pdf_link = pdf[0]['href']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        if 'psychiatriapolska' in driver.current_url:
            pdf = [a for a in soup.find_all('a') if '.pdf' in str(a)]
            pdf_link = pdf[0]['href'].split(' ')[0]
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue


        elif 'Index Copernicus' in soup.text:
            pdf = [a for a in soup.find_all('meta') if r'/pdf/' in str(a)]
            pdf_link = pdf[0]['content']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif driver.current_url[-4:] == '.pdf':
            pdf_link = driver.current_url
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'Przegląd Psychologiczny' in soup.text:
            pdf = soup.find_all('a', class_='btn btn-primary obj_galley_link pdf')
            pdf_link = pdf[0]['href']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'Polish Psychological Bulletin' in soup.text:
            pdf = [a for a in soup.find_all('meta') if r'.pdf' in str(a)]
            pdf_link = pdf[0]['content']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'Psychological Bulletin' in soup.text and 'Polish Psychological Bulletin' not in soup.text:
            pdf = soup.find_all('a', class_='btn btn-secondary btn-download galley-link')
            pdf = [p for p in pdf if 'pdf' in p['href']]
            pdf_link = pdf[0]['href']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'Annals of Agricultural and Environmental Medicine' in soup.text:
            pdf = [a for a in soup.find_all('meta') if r'.pdf' in str(a)]
            pdf_link = pdf[0]['content'].split(' ')[0]
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'Cardiology Journal' in soup.text:
            pdf = soup.find_all('a', class_='access')
            pdf = [p for p in pdf if 'view' in p['href']]
            pdf_link = pdf[0]['href']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'ijomeh' in driver.current_url:
            pdf = soup.find_all('a', class_='abstractFullText dirLeft')
            pdf_link = pdf[0]['href'].split(' ')[0]
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'Med Pr' in soup.text:
            pdf = soup.find_all('a', class_='abstractFullText dirLeft')
            pdf_link = pdf[0]['href'].split(' ')[0]
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'revistia' in driver.current_url:
            pdf = soup.find_all('a', class_='obj_galley_link file')
            pdf_link = pdf[0]['href']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'journals.plos' in driver.current_url:
            pdf = [a for a in soup.find_all('a') if 'downloadPdf' in str(a)]
            pdf_link = r'https://journals.plos.org' + pdf[0]['href']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'link.springer' in driver.current_url:
            pdf = [a for a in soup.find_all('meta') if '.pdf' in str(a)]
            pdf_link = pdf[0]['content']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'ucpress.edu/collabra' in driver.current_url:
            pdf = [a for a in soup.find_all('meta') if '.pdf' in str(a)]
            pdf_link = pdf[0]['content']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'e-medjournal' in driver.current_url:
            pdf = [l for l in soup.find_all('a', class_='obj_galley_link pdf') if 'Українська' not in l.text]
            pdf_link = pdf[0]['href']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'forumoswiatowe' in driver.current_url:
            pdf_link = driver.current_url
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'l1research' in driver.current_url:
            pdf = soup.find_all('a', class_='obj_galley_link pdf')
            pdf_link = pdf[0]['href']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'dovepress' in driver.current_url:
            pdf = [a for a in soup.find_all('meta') if 'citation_pdf_url' in str(a)]
            pdf_link = pdf[0]['content']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'bmcgeriatr' in driver.current_url:
            pdf = [p for p in soup.find_all('a') if 'download pdf' in str(p)]
            pdf_link = pdf[0]['href']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'globalizationandhealth.biomedcentral' in driver.current_url:
            pdf = [a for a in soup.find_all('meta') if 'citation_pdf_url' in str(a)]
            pdf_link = pdf[0]['content']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'nature.com' in driver.current_url:
            pdf = [a for a in soup.find_all('meta') if 'citation_pdf_url' in str(a)]
            pdf_link = pdf[0]['content']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'jmir' in driver.current_url:
            pdf = [a for a in soup.find_all('meta') if 'citation_abstract_pdf_url' in str(a)]
            pdf_link = pdf[0]['content']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'bmcpregnancychildbirth' in driver.current_url:
            pdf = [a for a in soup.find_all('meta') if '.pdf' in str(a)]
            pdf_link = pdf[0]['content']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'journals.pan.pl' in driver.current_url:
            pdf_link = driver.current_url
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'e-psychologiawychowawcza' in driver.current_url:
            pdf = [a for a in soup.find_all('meta') if 'citation_pdf_url' in str(a)]
            pdf_link = pdf[0]['content']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'psychologicabelgica' in driver.current_url:
            pdf = [a for a in soup.find_all('meta') if 'citation_pdf_url' in str(a)]
            pdf_link = pdf[0]['content']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'bmcpublichealth.biomedcentral' in driver.current_url:
            pdf = [a for a in soup.find_all('meta') if '.pdf' in str(a)]
            pdf_link = pdf[0]['content']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        elif 'dbc.wroc' in driver.current_url:
            pdf = soup.find_all('a', class_='download__all-button js-analytics-content')
            pdf_link = pdf[0]['href']
            type.append('pdf_site')
            direct_link.append(pdf_link)
            continue

        ###############################
        ###############################
        # download links
        ###############################
        ###############################

        elif 'Psychologia-Rozwojowa' in driver.current_url:
            pdf = [a for a in soup.find_all('meta') if r'pliki' in str(a)]
            pdf_link = pdf[0]['content']  # direct download link
            type.append('pdf_download')
            direct_link.append(pdf_link)
            continue

        elif 'pfp.ukw.edu' in driver.current_url:
            pdf = [a for a in soup.find_all('meta') if '.pdf' in str(a)]
            pdf_link = pdf[0]['content']  # download link
            type.append('pdf_download')
            direct_link.append(pdf_link)
            continue

        elif 'ejournals.eu/ijcm' in driver.current_url:
            pdf = [a for a in soup.find_all('meta') if 'fulltext_pdf' in str(a)]
            pdf_link = pdf[0]['content']  # download link
            type.append('pdf_download')
            direct_link.append(pdf_link)
            continue

        elif 'journalslibrary.nihr.' in driver.current_url:
            pdf = [a for a in soup.find_all('meta') if 'citation_pdf' in str(a)]
            pdf_link = pdf[0]['content']  # download link
            type.append('pdf_download')
            direct_link.append(pdf_link)
            continue

        elif 'kosmos.ptpk' in driver.current_url:
            pdf = [a for a in soup.find_all('meta') if 'citation_pdf_url' in str(a)]
            pdf_link = pdf[0]['content']  # download link
            type.append('pdf_download')
            direct_link.append(pdf_link)
            continue

        elif 'czasopisma.uni.lodz' in driver.current_url:
            pdf = soup.find_all('a', class_='obj_galley_link pdf')
            pdf_link = pdf[0]['href']  # download link
            type.append('pdf_download')
            direct_link.append(pdf_link)
            continue

        elif 'mdpi' in driver.current_url:
            pdf = [p for p in soup.find_all('meta') if 'citation_pdf_url' in str(p)]
            pdf_link = pdf[0]['content']  # download link
            type.append('pdf_download')
            direct_link.append(pdf_link)
            continue

        elif 'sciendo' in driver.current_url:
            pdf = [p for p in soup.find_all('meta') if 'citation_pdf_url' in str(p)]
            pdf_link = pdf[0]['content']  # download link
            type.append('pdf_download')
            direct_link.append(pdf_link)
            continue

        elif 'ojs.tnkul' in driver.current_url:
            pdf = soup.find_all('a', class_='obj_galley_link pdf')
            pdf_link = pdf[0]['href']  # download link
            type.append('pdf_download')
            direct_link.append(pdf_link)
            continue

        elif 'elifesciences' in driver.current_url:
            pdf = [a for a in soup.find_all('a') if 'data-download-type="pdf-article' in str(a)]
            pdf_link = pdf[0]['href']  # download link
            type.append('pdf_download')
            direct_link.append(pdf_link)
            continue

        elif 'jecs' in driver.current_url:
            pdf = soup.find_all('a', class_='obj_galley_link pdf')
            pdf_link = pdf[0]['href']  # download link
            type.append('pdf_download')
            direct_link.append(pdf_link)
            continue

        ###############################
        ###############################
        # scraping
        ###############################
        ###############################

        elif 'liebertpub' in driver.current_url:
            type.append('text_scraping')
            direct_link.append(driver.current_url)
            continue

        elif 'jasss.org' in driver.current_url:
            type.append('text_scraping')
            direct_link.append(driver.current_url)
            continue

        elif 'frontiersin' in driver.current_url:
            type.append('text_scraping')
            direct_link.append(driver.current_url)
            continue

        ###############################
        ###############################
        # for manual checks
        ###############################
        ###############################

        elif 'onlinelibrary.wiley' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'Polish Biochemical Society' in soup.text:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'Young Cardiology' in soup.text:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'psycnet.apa' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'tandfonline' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'doi.org' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'journals.kozminski' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'scholarlypublishingcollective.org/uip/ajp' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'econtent.hogrefe' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'psychologia-ekonomiczna' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'sciencedirect' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'protocols.io' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'cairn' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'czasopisma.tnkul' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'aimspress' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'scholar.com.pl' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'ingentaconnect' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'figshare.com' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'journals.lww' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'supp.apa.org' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'protocols.io' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'https://sciendo.com/journals/ppb/48/4/article-p430' in driver.current_url:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        elif 'sci-hub' in driver.current_url and 'Unfortunately' in soup.text:
            type.append('manual_checking')
            direct_link.append(link)
            continue

        type.append('slipped_through')
        direct_link.append(link)
    except:
        type.append('slipped_through')
        direct_link.append(link)

links_failed['type'] = type
links_failed['direct_link'] = direct_link

links_failed.to_csv('links_failed.csv', index=False)

unavailable = links_failed[links_failed['type'] == 'slipped_through']['link'].tolist()


from selenium import webdriver
from bs4 import BeautifulSoup as bs
# geckodriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
# geckodriver
options = webdriver.FirefoxOptions()

options.add_argument('--no-sandbox')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

import requests
cnt = 0
for link in tqdm(unavailable):
    driver.get(link)
    html = driver.page_source
    soup = bs(html, 'html.parser')
    'sci-hub' in driver.current_url and 'Unfortunately' in soup.text

    break

unavailable.pop(0)
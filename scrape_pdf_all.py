from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
import pandas as pd
import os
import time
import os
import glob
from tqdm import tqdm
from selenium.webdriver.common.by import By
import shutil



save_path = r'D:\data\ranking\pdfs'
downloads_url = r'C:\Users\hplis\Downloads'

def check_scihub(driver, url):
    if 'sci-hub' not in driver.page_source:
        # wait for 20 seconds
        print("Possible blank page. Waiting for 20 seconds.")
        time.sleep(20)
        # check again
        driver.get(url)
        check_scihub(driver, url)
    else:
        pass

for file in os.listdir(r'D:\data\ranking\publication_links'):
    failed = pd.DataFrame({'id': []})
    options = webdriver.FirefoxOptions()

    options.add_argument('--no-sandbox')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    if file in ['failed.csv', 'titles', 'other.csv', 'failed_swps.csv']:
        continue

    if os.path.exists(os.path.join(save_path, 'failed_pdf', file)):
        failed = pd.read_csv(os.path.join(save_path, 'failed_pdf', file))

    links = pd.read_csv(fr'D:\data\ranking\publication_links\{file}')

    links  = links[[True if 'http' in str(link) else False for link in links.link.values]]

    # create if not exists
    if not os.path.exists(os.path.join(save_path, file.replace('.csv', ''))):
        os.makedirs(os.path.join(save_path, file.replace('.csv', '')))
    counter = 0
    for link, id in tqdm(zip(links.link.values, links.id.values)):
        if os.path.exists(os.path.join(save_path, file.replace('.csv', ''), str(id) + '.pdf')):
            continue
        elif id in failed.id.values:
            continue
        counter += 1
        if counter % 50 == 0:
            driver.quit()
            time.sleep(40)
            options = webdriver.FirefoxOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        name = str(id)
        url = 'https://sci-hub.se/' + link
        driver.get(url)
        time.sleep(2)
        # check if "scihub" is on the page
        check_scihub(driver, url)
        try:
            button = driver.find_element(By.XPATH, '//button[text()="↓ save"]')
            button.click()
            time.sleep(1)
            # list all files in the directory
            files = glob.glob(os.path.join(downloads_url, "*"))

            # find the most recently downloaded file
            latest_file = max(files, key=os.path.getctime)

            # move the file to the save path
            shutil.move(latest_file, os.path.join(save_path, file.replace('.csv', ''), name + '.pdf'))


        except:
            continue

    files = os.listdir(os.path.join(save_path, file.replace('.csv', '')))
    downloaded_successfully = [True if i + '.pdf' in files else False for i in links.id.values]

    links['automatic_pdf_download'] = downloaded_successfully

    not_downloaded = links[links.automatic_pdf_download == False]

    # save
    not_downloaded.to_csv(rf'D:\data\ranking\pdfs\failed_pdf\{file}', index=False)

    # close driver
    driver.quit()

    time.sleep(40)



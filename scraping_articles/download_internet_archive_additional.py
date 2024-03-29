from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import pandas as pd
import os
import time
import os
import glob
from tqdm import tqdm
from selenium.webdriver.common.by import By
import shutil
import winsound
import requests
save_path = r'D:\data\ranking\pdfs'
downloads_url = r'C:\Users\hplis\Downloads'
files = glob.glob(os.path.join(downloads_url, "*"))

# find the most recently downloaded file
sorted_files = sorted(files, key=os.path.getctime)

latest_file = sorted_files[-1]
source_dir = r'D:\PycharmProjects\ranking\database_tests\problems'

def check_archive(driver, url):
    if 'archive' not in driver.page_source:
        # wait for 20 seconds
        print("Possible blank page. Waiting for 20 seconds.")
        time.sleep(20)
        # check again
        driver.get(url)
        check_archive(driver, url)
    else:
        pass


# ignore = ['failed.csv', 'titles', 'other.csv', 'failed_swps.csv', 'SWPS_Uniwersytet_Humanistycznospołeczny_z_siedzibą_w_Warszawie.csv', 'Akademia_Ignatianum_w_Krakowie.csv', 'Instytut_Psychologii_Polskiej_Akademii_Nauk.csv',
#           'Akademia_Pedagogiki_Specjalnej_Marii_Grzegorzewskiej_w_Warszawie.csv', 'Uniwersytet_Adama_Mickiewicza_w_Poznaniu.csv', 'Katolicki_Uniwersytet_Lubelski_Jana_Pawła_II_w_Lublinie.csv',
#           'Uniwersytet_Gdański.csv', 'Uniwersytet_Jagielloński_w_Krakowie.csv', 'Uniwersytet_Jana_Kochanowskiego_w_Kielcach.csv', 'Uniwersytet_Kardynała_Stefana_Wyszyńskiego_w_Warszawie.csv',
#           'Uniwersytet_Kazimierza_Wielkiego_w_Bydgoszczy.csv', 'Uniwersytet_Marii_Curie-Skłodowskiej_w_Lublinie.csv', 'Uniwersytet_Pedagogiczny_Komisji_Edukacji_Narodowej_w_Krakowie.csv',
#           'Uniwersytet_Szczeciński.csv', 'Uniwersytet_Warszawski.csv', 'Uniwersytet_Wrocławski.csv', 'Uniwersytet_Łódzki.csv', 'Uniwersytet_Śląski_w_Katowicach.csv']

ignore = ['failed.csv', 'titles', 'other.csv', 'failed_swps.csv']

for file in os.listdir(source_dir):
    # if file in ignore:
    #     continue
    if 'new_unpaired' not in file:
        continue
    failed = pd.DataFrame({'id': []})
    uni_name = file.replace('_new_unpaired.csv', '')

    options = webdriver.FirefoxOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    if os.path.exists(os.path.join(save_path, 'failed_pdf', file)):
        failed = pd.read_csv(os.path.join(save_path, 'failed_pdf', file))

    links = pd.read_csv(os.path.join(source_dir, file))

    links  = links[[True if 'http' in str(link) else False for link in links.link.values]]

    remain = []
    for link, id in tqdm(zip(links.link.values, links.id.values)):
        if os.path.exists(os.path.join(save_path, uni_name, str(id) + '.pdf')):
            remain.append(False)
        else:
            remain.append(True)

    left_links = links[remain]


    # create if not exists
    if not os.path.exists(os.path.join(save_path, uni_name)):
        os.makedirs(os.path.join(save_path, uni_name))
    counter = 0
    print(file)
    print('left links', len(left_links))
    for link, id in tqdm(zip(left_links.link.values, left_links.id.values)):
        counter += 1
        if counter % 50 == 0:
            driver.quit()
            time.sleep(40)
            options = webdriver.FirefoxOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        name = str(id)
        url = 'https://scholar.archive.org/'
        driver.get(url)
        WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
        search_box = driver.find_element(By.NAME , 'q')
        search_box.send_keys(link)
        search_button = driver.find_element(By.ID , 'search_submit_button')
        search_button.click()
        WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")

        check_archive(driver, url)

        try:
            css_selector = 'div.header > a:nth-child(1)'
            element = driver.find_element(By.CSS_SELECTOR, css_selector)
            element.click()
            # print('bip', id)
            # list all files in the directory
            downloading = True

        except:
            continue

        if '404 Not Found' in driver.page_source:
            print('404 Not Found')
            downloading = False
            continue

        if downloading:
            files = glob.glob(os.path.join(downloads_url, "*"))

            # find the most recently downloaded file
            sorted_files = sorted(files, key=os.path.getctime)
            temp_file = sorted_files[-1]
            second_latest = sorted_files[-2]
            while latest_file == temp_file or '.pdf' != temp_file[-4:] or latest_file != second_latest:
                time.sleep(1)
                files = glob.glob(os.path.join(downloads_url, "*"))

                # find the most recently downloaded file
                sorted_files = sorted(files, key=os.path.getctime)
                temp_file = sorted_files[-1]
                second_latest = sorted_files[-2]

            # move the file to the save path
            shutil.move(temp_file, os.path.join(save_path, uni_name, name + '.pdf'))
            # check if file already is in the given location
            time.sleep(10)
        # close second tab
        try:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except:
            pass


        files = glob.glob(os.path.join(downloads_url, "*"))

        # find the most recently downloaded file
        sorted_files = sorted(files, key=os.path.getctime)
        temp_file = sorted_files[-1]
        if temp_file != latest_file:
            print("Some issue with file movement")
            bug = True
            break

    files = os.listdir(os.path.join(save_path, uni_name))
    downloaded_successfully = [True if i + '.pdf' in files else False for i in links.id.values]

    links['automatic_pdf_download'] = downloaded_successfully

    not_downloaded = links[links.automatic_pdf_download == False]

    # save
    not_downloaded.to_csv(os.path.join(save_path, 'failed_pdf', file), index=False)

    # close driver
    driver.quit()

    time.sleep(1)




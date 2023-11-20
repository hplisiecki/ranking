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
from export_dataset.tools_SONaa import *
import winsound
import requests
import subprocess
import pickle
import sys
from selenium.webdriver.common.action_chains import ActionChains
# write Keys import
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService

save_path = r'D:\data\ranking\pdfs'
downloads_url = r'C:\Users\hplis\Downloads'

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


def close_driver(driver):
    try:
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            driver.close()
    except Exception as e:
        print(f"Error occurred while quitting driver: {e}")
        # Try to kill the geckodriver process
        subprocess.call(['taskkill', '/F', '/IM', 'geckodriver.exe'])



specific_pdf_dirs = ['v1', 'v1-1']

new_pdf_dir = 'v1-1-1'

def download_all():
    files = glob.glob(os.path.join(downloads_url, "*"))
    # find the most recently downloaded file
    sorted_files = sorted(files, key=os.path.getctime)
    LATEST_FILE = sorted_files[-1]

    with open(r'D:\PycharmProjects\ranking\data\publications\orcid\automated_doi\swps_links.pkl', 'rb') as f:
        # load the list of links
        links_list = pickle.load(f)

    with open(r'D:\PycharmProjects\ranking\data\publications\orcid\automated_doi\all_links_without_swps.pkl', 'rb') as f:
        # load the list of links
        temp_links = pickle.load(f)

    links_list.extend(temp_links)

    transformed_links = [create_Article_ID(link) + '.pdf' for link in links_list]

    downloaded_pdfs = []
    for pdf_dir in specific_pdf_dirs:
        temp_pdfs = glob.glob(os.path.join(save_path, pdf_dir, "*.pdf"))
        downloaded_pdfs.extend(temp_pdfs)

    current_downloaded = glob.glob(os.path.join(save_path, new_pdf_dir, "*.pdf"))
    downloaded_pdfs.extend(current_downloaded)

    sorted_files = sorted(current_downloaded, key=os.path.getctime)

    if len(sorted_files) > 0:
        last_downloaded_pdf = sorted_files[-1]
        last_downloaded_pdf = last_downloaded_pdf.split('\\')[-1]
        try:
            # locate index
            index = transformed_links.index(last_downloaded_pdf)
            # get all after the link
            links_list = links_list[index + 1:]
        except:
            pass

    downloaded_pdfs = [pdf.split('\\')[-1] for pdf in downloaded_pdfs]

    options = webdriver.FirefoxOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')

    # Set download preferences

    # Initialize the driver with the configured options
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    links_list = [link for link in links_list if create_Article_ID(link) + '.pdf' not in downloaded_pdfs]

    counter = 0
    for link in tqdm(links_list):
        id = create_Article_ID(link)
        id = str(id)

        if id + '.pdf' in downloaded_pdfs or os.path.exists(os.path.join(save_path, new_pdf_dir, id + '.pdf')):
            continue

        counter += 1
        if counter % 50 == 0:
            print('Restarting driver.')
            close_driver(driver)
            time.sleep(40)
            options = webdriver.FirefoxOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
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
            before_beep = 0
            while LATEST_FILE == temp_file or '.pdf' != temp_file[-4:] or LATEST_FILE != second_latest:
                time.sleep(1)
                files = glob.glob(os.path.join(downloads_url, "*"))

                # find the most recently downloaded file
                sorted_files = sorted(files, key=os.path.getctime)
                temp_file = sorted_files[-1]
                second_latest = sorted_files[-2]
                if len(driver.window_handles) == 1 and before_beep > 4 and before_beep % 3 == 0:
                    winsound.Beep(1000, 500)
                before_beep += 1

            # move the file to the save path
            shutil.move(temp_file, os.path.join(save_path, new_pdf_dir, id + '.pdf'))
            # check if file already is in the given location
            time.sleep(10)
        # close second tab
        try:
            driver.switch_to.window(driver.window_handles[1])
            # close the tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except:
            pass


        files = glob.glob(os.path.join(downloads_url, "*"))

        # find the most recently downloaded file
        sorted_files = sorted(files, key=os.path.getctime)
        temp_file = sorted_files[-1]
        if temp_file != LATEST_FILE:
            print("Some issue with file movement")
            bug = True
            break

    if not bug:
        # close  driver
        close_driver(driver)
        print('ALL PROCESSES FINISHED!')
    else:
        # report bug
        print("MAJOR BUG!")
        return



if __name__ == '__main__':
    # iterate until all files are downloaded
    while True:
        try:
            download_all()
            break
        except:
            # report the actual error
            print(sys.exc_info()[0])
            print("Error. Restarting in 30 seconds.")
            time.sleep(30)
            continue
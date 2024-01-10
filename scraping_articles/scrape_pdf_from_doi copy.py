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
from tools_SONaa import *
import pickle
import sys
import subprocess, signal

save_path = r'C:\data'
downloads_url = r'C:\Users\Paweł Lenartowicz\Downloads'

def check_scihub(driver, url):
    if 'sci-hub' not in driver.page_source:
        print("Possible blank page. Waiting for 20 seconds.")
        time.sleep(20)
        # check again
        driver.get(url)
        time.sleep(5)
        check_scihub(driver, url)
    else:
        pass

def check_scihub_post_button(driver, LATEST_FILE):  
    window_handles = driver.window_handles

    if len(window_handles) == 1 and '404 Not Found' not in driver.page_source:
        time.sleep(60)
        files = glob.glob(os.path.join(downloads_url, "*"))
        sorted_files = sorted(files, key=os.path.getctime)
        temp_file = sorted_files[-1]
        second_latest = sorted_files[-2]

        if LATEST_FILE == temp_file or '.pdf' != temp_file[-4:] or LATEST_FILE != second_latest:
            print("Possible blank page after button. Waiting for 10 seconds.")
            # check again
            driver.refresh()
            time.sleep(5)
            check_scihub_post_button(driver, LATEST_FILE)

    elif '404 Not Found' in driver.page_source:
        print('404 Not Found')
        return False

    return True


def close_driver(driver):
    try:
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            driver.close()
    except Exception as e:
        print(f"Error occurred while quitting driver: {e}")
        # Try to kill the geckodriver process
        subprocess.call(['taskkill', '/F', '/IM', 'geckodriver.exe'])

def download_all():
    files = glob.glob(os.path.join(downloads_url, "*"))
    # find the most recently downloaded file
    sorted_files = sorted(files, key=os.path.getctime)
    LATEST_FILE = sorted_files[-1]

    # load
    links_list = pd.read_csv('../nowe_doi_do_sciagniecia.csv')['link'].to_list()

    transformed_links = [short_DOI(link) + '.pdf' for link in links_list]

    downloaded_pdfs = glob.glob(os.path.join(save_path, "*.pdf"))
    sorted_files = sorted(downloaded_pdfs, key=os.path.getctime)
    last_downloaded_pdf = sorted_files[-1]
    last_downloaded_pdf = last_downloaded_pdf.split('\\')[-1]

    try:
        # locate index
        index = transformed_links.index(last_downloaded_pdf)
        # get all after the link
        links_list = links_list[index + 1:]
    except:
        pass

    # get the driver up and running
    options = webdriver.FirefoxOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))


    counter = 0
    bug = False
    for link in tqdm(links_list):

        # create article id
        id = create_Article_ID(link)
        id = str(id)

        # check if the file already exists or if it has been tried before
        if os.path.exists(os.path.join(save_path, id + '.pdf')):
            continue

        # update the counter and refresh if divisible by 50
        counter += 1
        if counter % 50 == 0:
            print('Restarting driver.')
            close_driver(driver)
            time.sleep(40)
            options = webdriver.FirefoxOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

        # get the first page
        url = 'https://sci-hub.se/' + link
        driver.get(url)
        WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")


        # check if "scihub" is on the page
        check_scihub(driver, url)

        # click the button
        try:
            button = driver.find_element(By.XPATH, '//button[text()="↓ save"]')
            button.click()
            time.sleep(1)
            # list all files in the directory
        except:
            continue

        # ensure good readout on the page
        downloading = check_scihub_post_button(driver, LATEST_FILE)

        # if it isn't downloading then skip it
        if not downloading:
            continue

        # if it is then move the file
        if downloading:
            files = glob.glob(os.path.join(downloads_url, "*"))

            # find the most recently downloaded file
            sorted_files = sorted(files, key=os.path.getctime)
            temp_file = sorted_files[-1]
            second_latest = sorted_files[-2]
            while LATEST_FILE == temp_file or '.pdf' != temp_file[-4:] or LATEST_FILE != second_latest:
                time.sleep(1)
                files = glob.glob(os.path.join(downloads_url, "*"))

                # find the most recently downloaded file
                sorted_files = sorted(files, key=os.path.getctime)
                temp_file = sorted_files[-1]
                second_latest = sorted_files[-2]

            # move the file to the save path
            shutil.move(temp_file, os.path.join(save_path, id + '.pdf'))
            # check if file already is in the given location
            time.sleep(10)

        # close second tab
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # double check if the file has been properly moved
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


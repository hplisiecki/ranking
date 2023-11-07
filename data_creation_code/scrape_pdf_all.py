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



def download_all():
    save_path = r'D:\data\ranking\pdfs'
    downloads_url = r'C:\Users\hplis\Downloads'
    files = glob.glob(os.path.join(downloads_url, "*"))

    # find the most recently downloaded file
    sorted_files = sorted(files, key=os.path.getctime)
    latest_file = sorted_files[-1]
    def check_scihub(driver, url):
        if 'sci-hub' not in driver.page_source:
            # wait for 20 seconds
            print("Possible blank page. Waiting for 20 seconds.")
            time.sleep(20)
            # check again
            driver.get(url)
            time.sleep(5)
            check_scihub(driver, url)
        else:
            pass

    def check_scihub_post_button(driver):
        window_handles = driver.window_handles

        if len(window_handles) == 1 and '404 Not Found' not in driver.page_source:
            # wait for 20 seconds
            print("Possible blank page after button. Waiting for 10 seconds.")
            time.sleep(10)
            # check again
            driver.refresh()
            time.sleep(5)
            check_scihub_post_button(driver)

        elif '404 Not Found' in driver.page_source:
            print('404 Not Found')
            return False

        return True

    for file in os.listdir(r'D:\PycharmProjects\ranking\data\publications\orcid\export_to_automated'):
        print(file)
        if file in []:
            continue
        failed = pd.DataFrame({'id': []})
        options = webdriver.FirefoxOptions()
        uni_name = file.replace('.csv', '')


        options.add_argument('--no-sandbox')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

        if file in ['failed.csv', 'titles', 'other.csv', 'failed_swps.csv']:
            driver.quit()
            continue

        if os.path.exists(os.path.join(save_path, 'failed_pdf', file)):
            failed = pd.read_csv(os.path.join(save_path, 'failed_pdf', file))

        links = pd.read_csv(fr'D:\PycharmProjects\ranking\data\publications\orcid\export_to_automated\{file}')

        links  = links[[True if 'http' in str(link) else False for link in links.link.values]]

        # create if not exists
        if not os.path.exists(os.path.join(save_path, uni_name)):
            os.makedirs(os.path.join(save_path, uni_name))
        counter = 0
        bug = False
        for link, id in tqdm(zip(links.link.values, links.id.values)):
            if os.path.exists(os.path.join(save_path, uni_name, str(id) + '.pdf')):
                continue
            # elif id in failed.id.values:
            #     continue
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
            WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")


            # check if "scihub" is on the page
            check_scihub(driver, url)

            downloading = False
            temp_file = latest_file
            try:
                button = driver.find_element(By.XPATH, '//button[text()="↓ save"]')
                button.click()
                time.sleep(1)
                # list all files in the directory
            except:
                continue

            downloading = check_scihub_post_button(driver)

            if not downloading:
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
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])


            files = glob.glob(os.path.join(downloads_url, "*"))

            # find the most recently downloaded file
            sorted_files = sorted(files, key=os.path.getctime)
            temp_file = sorted_files[-1]
            if temp_file != latest_file:
                print("Some issue with file movement")
                bug = True
                break

        if not bug:
            files = os.listdir(os.path.join(save_path, uni_name))
            downloaded_successfully = [True if i + '.pdf' in files else False for i in links.id.values]

            links['automatic_pdf_download'] = downloaded_successfully

            not_downloaded = links[links.automatic_pdf_download == False]

            # save
            not_downloaded.to_csv(rf'D:\data\ranking\pdfs\failed_pdf\{file}', index=False)

            # close driver
            driver.quit()

            time.sleep(30)
        else:
            break


if __name__ == '__main__':
    while True:
        try:
            download_all()
            break
        except:
            print("Error. Restarting in 30 seconds.")
            time.sleep(30)
            continue

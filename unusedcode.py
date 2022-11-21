#from wrangle.py:
#  new_columns = ['Lp', 'id', 'name', 'second_name', 'pre_surname', 'surname', 'uni_id', 'uni_name', 'date_start',
#                  'is_main_job', 'disciplines', 'work_title_name', 'work_title_disciplines', 'work_title_giver',
#                  'work_foreign_title_giver', 'work_title_date', 'work_title_country', 'science_title_name',
#                  'science_title_type', 'science_title_date' 'science_title_giver', 'science_foreign_title_reason',
#                  'science_foreign_title_giver', 'science_title_country']


numbers = df.id.value_counts()
df['number_of_affiliations'] = df.id.map(numbers)
a = df['uni_name'].value_counts()
## retain more than one
a = a[a > 1]

"""
not_psych = swps_waw[~swps_waw['disciplines'].str.contains('psycholog', na = False)]

psych = swps_waw[swps_waw['disciplines'].str.contains('psycholog', na = False)]


more_than_one = psych[psych['number_of_affiliations'] > 1]


not_main = more_than_one[more_than_one['is_main_job'] != 'Tak']
# reset index
not_main = not_main.reset_index(drop=True)

outside_list = ['Magdalena Witkowska', 'Marzenna Teresa Zakrzewska']
psych = psych[~psych['fullname'].isin(outside_list)]

names_and_starts = psych[['fullname', 'date_start']]
# dropn duplicates from fullnames
names_and_starts = names_and_starts.drop_duplicates(subset=['fullname'], keep='first')

names = names_and_starts[['fullname']]

filled_hubert = pd.read_csv('filled_hubert.csv')
filled_hubert = filled_hubert[filled_hubert.fullname.isin(names.fullname)]

# map orcids
orcids_hubert = filled_hubert[['fullname', 'orcid', 'assigned']]

# save
orcids_hubert.to_csv('orcids_hubert.csv', index=False)
# to excel
orcids_hubert.to_excel('orcids_hubert.xlsx', index=False)



assigned = []
assigned = ['Kacper' for i in range(63)]
assigned.extend(['Ignacy' for i in range(63)])
assigned.extend(['Paweł' for i in range(63)])
assigned.extend(['Hubert' for i in range(65)])

names['assigned'] = assigned
# reset index
names = names.reset_index(drop=True)

orcid = []
from selenium import webdriver

# geckodriver
options = webdriver.FirefoxOptions()

options.add_argument('--no-sandbox')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
driver = webdriver.Firefox(executable_path='D:/PycharmProjects/webdriver/geckodriver.exe' , options=options)

idx = 0
for name in tqdm(names['fullname']):
    idx += 1
    if idx == 50:
        # kill driver
        driver.quit()
        # wait 5 seconds
        time.sleep(5)
        # start new driver
        driver = webdriver.Firefox(executable_path='D:/PycharmProjects/webdriver/geckodriver.exe' , options=options)
        idx = 0

    if len(name.split(' ')) >2:
        name = name.split(' ')[0] + ' ' + name.split(' ')[-1]
    name = name.replace(' ', '+') + '+orcid'
    query = name
    url = f'''https://www.google.com/search?q={query}&hl=pl&source=hp&ei=BbAxY4XmJYKIur4Pr9yK4AM&iflsig=AJiK0e8AAAAAYzG-FfsbNbkBCu37xsS2P8eeNA1vzeH-&ved=0ahUKEwjF_IbhzrL6AhUChM4BHS-uAjwQ4dUDCAc&uact=5&oq=__query__&gs_lcp=Cgdnd3Mtd2l6EAMyBggAEB4QCjIECAAQHjIECAAQHjIECAAQHjIECAAQHjIECAAQHjIECAAQHjIECAAQHjIECAAQHjIECAAQHjoKCAAQ6gIQtAIQQzoTCC4QxwEQ0QMQ1AIQ6gIQtAIQQzoQCC4QxwEQ0QMQ6gIQtAIQQzoTCC4QxwEQrwEQ1AIQ6gIQtAIQQzoFCAAQgAQ6CAgAEIAEELEDOgUILhCABDoFCAAQkgM6BwgAEB4QyQM6CggAELEDEIMBEA06BwgAELEDEA06BAgAEA06BAguEBM6BggAEAoQEzoGCAAQHhATOggIABAeEAoQEzoFCAAQogRQlAZY5Cpg4yxoBnAAeACAAekBiAHsDpIBBjEuMTIuMZgBAKABAbABCg&sclient=gws-wiz'''
    driver.get(url)
    try:
        xpath = '/html/body/div[3]/div[3]/span/div/div/div/div[3]/div[1]/button[1]/div'
        # click
        driver.find_element('xpath', xpath).click()
    except:
        pass
    # get recovered urls
    xpath = '//div[@class="yuRUbf"]/a'
    urls = driver.find_elements('xpath', xpath)
    # to string
    urls = [url.get_attribute('href') for url in urls]
    found = False

    for url in urls:
        if 'orcid' in url:
            if found == False:
                orcid.append(url)
                found = True
    if found == False:
        orcid.append('')

names['orcid'] = orcid

# save
names.to_csv('names_with_orcids.csv')

import time

# load




names = pd.read_csv('names_with_orcids.csv')

from selenium import webdriver

# geckodriver
options = webdriver.FirefoxOptions()

options.add_argument('--no-sandbox')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
driver = webdriver.Firefox(executable_path='D:/PycharmProjects/webdriver/geckodriver.exe' , options=options)

legit = []
for name, orcid in tqdm(zip(names.fullname.values, names.orcid.values)):
    time.sleep(1)
    if len(name.split(' ')) >2:
        name = name.split(' ')[0] + ' ' + name.split(' ')[-1]
    # check if name is on the page
    try:
        driver.get(orcid)
        html = driver.page_source
        if name in html:
            legit.append(True)
        else:
            legit.append(False)
    except:
        legit.append(False)

names['legit'] = legit

names.to_csv('names_with_orcids.csv')
"""
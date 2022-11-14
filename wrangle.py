import time
import numpy as np
import pandas as pd
from tqdm import tqdm

# scientist.csv is file download from radon.pl wchich contains data for registered scientist in Poland. 
# Registration i obligatory for almost all active scienists, especialy those who works at Universities
df = pd.read_csv('scientists.csv')

#Selecting columns
df = df[['Lp', 'Id', 'Dane podstawowe - Imię', 'Dane podstawowe - Drugie imię',
         'Dane podstawowe - Przedrostek nazwiska', 'Dane podstawowe - Nazwisko',
         'Zatrudnienie - Id', 'Zatrudnienie - Nazwa']]

#changing names to English
df.columns = ['Lp', 'id', 'name', 'second_name', 'pre_surname', 'surname', 'uni_id', 
                'uni_name']

#filling missing names values
prev_id = 'melon'
names = []
for index, row in df.iterrows():
    if row['id'] != prev_id:
        prev_id = row['id']
        names_pieces = []
        if str(row['name']) != 'nan':
            first_name = row['name']
            names_pieces.append(first_name)
        if str(row['second_name']) != 'nan':
            second_name = row['second_name']
            names_pieces.append(second_name)
        if str(row['pre_surname']) != 'nan':
            pre_surname = row['pre_surname']
            names_pieces.append(pre_surname)
        if str(row['surname']) != 'nan':
            surname = row['surname']
            names_pieces.append(surname)
    names.append(' '.join(names_pieces))

df['fullname'] = names

#selecting institutes with at least 30 scientists
institutes = df['uni_name'].value_counts()
institutes = institutes[institutes > 29]
institutes.to_csv('institutes.csv')
institutes.colums = ['Uni.name','counts']


#for i in institutes


#institutes = list(set(df['uni_name'].to_list()))

#institutes = (i for i in institutes if str(i) != 'nan')

#swps_waw = df[df['uni_name'] == 'SWPS Uniwersytet Humanistycznospołeczny z siedzibą w Warszawie']


#duplicates = swps_waw[swps_waw.duplicated(subset=['fullname'], keep=False)]

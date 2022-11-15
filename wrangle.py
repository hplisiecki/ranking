import time
import numpy as np
import pandas as pd
from tqdm import tqdm
import os

# scientist.csv is file download from radon.pl wchich contains data for registered scientist in Poland. 
# Registration i obligatory for almost all active scienists, especialy those who works at Universities
df = pd.read_csv('scientists.csv')

#Selecting columns
df = df[['Id', 'Dane podstawowe - Imię', 'Dane podstawowe - Drugie imię',
         'Dane podstawowe - Przedrostek nazwiska', 'Dane podstawowe - Nazwisko', 'Zatrudnienie - Nazwa','Zatrudnienie - Podstawowe miejsce pracy',]]

#changing names to English
df.columns = ['id', 'name', 'second_name', 'pre_surname', 'surname', 
                'uni_name', 'is_a_main_job']

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

#create file with institutions' names
institutes.to_csv('institutes.csv')

#selecting scientists who are connected to selected institutions
df_selected=df[df['uni_name'].isin(institutes.index)]
#df_selected=df_selected[['id', 'fullname','uni_name']]
df_selected=df_selected.drop_duplicates(subset=['id'], keep='first')

#making file for sciencits who wasn't selected
df_notselected=df[~df['id'].isin(df_selected.id)]
df_notselected=df_notselected.drop_duplicates(subset=['id'], keep='first')

#making files for selected scientists
for i in institutes.index:
    x=df_selected[df_selected.uni_name==i]
    dir=os.path.join('test', i)
    if not os.path.exists(dir):
        os.makedirs(dir)
    x[['fullname', 'uni_name']].to_csv('%s/names.csv' % dir)

#making file for unselected
df_notselected[['fullname','uni_name']].to_csv('test/other/names.csv')
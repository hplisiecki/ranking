import time
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
from tqdm import tqdm
import os

# scientist.csv is file downloaded from radon.plm which contains data for registered scientist in Poland. 
# Registration i obligatory for almost all active scienists, especialy those who works at Universities
df = pd.read_csv('./data/scientists.csv')

#Selecting columns & changing names to English
df = df[['Id', 'Dane podstawowe - Imię', 'Dane podstawowe - Drugie imię',
         'Dane podstawowe - Przedrostek nazwiska', 'Dane podstawowe - Nazwisko', 
         'Zatrudnienie - Nazwa','Zatrudnienie - Podstawowe miejsce pracy',]]

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

#splitting into those, who declared "main job" and others
temp_df=df[df['is_a_main_job']=="Tak"]
unlisted=df[~df['id'].isin(temp_df.id)]
unlisted[['fullname', 'uni_name', 'is_a_main_job']].to_csv('./data/other/unlisted.csv')
df=temp_df

#selecting institutes with at least 25 listed scientists
institutes = df['uni_name'].value_counts()
institutes = institutes[institutes > 24]
institutes.to_csv('./data/institutes.csv')

#selecting scientists who are connected to selected institutions
df_selected=df[df['uni_name'].isin(institutes.index)]
df_notselected=df[~df['id'].isin(df_selected.id)]
df_notselected[['fullname','uni_name']].to_csv('./data/other/names.csv')

selected=pd.DataFrame()
#making files for selected scientists
for i in institutes.index:
    x=df_selected[df_selected.uni_name==i]
    selected=pd.concat([selected,x[['fullname','uni_name']]])
    dir=os.path.join('data', i)
    if not os.path.exists(dir):
        os.makedirs(dir)
    x[['fullname']].to_csv('%s/names.csv' % dir)

#making Where is Wally
selected['file']='selected'
df_notselected['file']='other-names'    
unlisted['file']="other-unlisted"
unlisted=unlisted.dropna()

WhereIsWally = pd.concat([
    selected,
    df_notselected[['fullname','uni_name','file']],
    unlisted[['fullname', 'uni_name', 'file','is_a_main_job']]
])

WhereIsWally.to_csv('./data/WhereIsWally.csv')
##### ###
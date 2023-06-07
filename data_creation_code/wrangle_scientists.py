import pandas as pd
pd.options.mode.chained_assignment = None
from tqdm import tqdm
import os

# scientist.csv is file downloaded from radon.pl database of registered scientist in Poland. 
# Registration i obligatory for almost all active scienists, especialy those who works at Universities
df = pd.read_csv('../data/scientists.csv')

# Selecting columns & changing names to English
df = df[['Id', 'Dane podstawowe - Imię', 'Dane podstawowe - Drugie imię',
         'Dane podstawowe - Przedrostek nazwiska', 'Dane podstawowe - Nazwisko', 
         'Zatrudnienie - Nazwa','Zatrudnienie - Podstawowe miejsce pracy',]]

df.columns = ['id', 'name', 'second_name', 'pre_surname', 'surname', 
                'uni_name', 'is_a_main_job']

# change names for interoperability
df=df.replace({'uni_name':'im. '},{'uni_name':''},regex=True)
df=df.replace({'uni_name':'sp. z o.o. '},{'uni_name':''},regex=True)
df=df.replace({'uni_name':' '},{'uni_name':'_'},regex=True)

# Filling missing names values
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

# Splitting into those, who declared "main job" and others
temp_df  = df[df['is_a_main_job']=="Tak"]
unlisted = df[~df['id'].isin(temp_df.id)]
unlisted = unlisted[['fullname', 'uni_name', 'is_a_main_job']].dropna()
unlistedNamesOnly = unlisted[['fullname']].drop_duplicates()

# Safe files
unlisted.to_csv('../data/institutions/other/unlisted.csv')
unlistedNamesOnly.to_csv('../data/institutions/other/unlisted_names_only.csv')

df = temp_df

# Creating dataset of institutions
institutes = df['uni_name'].value_counts().to_frame()

# Upload information about evaluation
evaluation = pd.read_csv('../data/institutions/evaluation_data.csv', index_col="uni_code")
institutes = institutes.join(evaluation)

# Select only evaluated institutes
institutes_ev = institutes.dropna()

# Save file with all institutes and evaluated
institutes.to_csv('../data/institutions/institutes_all.csv')
institutes_ev.to_csv('../data/institutions/institutes_ev.csv')

# Selecting scientists who are connected to evaluated institutions
df_selected    = df[df['uni_name'].isin(institutes_ev.index)]
df_notselected = df[~df['id'].isin(df_selected.id)]

# Safe notselecter to file
df_notselected[['fullname','uni_name']].to_csv('../data/institutions/other/names.csv')

selected=pd.DataFrame()

# Making files for selected scientists
for i in institutes_ev.index:
    x=df_selected[df_selected.uni_name==i]
    selected=pd.concat([selected,x[['fullname','uni_name']]])
    dir=os.path.join('../data/institutions', i)
    if not os.path.exists(dir):
        os.makedirs(dir)
    x[['fullname']].to_csv('%s/names.csv' % dir)

# Making Where is Wally
selected['file'] = 'selected'
df_notselected['file'] = 'other-names'    
unlistedNamesOnly['file']=  "other-unlisted"

WhereIsWally = pd.concat([
    selected[['fullname','file', 'uni_name']],
    df_notselected[['fullname','file']],
    unlistedNamesOnly[['fullname', 'file']]
])

WhereIsWally.to_csv('../data/institutions/WhereIsWally.csv')
##### ###

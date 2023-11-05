import pandas as pd
import os
import json
from tqdm import tqdm

# to do
# add other information
# remove brackets from 'fullname'

## this part is alternative to wrangle_scientists.py ##

def author_export(source = '../data/scientists.csv', dest = '../exportable_dataset/List_of_authors.csv'):
    
    df = pd.read_csv(file)
    # Selecting columns & changing names to English
    df = df[['Id', 'Dane podstawowe - Imię', 'Dane podstawowe - Drugie imię', 'Dane podstawowe - Przedrostek nazwiska', 'Dane podstawowe - Nazwisko', 
                'Zatrudnienie - Nazwa','Zatrudnienie - Podstawowe miejsce pracy', "Zatrudnienie - Oświadczone dyscypliny", "Stopnie naukowe - Stopień naukowy", "Stopnie naukowe - Rok uzyskania stopnia"]]

    df.columns = ['id', 'name', 'second_name', 'pre_surname', 'surname', 
                'uni_name', 'is_a_main_job', "declared_discipline", "degree", "degree_year"]

    # change univeristy names for interoperability
    df=df.replace({'uni_name':'im. '},{'uni_name':''},regex=True)
    df=df.replace({'uni_name':'sp. z o.o. '},{'uni_name':''},regex=True)
    df=df.replace({'uni_name':' '},{'uni_name':'_'},regex=True)

    authors_raw = df

    b = 0

    authors = pd.DataFrame()

    # Iterating by authors' ids
    for i in authors_raw.id.unique():
        
        df = authors_raw.loc[authors_raw["id"] == i]
        
        author = []
        
        for index, row in df.iterrows():

            if row['surname'] == row['surname']:
                author = row[['id', 'name', 'second_name', 'pre_surname', 'surname']]     
            
            if row['is_a_main_job'] == 'Tak':
                author['main_job'] = row['uni_name']
        

        names = []
        fullname = []
        if str(author['name']) != 'nan':
            first_name = author['name']
            fullname.append(first_name)
        if str(author['second_name']) != 'nan':
            second_name = author['second_name']
            fullname.append(second_name)
        if str(author['pre_surname']) != 'nan':
            pre_surname = author['pre_surname']
            fullname.append(pre_surname)
        if str(author['surname']) != 'nan':
            surname = author['surname']
            fullname.append(surname)

        names.append(' '.join(fullname))
        author['fullname'] = names

        authors = pd.concat([authors,author.to_frame().T])
                
    authors.to_csv(dest)

# def add_articles_to_dataset(articles_source ="../data/publications/orcid", files_source = None, dest="../exportable_dataset/List_of_articles"):
dest = ''

try:
    json_file = open("List_of_articles.SONaa", encoding="utf8")
    List_of_articles = json.load(json_file)
except:
    List_of_articles = []






articles_source = "../data/publications/orcid"





files = os.listdir(articles_source)

for file in files:
    # skip certain files
    if file in ['export_to_automated', 'export_to_manual', 'failed.csv']:
        continue
    
    # read file with articles
    uni_authors = pd.read_csv(articles_source+"/"+file)
    
    for i, row in tqdm(uni_authors.iterrows()):

        # if there is no doi, check titles
        
            # if yes, check author
            # if diferent, add new
        
        
        # if not exist, create one
        article = {'doi':row["link"],
             'title':row["title"],
             'date':row["date"],
             'journal':row["journal"],
             'authors':[row['name']]}

        List_of_articles.append(article)

with open('../exportable_dataset/List_of_articles.SONaa', 'w', encoding='utf-8') as f:
    json.dump(List_of_articles, f, ensure_ascii=False, indent=4)

# add_articles_to_dataset()
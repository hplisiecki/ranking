import pandas as pd
import os
import json
from tools_SONaa import *
from glob import glob

# to do
# add other information to authors_export

## this part is alternative to wrangle_scientists.py ##
def author_export(source = '../data/scientists.csv', dest = './exportable_dataset'):
    
    df = pd.read_csv(source)
    
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
        author['fullname'] = names[0]

        authors = pd.concat([authors,author.to_frame().T])
                
    authors.to_csv(dest+"/List_of_authors.csv", index=False)


# import orcid's article list
def import_orcid_article_list(source = "../data/publications/orcid", save_as_csv = False):

    files = os.listdir(source)
    df = pd.DataFrame()
    
    for file in files:
        # skip certain files
        if file in ['automated_doi', 'export_to_automated', 'export_to_manual', 'failed.csv']:
            continue
        
        # read file with articles
        uni_authors = pd.read_csv(source+"/"+file)
        
        df = pd.concat([df, uni_authors])

    Article_ID = []
    for i, row in (df.iterrows()):
        y = create_Article_ID(row)
        print(row['title'])
        Article_ID += [y]

    df.rename(columns = {'id':'filename', 'link':'doi'}, inplace = True)
    df['Article_ID'] = Article_ID

    if save_as_csv == True:
        df.to_csv('raw_article_list.csv')

        duplicated = df[df[['name', 'Article_ID']].duplicated(keep=False)]
        duplicated.to_csv('duplicates_import_orcid.csv', index=False)

    return(df)


def create_SONaa(raw_article_list = 'raw_article_list.csv', 
                 existing_SONaa = "exportable_dataset\List_of_articles.SONaa", 
                 save_duplicated_to_csv = False, 
                 dest = './exportable_dataset'):

    if isinstance(raw_article_list, str):
        raw_article_list = pd.read_csv(raw_article_list)

    try:
        SONaa = open_SONaa(existing_SONaa)
    except:
        SONaa = {}
        
        
    duplicated = []

    for i, row in raw_article_list.iterrows():
        if row['Article_ID'] in SONaa.keys():
            if row['name'] in SONaa[row['Article_ID']]['authors']:
                duplicated += [row]
            else:
                SONaa[row['Article_ID']]['authors'] += [row['name']]

        else:
            article = {
                'authors': [row["name"]],
                'title': row["title"],
                'doi': row["doi"],
                'date': row['date']}

            SONaa.update({row['Article_ID']: article})
    
    destination = dest + '/List_of_articles.SONaa'
    with open(destination, 'w', encoding='utf-8') as f:
        json.dump(SONaa, f, ensure_ascii=False, indent=4)
    # create DF with articles' properties
    if save_duplicated_to_csv:
        duplicated = pd.DataFrame(duplicated)
        duplicated.to_csv('duplicated_SONaa.csv', index=False)


def create_article_base(raw_article_list = 'raw_article_list.csv', 
                        existing_SONaa = "exportable_dataset\List_of_articles.SONaa", 
                        source_path = "S:/My Drive/ranking_instytutow/data_completion/articles/*/*/*.pdf", 
                        dest = 'temp_export', 
                        save_missing_to_csv = True):
    
    if isinstance(raw_article_list, str):
        raw_article_list = pd.read_csv(raw_article_list)
    
    SONaa = open_SONaa(existing_SONaa)
    
    # create list of existing files
    list_of_files = pd.DataFrame()
    temp_list = glob(source_path, recursive = True)
    list_of_files['path'] = temp_list
    list_of_files['file'] = [path.split('\\')[-1] for path in temp_list]

    missing_files = pd.DataFrame()
    
    # Find file for every article
    for Article_ID in SONaa.keys():
        article = raw_article_list[raw_article_list['Article_ID'] == Article_ID]
        
        for filename in article['filename']:
            if list_of_files['file'].str.contains(filename).any():
                break
            else:
                missing_files = pd.concat([missing_files, article])
            
    
    if save_missing_to_csv:
        missing_files = pd.DataFrame(missing_files)
        missing_files.to_csv('missing_files.csv', index=False)

    missing_n = len(missing_files['Article_ID'].unique())
    print(missing_n)


# import excluded from orcid
def import_excluded_from_orcid(save_missing_titles=True):
    source_path = '..\database_tests\problems\*_old_unpaired.csv'
    temp_list = glob(source_path, recursive = True)
    df = pd.DataFrame()

    for file in temp_list:
        
        # read file with articles
        uni_authors = pd.read_csv(file)
        
        df = pd.concat([df, uni_authors])
        
    title = []
    empty_titles = []
    for i, row in df.iterrows():
        if 'doi.org' in row['link']:
            title += ['empty']
            empty_titles += [row['link']]
            continue
        else:
            title += [row['link']]
            row['link'] = 'empty'
    
    df['titles'] = title
    if save_missing_titles:
        pd.DataFrame(empty_titles).to_csv('empty_titles.csv')
    
    return df
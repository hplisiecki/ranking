import pandas as pd

# to do
# add other information
# remove brackets from 'fullname'



## this part is alternative to wrangle_scientists.py ##

df = pd.read_csv('../data/scientists.csv')

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
    
authors.to_csv('../exportable_dataset/List_of_authors.csv')

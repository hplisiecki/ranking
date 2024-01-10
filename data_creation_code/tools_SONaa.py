import re


## Function and it's revers for make short version of DOI
def short_DOI(DOI, ID= True):
    """_summary_
    Args:
        DOI (string): string which is DOI in format both 'DOI:' and hyperlink.
        ID (bool, optional): True if shortened string should be returned in "ID format" with replaced characters. Defaults to True.
    """
    x = DOI.split("org/")[-1]
    if ID:
        x = x.replace('.', '_')
        x = x.replace('/', '&')
    return(x)

def long_DOI(DOI, hyperlink = True):
    """_summary_

    Args:
        DOI (_type_): short version of DOI or ID
        hyperlink (bool, optional): Should be added "https://doi.org/" before string?. Defaults to True.
    """
    x = DOI.replace('_', '.')
    x = x.replace('&', '/')
    if hyperlink:
        x = 'https://doi.org/' + x
    return(x)

# Create ID
def create_Article_ID(rowOrDOI, DOI = "doi", title = "title", joural = 'journal', date = 'date', old = False):
    if isinstance(rowOrDOI, str):
        return(short_DOI(rowOrDOI))       

    elif rowOrDOI[DOI] != "empty":
        return(short_DOI(rowOrDOI[DOI]))
    else:
        if old:
            t_old = rowOrDOI[title]+str(rowOrDOI[joural])
            return(hash(t_old))
        
        
        
        else:
            i = 0
            t_new = list('_'*40)
            
            # Tittle
            for t in rowOrDOI[title]:
                if i == 22: break
                t_new[i] = t
                i+=1
            
            i = 23
            
            # Journal
            for t in str(rowOrDOI[joural]):
                if i == 35: break
                t_new[i] = t
                i+=1
                
            
            i = 36
            # Date
            str_date = clean_date(rowOrDOI[date])
            for t in str_date:
                if i == 40: break
                t_new[i] = str(t)
                i+=1
            
            return ''.join(t_new)
  
def create_Auhor_ID(fullname):
    import random
    chars = ('abcdefghijklmnoprstuwxyz1234567890ABCDEFGHIJKLMNOPRSTUWXYZ')
    x = fullname.replace(" ", "_")
    y = "".join(random.sample(chars,3))
    return(x+"_"+y)


def open_SONaa(file):
    import json
    json_file = open(file, encoding="utf8")
    List_of_articles = json.load(json_file)
    return(List_of_articles)


# clean_date
def clean_date(date):
    if date == 'unrecovered': return(date)
    elif len(date) == 4: return(date)
    else:
        s = re.split('-|/',date)
    s = [item for item in s if len(item)==4]
    return(s[0])


def update_SONaa_Orcid(raw_article_list, 
                 existing_SONaa = "../main_dataset\List_of_articles.SONaa", 
                 save_duplicated_to_csv = False, 
                 dest = ''):


    import pandas as pd
    if isinstance(raw_article_list, str): 
        raw_article_list = pd.read_csv(raw_article_list)

    try:
        SONaa = open_SONaa(existing_SONaa)
    except:
        SONaa = {}
        print(existing_SONaa, ' not found, new file created')
        
        
    duplicated = []

    for i, row in tqdm(raw_article_list.iterrows()):
        if row['Article_ID'] in SONaa.keys():
            if (row["name"], row['author_id']) in SONaa[row['Article_ID']]['authors']:
                duplicated += [row]
            else:
                SONaa[row['Article_ID']]['authors'] += [row['author_id']]

        else:
            article = {
                'authors': [row['author_id']],
                'title': row["title"],
                'doi': row["doi"],
                'date': clean_date(row['date'])}

            SONaa.update({row['Article_ID']: article})
    
    destination = dest + 'List_of_articles.SONaa'
    import json
    with open(destination, 'w', encoding='utf-8') as f:
        json.dump(SONaa, f, ensure_ascii=False, indent=4)

    # create DF with articles' properties
    if save_duplicated_to_csv:
        duplicated = pd.DataFrame(duplicated)
        duplicated.to_csv('duplicated_SONaa.csv', index=False)
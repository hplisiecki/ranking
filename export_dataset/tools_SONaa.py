## Function and it's revers for make short version of DOI
def short_DOI(DOI):
    try:
        x = DOI.split("org/")[1]
        x = x.replace('.', '-')
        x = x.replace('/', '_')
        return(x)
    except:
        return("__hjuston, mamy problem"+DOI)

def long_DOI(DOI):
    x = DOI.replace('-', ',')
    x = DOI.replace('_', '/')
    x = 'https://doi.org/' + x
    return(x)




def create_identificator(row, DOI = "link", title = "title"):
    if row[DOI] != "empty":
        return(short_DOI(row[DOI]))
    else:
        t = row[title]
        l = len(t)
        if l>24:
            return(t[0:20])
        elif l==0:
            return("no title")
        else:
            return(t[0:l])
        

#read_SONaa
def read_SONaa():
    import pandas as pd
    import json

    json_file = open("List_of_articles.SONaa", encoding="utf8")
    List_of_articles = json.load(json_file)

    df = pd.DataFrame(List_of_articles)
    
    return(df)



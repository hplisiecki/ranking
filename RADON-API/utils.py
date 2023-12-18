import pandas as pd

def list_of_scientists():
    institutes = pd.read_csv('RADON-API/institutes_ev.csv')['uni_name'].to_list()
    scientists = pd.read_csv('RADON-API/List_of_authors.csv', index_col=False)

    SoIs = []
    
    for i, row in scientists.iterrows():
        if row['main_job'] in institutes:
            SoI = {
                'id':         row['id'],
                'firstName':  row['name'],
                'lastName':   row['surname'],
                'uni':        row['main_job']
            }
            SoIs.append(SoI)
            
    return SoIs
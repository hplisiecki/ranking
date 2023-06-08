import pandas as pd
import os

def split(file = None, data_dir = r'../data/publications/orcid', export_dir = r'../data/publications/orcid'):
    #get files' names
    if file == None:
        directories = os.listdir(data_dir)
    else:
        directories = [file]
        
    for file in directories:
        # skip certain files
        if file in ['export_to_automated', 'export_to_manual', 'failed.csv']:
            continue
        
        df = pd.read_csv(rf'../data/publications/orcid/{file}')
        id_list = []
        name = 'banana'
        
        # create ID's
        cnt = 1
        for fullname in df.name.values:
            fullname = fullname.replace(' ', '_')
            if fullname == name:
                cnt += 1
            else:
                cnt = 1
                name = fullname
            id = fullname + '_' + str(cnt)
            id_list.append(id)
        df['id'] = id_list
        
        
        # save
        export_to_automated = df[[True if 'http' in str(link) else False for link in df.link.values]]
        export_to_automated.to_csv(os.path.join(export_dir, rf'export_to_automated\{file}'), index=False)

        export_to_manual = df[[False if 'http' in str(link) else True for link in df.link.values]]
        new_names = file.replace('.csv', '_titles.xlsx')
        export_to_manual.to_excel(os.path.join(export_dir, rf'export_to_manual\{new_names}'), index=False)

split()
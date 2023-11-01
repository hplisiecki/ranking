import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import os

old_uni_list = ['Akademia_Ignatianum_w_Krakowie.csv', 'Instytut_Psychologii_Polskiej_Akademii_Nauk.csv',
          'Akademia_Pedagogiki_Specjalnej_Marii_Grzegorzewskiej_w_Warszawie.csv', 'Uniwersytet_Adama_Mickiewicza_w_Poznaniu.csv', 'Katolicki_Uniwersytet_Lubelski_Jana_Pawła_II_w_Lublinie.csv',
          'Uniwersytet_Gdański.csv', 'Uniwersytet_Jagielloński_w_Krakowie.csv', 'Uniwersytet_Jana_Kochanowskiego_w_Kielcach.csv', 'Uniwersytet_Kardynała_Stefana_Wyszyńskiego_w_Warszawie.csv',
          'Uniwersytet_Kazimierza_Wielkiego_w_Bydgoszczy.csv', 'Uniwersytet_Marii_Curie-Skłodowskiej_w_Lublinie.csv', 'Uniwersytet_Pedagogiczny_Komisji_Edukacji_Narodowej_w_Krakowie.csv',
          'Uniwersytet_Szczeciński.csv', 'Uniwersytet_Warszawski.csv', 'Uniwersytet_Wrocławski.csv', 'Uniwersytet_Łódzki.csv', 'Uniwersytet_Śląski_w_Katowicach.csv']

old_uni_list = ['Uniwersytet_Gdański.csv']


dir_new = r'..\data\publications\orcid'
dir_old = r'..\publication_links_old'

for uni in old_uni_list:
    file_new = pd.read_csv(os.path.join(dir_new, uni))
    file_old = pd.read_csv(os.path.join(dir_old, uni))
    file_compare = file_old    
    
    overwrite = pd.DataFrame()
    
    missing_records = pd.DataFrame()
    unpaired_record = pd.DataFrame()
    
    for i, row in file_new.iterrows():
        x = file_old[file_old['id'] == row['id']]
        if x.empty:
            missing_records = missing_records.append(row)
        else:
            x = x.squeeze()
            if row['link'] == 'empty':
                if row['title'] != x['link']:
                    unpaired_record = unpaired_record.append(row)
                    unpaired_record = unpaired_record.append(x)

            else:
                if row['link'] != x['link']:
                    y = file_compare[file_compare['link'] == row['link']]
                    z = y[y['name'] == row['name']]
                    z = z.squeeze()
                    if not z.empty and row['link'] == z['link']:
                        row['old_id'] = z['id']
                        overwrite = overwrite.append(row)
                    else:
                        unpaired_record = unpaired_record.append(row)
                        unpaired_record = unpaired_record.append(x)


            file_old = file_old[file_old['id'] != row['id']]

    # save file
    uni = uni.replace('.csv', '')
    
    if not file_old.empty:
        file_old.to_csv(rf'problems\{uni}_old_unpaired.csv')
    if not unpaired_record.empty:
        unpaired_record.to_csv(rf'problems\{uni}_wrong_paired.csv')
    if not missing_records.empty:
        missing_records.to_csv(rf'problems\{uni}_new_unpaired.csv')
    if not overwrite.empty:
        overwrite.to_csv(rf'problems\{uni}_overwrite.csv')
    
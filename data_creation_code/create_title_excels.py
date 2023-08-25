import pandas as pd
import os


for file in os.listdir(r'D:\data\ranking\publication_links\new'):
    if file in ['failed.csv', 'titles', 'other.csv']:
        continue
    links = pd.read_csv(rf'D:\data\ranking\publication_links\new\{file}')
    id_list = []
    name = 'banana'
    cnt = 1
    for fullname in links.name.values:
        fullname = fullname.replace(' ', '_')
        if fullname == name:
            cnt += 1
        else:
            cnt = 1
            name = fullname
        id = fullname + '_' + str(cnt)
        id_list.append(id)
    links['id'] = id_list
    # save
    links.to_csv(rf'D:\data\ranking\publication_links\new\{file}', index=False)

    titles = links[[False if 'http' in str(link) else True for link in links.link.values]]
    new_file = file.replace('.csv', '_titles.xlsx')
    titles.to_excel(rf'D:\data\ranking\publication_links\titles\{new_file}', index=False)


import os
import pandas as pd
import pickle

links_list = []
for file in os.listdir(r'D:\PycharmProjects\ranking\data\publications\orcid\export_to_automated'):
    if file in ['failed.csv', 'titles', 'other.csv', 'failed_swps.csv', 'SWPS_Uniwersytet_Humanistycznospołeczny_z_siedzibą_w_Warszawie.csv']:
        continue
    else:
        df = pd.read_csv(os.path.join(r'D:\PycharmProjects\ranking\data\publications\orcid\export_to_automated', file))
        links = df.link.values
        links_list.extend(links)

links_list = list(set(links_list))

# save
with open(r'D:\PycharmProjects\ranking\data\publications\orcid\automated_doi\all_links_without_swps.pkl', 'wb') as f:
    pickle.dump(links_list, f)



############# SWPS ################
import os
import pandas as pd
import pickle

df = pd.read_csv(r'D:\PycharmProjects\ranking\data\publications\orcid\export_to_automated\SWPS_Uniwersytet_Humanistycznospołeczny_z_siedzibą_w_Warszawie.csv')
links = list(df.link.values)

links_list = list(set(links))

# load
with open(r'D:\PycharmProjects\ranking\data\publications\orcid\automated_doi\all_links_without_swps.pkl', 'rb') as f:
    links_list_rest = pickle.load(f)

links_list = [link for link in links_list if link not in links_list_rest]


# save
with open(r'D:\PycharmProjects\ranking\data\publications\orcid\automated_doi\swps_links.pkl', 'wb') as f:
    pickle.dump(links_list, f)


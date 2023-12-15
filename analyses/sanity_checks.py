import os
from analyses.tools_SONaa import open_SONaa



dirs = [r'D:\data\ranking\pdfs\v1-1', r'D:\data\ranking\pdfs\v1-2', r'D:\data\ranking\pdfs\v1']


files = os.listdir(dirs[2])

sona = open_SONaa(r'D:\PycharmProjects\ranking\analyses\List_of_articles.SONaa')

sona[list(sona.keys())[0]]

years = [sona[link.replace('.pdf','')]['date'] for link in files]

years = [year.split('-')[0] for year in years]

# count values
from collections import Counter
Counter(years)
import time
import numpy as np
import pandas as pd


df = pd.read_csv('Przypisanie osobom kodu ORCID_WOS - Lista osób.csv')
df2 = pd.read_csv('./SWPS Uniwersytet Humanistycznospołeczny z siedzibą w Warszawie/names.csv')

df[~df['fullname'].isin(df2.fullname)].to_csv('kto_by_wyleciał.csv')
df2[~df2['fullname'].isin(df.fullname)].to_csv('kogo_brakuje_na_starej_liście.csv')
import pandas as pd
import os

dir = r'D:\data\ranking\pdfs\failed_pdf'


df_list = []
for file in os.listdir(dir):
    df = pd.read_csv(os.path.join(dir, file))
    df_list.append(df)

df = pd.concat(df_list)


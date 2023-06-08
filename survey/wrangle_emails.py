import numpy as np
import pandas as pd
import os

emailList = pd.DataFrame(columns=['fullname', 'institution', 'email1', 'email2'])

for institution in os.walk('../anonymized/data'):
    for file in institution[2]:
        if file == 'names.xlsx':
            dir = os.path.join(institution[0], file)
            institutionName = os.path.basename(institution[0])
            
            df = pd.read_excel(dir)[['fullname', 'Email 1.', 'Email. 2']]

            df.insert(1, 'institution', str(institutionName))

            df.columns = ['fullname', 'institution', 'email1', 'email2']

            df = df.dropna(subset = ['email1'])
            
            emailList = pd.concat([emailList, df])

emailList.reset_index
emailList.to_csv('../anonymized/survey/emailList.csv')
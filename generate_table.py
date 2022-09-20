from tinydb import TinyDB, Query
from pprint import pprint
db = TinyDB('processos.db')
import pandas as pd 

df = pd.read_csv('19_09.csv')
print(df.head())
df['ANDAMENTO'] = ''
print(df.columns)
for item in db:
    if item['PROCCESS_NUMBER'] != '':
        df.loc[df['PROCESSO'] == item['PROCCESS_NUMBER'], 'ANDAMENTO'] = item['LAST_ACTION']

print(df.head(25))
df.to_csv('updated_19.csv')
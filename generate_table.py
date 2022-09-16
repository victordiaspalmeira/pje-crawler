from tinydb import TinyDB, Query
from pprint import pprint
db = TinyDB('processos.db')
import pandas as pd 

df = pd.read_csv('ELEIÇÕES 2022 - ANDAMENTO PROCESSUAL  - 15.09.2022.csv')
df['ANDAMENTO'] = ''
print(df.columns)
for item in db:
    if item['proccess_number'] != '':
        df.loc[df['PROCESSO'] == item['proccess_number'], 'ANDAMENTO'] = item['fase_atual']

print(df.head(25))
df.to_csv('updated.csv')
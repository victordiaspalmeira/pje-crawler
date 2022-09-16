from tinydb import TinyDB, Query
from pprint import pprint
db = TinyDB('processos.db')

for item in db:
    if item['proccess_number'] != '':
        pprint(item)
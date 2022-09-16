from pprint import pprint
from tinydb import TinyDB, Query

db = TinyDB('processos.db')
print(len(db))
for item in db:
    pprint(item['proccess_number'])
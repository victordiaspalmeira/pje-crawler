import pickle 
from tinydb import TinyDB, Query

def init_query_list():
    db = TinyDB('processos.db')
    with open('keys.txt') as f:
        keys = f.read().splitlines()
        keys = list(dict.fromkeys(keys))

    with open('blacklist.txt') as f1:
        blacklist_keys = f1.read().splitlines()
        blacklist_keys = list(dict.fromkeys(blacklist_keys))   

    for key in blacklist_keys:
        keys.remove(key)

    for item in db:
        if item['proccess_number'] in keys:
            keys.remove(item['proccess_number'])

    print(len(keys))

    file = open('keys_list.p', 'wb')
    pickle.dump(keys, file)
    file.close()
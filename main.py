from pje_processos import get_data_from_proccess_number
import time
import re 

import sqlite3

pattern = r'[^A-Za-z0-9]+'
base_time = 5.0

def insert_into_table(data):
    conn = sqlite3.connect('processos.db')
    sql = """
        INSERT INTO Processos(
            n_processo,
            orgao_justica,
            origem,
            relator,
            data_autuacao,
            data_ultimo_movimento,
            classe_judicial,
            assunto_principal,
            ano_eleicao,
            data_acesso
        )
        VALUES(?,?,?,?,?,?,?,?,?,?);
    """

    c = conn.cursor()
    c.execute(sql, data)
    conn.commit()
    conn.close()

def create_db():
    conn = sqlite3.connect('processos.db')
    sql = """
        CREATE TABLE IF NOT EXISTS Processos(
            n_processo TEXT,
            fase_atual TEXT,
            orgao_justica TEXT,
            origem TEXT,
            relator TEXT,
            data_autuacao TEXT,
            data_ultimo_movimento TEXT,
            classe_judicial TEXT,
            assunto_principal TEXT,
            ano_eleicao TEXT,
            data_acesso TEXT
        )
    """
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()

create_db()

if __name__ == "__main__":
    #init database
    conn = sqlite3.connect('processos.db')
    
    #carrega todas as chaves de busca
    with open('keys.txt') as f:
        keys = f.read().splitlines()

    for key in keys:
        try:
            filtered_key = re.sub(pattern, '', key)
            output = get_data_from_proccess_number(filtered_key)

        except Exception as e:
            print('erro ao coletar dados:', e)
            time.sleep(200)
        
import sqlite3 as lite

con = lite.connect('banco_dados.db')
cursor = con.cursor()


def criar_tabela():
    with con:
        try:
            cursor.execute("""
                CREATE TABLE produtos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marca TEXT,
                modelo TEXT,
                valor FLOAT)
            """)
            print('Tabela criada com sucesso.')
        except:
            print('Não foi possível criar a tabela.')


def inserir_dados():
    with con:
        marca = str(input('Nome: ')).strip().lower()
        modelo = str(input('Usuário: ')).strip().lower()
        valor = float(input('Senha: ')).strip().lower()
        try:
            cursor.execute(f"""
                INSERT INTO produtos(marca, modelo, valor)
                VALUES('{marca}', '{modelo}', '{valor}') 
            """)
            print('Dados inseridos com sucesso.')
        except:
            print('Não foi possível inserir os dados.')


def atualizar_dados():
    with con:
        id = int(input('Id: '))
        marca = str(input('Marca: ')).strip().lower()
        modelo = str(input('Modelo: ')).strip().lower()
        valor = str(input('Valor: ')).strip().lower()
        try:
            cursor.execute(f"""
                UPDATE produtos SET marca='{marca}', modelo='{modelo}', valor='{valor}' WHERE id={id}
            """)
            print('Dados atualizados com sucesso.')
        except:
            print('Não foi possível atualizar os dados.')


def consultar_dados():
    with con:
        print('\n*** PARA PESQUISAR, DIGITE O NOME DO MODELO DO CELULAR ***')
        modelo = str(input('Digite parte do nome do modelo para pesquisar: ')).strip().lower()
        try:
            cursor.execute(f"""
                SELECT * FROM produtos WHERE nome LIKE '%{modelo}%'
            """)
            res = cursor.fetchall()
            for item in res:
                print(item)
        except:
            print('Não foi possível localizar o cadastro.')


def deletar_dados():
    with con:
        print('*** DIGITE O ID QUE DESEJA EXCLUIR ***')
        id = int(input('Id: '))
        try:
            cursor.execute(f"""
                DELETE FROM produtos WHERE id='{id}'
            """)
            print('O cadastro foi excluído com sucesso.')
        except:
            print('Não foi possível excluir os dados.')

"""
Desenvolvedor: Marley Paranhos
Software: Sistema tabela de preços de telas de celular, consulta por modelo do celular
Versão: 1.0
Layout: Custom Tkinter
"""

from tkinter import ttk, messagebox
from customtkinter import *
import sqlite3 as lite

conn = lite.connect('banco_dados.db')
cursor = conn.cursor()

global treev


##### Funções
# Função mostrar dados no treeview
def mostrar_dados():
    with conn:
        try:
            lista = []
            cursor.execute("""
                SELECT * FROM produtos
            """)
            res = cursor.fetchall()
            for item in res:
                lista.append(item)
            return lista
        except:
            print('Erro ao mostrar os dados.')


# Função cadastrar
def cadastrar_dados():
    global treev
    with conn:
        try:
            if entry_marca.get() == '' or entry_modelo.get() == '' or entry_valor.get() == '':
                messagebox.showinfo('Atenção!', 'Os campos [marca, modelo e valor] não podem ser vazio')
                return
            else:
                marca = entry_marca.get().strip().upper()
                modelo = entry_modelo.get().strip().upper()
                valor = entry_valor.get().strip()
                valor_tratado = valor.replace(',', '.')

                cursor.execute(f"""
                    INSERT INTO produtos(marca, modelo, valor)
                    VALUES('{marca}', '{modelo}', {valor_tratado}) 
                """)

                messagebox.showinfo('Sucesso!', 'Cadastro realizado com sucesso')

                # Limpando as entry
                entry_marca.delete(0, END)
                entry_modelo.delete(0, END)
                entry_valor.delete(0, END)
                entry_marca.focus()
        except:
            messagebox.showerror('Erro!', 'Não foi possível cadastrar os dados')

        mostrar_tabela()


# Função atualizar
def atualizar_dados():
    global treev
    try:
        marca = entry_marca.get().strip().upper()
        modelo = entry_modelo.get().strip().upper()
        valor = entry_valor.get().strip()

        treev_dados = treev.focus()
        treev_dicionario = treev.item(treev_dados)
        treev_lista = treev_dicionario['values']

        # Limpando as entry
        entry_marca.delete(0, END)
        entry_modelo.delete(0, END)
        entry_valor.delete(0, END)

        # Inserindo os dados nas entry
        id = int(treev_lista[0])
        entry_marca.insert(0, treev_lista[1])
        entry_modelo.insert(0, treev_lista[2])
        entry_valor.insert(0, treev_lista[3])
    except:
        messagebox.showerror('Erro!', 'Selecione um cadastro para atualizar')
        return

    # Função salvar dados após atualizar
    def salvar_dados():
        with conn:
            try:
                if entry_marca.get() == '' or entry_modelo.get() == '' or entry_valor.get() == '':
                    messagebox.showinfo('Atenção!', 'Preencha todos os campos')
                    return

                marca = entry_marca.get().strip().upper()
                modelo = entry_modelo.get().strip().upper()
                valor = entry_valor.get().strip()
                valor_tratado = valor.replace(',', '.')

                treev_dados = treev.focus()
                treev_dicionario = treev.item(treev_dados)
                treev_lista = treev_dicionario['values']

                id = int(treev_lista[0])

                cursor.execute(f"""
                                    UPDATE produtos SET marca='{marca}', modelo='{modelo}', valor={valor_tratado} WHERE id={id}
                                """)

                # Limpando as entry
                entry_marca.delete(0, END)
                entry_modelo.delete(0, END)
                entry_valor.delete(0, END)

                messagebox.showinfo('Sucesso!', 'Cadastro atualizado com sucesso!')
            except:
                messagebox.showerror('Erro!', 'Não foi possível atualizar o cadastro')

        button_salvar.destroy()

        mostrar_tabela()

    button_salvar = CTkButton(frame_cima, text='Salvar', command=salvar_dados, width=90, corner_radius=10,
                              fg_color=('red', 'blue'))
    button_salvar.place(x=310, y=180)


# Função deletar
def deletar_dados():
    global treev
    with conn:
        try:
            treev_dados = treev.focus()
            treev_dicionario = treev.item(treev_dados)
            treev_lista = treev_dicionario['values']
            id = treev_lista[0]

            cursor.execute(f"""
                            DELETE FROM produtos WHERE id='{id}'
                        """)
            messagebox.showinfo('Sucesso!', 'Cadastro deletado com sucesso')
        except:
            messagebox.showerror('Erro!', 'Selecione um cadastro para deletar')

        mostrar_tabela()


# Função pesquisar
def pesquisar_dados():
    global treev
    with conn:
        try:
            treev.delete(*treev.get_children())
            cursor.execute(f"""
                            SELECT * FROM produtos WHERE modelo LIKE '%{entry_pesquisar.get()}%'
                        """)
            res = cursor.fetchall()
            for item in res:
                treev.insert('', 'end', values=item)
        except:
            messagebox.showerror('Erro!', 'Não foi possível localizar o cadastro')


app = CTk()
app.title('Sistema Tabela de Preços - MagnoTech - v1.0')
app.geometry('900x510')
app.resizable(width=False, height=False)

# Janela maximizada
# app.state('zoomed')

# Estilo da janela
style = ttk.Style()
style.theme_use('clam')

##### Frames
# Frame cima
frame_cima = CTkFrame(app, width=900, height=250)
frame_cima.grid(row=0, column=0)

# Frame baixo
frame_baixo = CTkFrame(app, width=900, height=300)
frame_baixo.grid(row=1, column=0)

# Label cadastro
label_cadastro = CTkLabel(frame_cima, text='Cadastro de Produtos e Preços', text_color='blue')
label_cadastro.place(x=10, y=10)

# Label e Entry
label_marca = ttk.Label(frame_cima, text='Marca do Celular', font='ivy 11')
label_marca.place(x=10, y=50)
entry_marca = CTkEntry(frame_cima, width=180, height=10, placeholder_text='Digite a marca do celular')
entry_marca.place(x=10, y=75)

label_modelo = ttk.Label(frame_cima, text='Modelo do Celular', font='ivy 11')
label_modelo.place(x=210, y=50)
entry_modelo = CTkEntry(frame_cima, width=180, height=10, placeholder_text='Digite o modelo do celular')
entry_modelo.place(x=210, y=75)

label_valor = ttk.Label(frame_cima, text='Valor da Tela', font='ivy 11')
label_valor.place(x=410, y=50)
entry_valor = CTkEntry(frame_cima, width=180, height=10, placeholder_text='Digite o valor do produto')
entry_valor.place(x=410, y=75)

label_pesquisar = ttk.Label(frame_cima, text='Pesquisa pelo modelo do celular', font='ivy 11')
label_pesquisar.place(x=610, y=110)
entry_pesquisar = CTkEntry(frame_cima, width=180, height=10, placeholder_text='Digite o modelo do celular')
entry_pesquisar.place(x=610, y=135)

# Botões
button_cadastrar = CTkButton(frame_cima, text='Cadastrar', command=cadastrar_dados, width=90, corner_radius=10)
button_cadastrar.place(x=10, y=180)

button_atualizar = CTkButton(frame_cima, text='Atualizar', command=atualizar_dados, width=90, corner_radius=10)
button_atualizar.place(x=110, y=180)

button_deletar = CTkButton(frame_cima, text='Deletar', command=deletar_dados, width=90, corner_radius=10)
button_deletar.place(x=210, y=180)

button_pesquisar = CTkButton(frame_cima, text='Pesquisar', command=pesquisar_dados, width=90, corner_radius=10)
button_pesquisar.place(x=650, y=180)

# Label tabela
label_tabela = ttk.Label(frame_baixo, text='Tabela de usuários', font='ivy 9 bold', foreground='#008080')
# label_tabela.grid(row=0, column=0)
label_tabela.place(x=10, y=10)


# Função mostrar tabela
def mostrar_tabela():
    global treev
    # Criando TreeView
    lista_cabecalho = ['ID', 'MARCA DO CELULAR', 'MODELO DO CELULAR', 'VALOR DA TELA']

    treev = ttk.Treeview(frame_baixo, selectmode='extended', columns=lista_cabecalho, show='headings')

    # Posicionamento dos scrollbar
    vertical_scroll = ttk.Scrollbar(frame_baixo, orient='vertical', command=treev.yview())
    vertical_scroll.grid(row=1, column=1, sticky='ns')
    horizontal_scroll = ttk.Scrollbar(frame_baixo, orient='horizontal', command=treev.xview())
    horizontal_scroll.grid(row=2, column=0, sticky='ew')
    treev.configure(yscrollcommand=vertical_scroll, xscrollcommand=horizontal_scroll)
    treev.grid(row=1, column=0, columnspan=1, pady=5)
    frame_baixo.grid_rowconfigure(0, weight=12)

    # Inserir títulos no cabeçalho da tabela
    hd = ['nw', 'nw', 'nw', 'e']
    h = [50, 350, 300, 150]
    n = 0

    # Inserir os nomes no cabeçalho da tabela
    for coluna in lista_cabecalho:
        treev.heading(coluna, text=coluna.title(), anchor=CENTER)
        treev.column(coluna, width=h[n], anchor=hd[n])
        n += 1

    # Lista com os dados do banco de dados
    lista = mostrar_dados()

    # Inserir os dados na tabela
    for item in lista:
        # valor_formatado = "{:,.2f}".format(item).replace(".", ",")
        treev.insert('', 'end', values=item)


mostrar_tabela()

app.mainloop()

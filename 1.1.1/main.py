"""
Desenvolvedor: Marley Paranhos.
Software: Cadastro de produtos.
Versão: 1.1.1 - O programa passa a ser Cadastro de Produtos.
Automação de tarefas, adicionado a função backup do banco de dados.
Sempre que rodar o programa, será feita uma cópia de segurança do banco de dados em um diretório diferente.
A janela passa de 900x510 para maximizada.
Acrescentado o campo quantidade de produtos.
No campo de pesquisa o processo é automatizado por filtragem autocomplete, a medida que o usuário digita, é exibido
o resultado da pesquisa.
Os valores estão com duas casas decimais e separados por vírgula.
Teclas de atalho: no formulário, o usuário tem a opção de navegar nos registros com as teclas de atalho Ctrl+End para selecionar o último registro,
Ctrl+Home para o primeiro registro e PageDown e PageUp para paginação.
"""

import os.path
import shutil
from tkinter import ttk, messagebox, Tk, Label
from PIL import Image, ImageTk
from customtkinter import *
import sqlite3 as lite

conn = lite.connect('banco_dados.db')
cursor = conn.cursor()

global treev


# Funções
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
        except Exception as e:
            print(f'Erro ao mostrar os dados: {str(e)}')


# Função cadastrar
def cadastrar_dados():
    global treev
    with conn:
        try:
            if entry_marca.get() == '' or entry_modelo.get() == '' or entry_valor.get() == '' or entry_quantidade.get() == '':
                messagebox.showinfo('Atenção!',
                                    'Se você não preencher os campos\n[nome, modelo, valor e quantidade do produto]\n'
                                    'não será possível realizar o cadastro!\n'
                                    'Volta lá e faz bonito.')
                return
            else:
                marca = entry_marca.get().strip().upper()
                modelo = entry_modelo.get().strip().upper()
                valor = entry_valor.get().strip()
                valor_formatado = float(valor.replace(',', '.'))
                quantidade = entry_quantidade.get().strip()

                cursor.execute(f"""
                    INSERT INTO produtos(marca, modelo, valor, quantidade)
                    VALUES('{marca}', '{modelo}', '{valor_formatado:.2f}', '{quantidade}') 
                """)

                messagebox.showinfo('Sucesso!', 'Cadastro realizado com sucesso')

                # Limpando as entry
                entry_marca.delete(0, END)
                entry_modelo.delete(0, END)
                entry_valor.delete(0, END)
                entry_quantidade.delete(0, END)
                entry_marca.focus()
        except Exception:
            messagebox.showerror('Erro!', 'Não foi possível cadastrar os dados')

        mostrar_tabela()


# Função atualizar
def atualizar_dados():
    global treev
    try:
        entry_marca.get().strip().upper()
        entry_modelo.get().strip().upper()
        entry_valor.get().strip()
        entry_quantidade.get().strip()

        treev_dados = treev.focus()
        treev_dicionario = treev.item(treev_dados)
        treev_lista = treev_dicionario['values']

        # Limpando as entry
        entry_marca.delete(0, END)
        entry_modelo.delete(0, END)
        entry_valor.delete(0, END)
        entry_quantidade.delete(0, END)

        # Inserindo os dados nas entry
        id = int(treev_lista[0])
        entry_marca.insert(0, treev_lista[1])
        entry_modelo.insert(0, treev_lista[2])
        entry_valor.insert(0, treev_lista[3])
        entry_quantidade.insert(0, treev_lista[4])
    except Exception:
        messagebox.showerror('Erro!', 'Selecione um cadastro para atualizar')
        return

    # Função salvar dados após atualizar
    def salvar_dados():
        with conn:
            try:
                if entry_marca.get() == '' or entry_modelo.get() == '' or entry_valor.get() == '' or entry_quantidade.get() == '':
                    messagebox.showinfo('Atenção!',
                                        'Se você não preencher os campos\n[nome, modelo, valor e quantidade do produto]\n'
                                        'não será possível atualizar!\n'
                                        'Volta lá e faz bonito.')
                    return

                marca = entry_marca.get().strip().upper()
                modelo = entry_modelo.get().strip().upper()
                valor = entry_valor.get().strip()
                valor_tratado = float(valor.replace(',', '.'))
                quantidade = entry_quantidade.get().strip()

                treev_dados = treev.focus()
                treev_dicionario = treev.item(treev_dados)
                treev_lista = treev_dicionario['values']

                id = int(treev_lista[0])

                cursor.execute(f"""
                                    UPDATE produtos SET marca='{marca}', modelo='{modelo}', valor='{valor_tratado:.2f}',
                                    quantidade='{quantidade}' WHERE id={id}
                                """)

                # Limpando as entry
                entry_marca.delete(0, END)
                entry_modelo.delete(0, END)
                entry_valor.delete(0, END)
                entry_quantidade.delete(0, END)

                messagebox.showinfo('Sucesso!', 'Cadastro atualizado com sucesso!')
            except Exception as e:
                print(f'{e}')
                messagebox.showerror('Erro!', f'Não foi possível atualizar o cadastro: {e}')

        button_salvar.destroy()

        mostrar_tabela()

    button_salvar = CTkButton(frame_cima, text='Salvar', command=salvar_dados, width=90, corner_radius=10, height=100,
                              text_color='white', font=('ivy', 15, 'bold'))
    button_salvar.place(x=340, y=140)


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
        except Exception:
            messagebox.showerror('Erro!', 'Selecione um cadastro para deletar')

        mostrar_tabela()


# Função pesquisar
def pesquisar_dados(event):
    global treev
    with conn:
        try:
            lista = []
            treev.delete(*treev.get_children())
            cursor.execute(f"""
                            SELECT * FROM produtos WHERE modelo LIKE '%{entry_pesquisar.get()}%'
                        """)
            res = cursor.fetchall()
            for item in res:
                valor = float(item[3])
                valor_formatado = f'{valor:.2f}'
                valor_tratado = valor_formatado.replace('.', ',')
                treev.insert('', 'end', values=(item[0], item[1], item[2], valor_tratado, item[4]))
                lista.append(item)
        except Exception:
            messagebox.showerror('Erro!', 'Não foi possível localizar o cadastro')


# Função backup do banco de dados
def salvar_banco():
    diretorio = 'C:\\backup_banco_dados'
    os.path.join('diretorio', 'banco_dados.db')
    shutil.copy('banco_dados.db', diretorio)


# função ctrl+end
def ctrl_end(event):
    global treev
    ultimo_item = treev.get_children()[-1]
    treev.selection_set(ultimo_item)
    treev.focus(ultimo_item)
    treev.see(ultimo_item)


# função ctrl+home
def ctrl_home(event):
    global treev
    primeiro_item = treev.get_children()[0]
    treev.selection_set(primeiro_item)
    treev.focus(primeiro_item)
    treev.see(primeiro_item)


# Chamando a função salvar_banco
salvar_banco()

app = Tk()
app.title('Sistema de Cadastro - MagnoTech - v1.1.1')

# adicionando ícone na janela
app.iconbitmap('celular_ico.ico')

# Janela maximizada
app.state('zoomed')

# Estilo da janela
style = ttk.Style()
style.theme_use('clam')

# Frames
# Frame cima
frame_cima = CTkFrame(app, width=1400, height=350)
frame_cima.grid(row=0, column=0)

# Frame baixo
frame_baixo = CTkFrame(app, height=1000)
frame_baixo.grid(row=1, column=0)

# label da logo
imagem = Image.open('logo.png')
imagem = imagem.resize((250, 150))
foto = ImageTk.PhotoImage(imagem)

label_imagem = Label(frame_cima, image=foto, bg='#d9d9d9')
label_imagem.place(x=1000, y=30)

label_tecla_atalho = Label(frame_cima, text='Teclas de Atalho:\n\nCtrl+Home: Seleciona o primeiro registro\n'
                                            'Ctrl+End: Seleciona o último registro', justify='left', font='ivy 10', bg='#d9d9d9')
label_tecla_atalho.place(x=1000, y=235)

# Label cadastro
label_cadastro = CTkLabel(frame_cima, text='Cadastro de Produtos', text_color='blue')
label_cadastro.place(x=10, y=10)

# Label e Entry
label_marca = ttk.Label(frame_cima, text='Nome do produto', font='ivy 11')
label_marca.place(x=10, y=50)
entry_marca = CTkEntry(frame_cima, width=180, height=10, placeholder_text='Digite o nome do produto')
entry_marca.place(x=10, y=75)

label_modelo = ttk.Label(frame_cima, text='Modelo do produto', font='ivy 11')
label_modelo.place(x=210, y=50)
entry_modelo = CTkEntry(frame_cima, width=180, height=10, placeholder_text='Digite o modelo do produto')
entry_modelo.place(x=210, y=75)

label_valor = ttk.Label(frame_cima, text='Valor do produto', font='ivy 11')
label_valor.place(x=410, y=50)
entry_valor = CTkEntry(frame_cima, width=180, height=10, placeholder_text='Digite o valor do produto')
entry_valor.place(x=410, y=75)

label_quantidade = ttk.Label(frame_cima, text='Quantidade do produto', font='ivy, 11')
label_quantidade.place(x=610, y=50)
entry_quantidade = CTkEntry(frame_cima, width=90, height=10, placeholder_text='Quantidade')
entry_quantidade.place(x=610, y=75)

label_pesquisa = CTkLabel(frame_cima, text='Campo de Busca', text_color='blue')
label_pesquisa.place(x=680, y=170)
label_pesquisar = ttk.Label(frame_cima, text='Pesquisa pelo modelo do produto', font='ivy 11')
label_pesquisar.place(x=680, y=210)
entry_pesquisar = CTkEntry(frame_cima, width=180, height=10, placeholder_text='Digite o modelo do produto')
entry_pesquisar.place(x=680, y=235)

# vincula o evento de autocomplementar a medida que o usuário digita no widget entry_pesquisar para iniciar a pesquisa
entry_pesquisar.bind('<KeyRelease>', pesquisar_dados)

# Botões
button_cadastrar = CTkButton(frame_cima, text='Cadastrar', command=cadastrar_dados, width=90,
                             corner_radius=10, height=100, text_color='white', font=('ivy', 15, 'bold'))
button_cadastrar.place(x=10, y=140)

button_atualizar = CTkButton(frame_cima, text='Atualizar', command=atualizar_dados, width=90,
                             corner_radius=10, height=100, text_color='white', font=('ivy', 15, 'bold'))
button_atualizar.place(x=120, y=140)

button_deletar = CTkButton(frame_cima, text='Deletar', command=deletar_dados, width=90,
                           corner_radius=10, height=100, text_color='white', font=('ivy', 15, 'bold'))
button_deletar.place(x=230, y=140)

button_pesquisar = CTkButton(frame_cima, text='Pesquisar', command=lambda: pesquisar_dados(event='<KeyRelease>'),
                             width=90, height=40,
                             corner_radius=10, text_color='white', font=('ivy', 12, 'bold'))
button_pesquisar.place(x=710, y=280)

# Label tabela
label_tabela = ttk.Label(frame_baixo, text='Tabela de usuários', font='ivy 9 bold', foreground='#008080')
# label_tabela.grid(row=0, column=0)
label_tabela.place(x=10, y=10)


# Função mostrar tabela
def mostrar_tabela():
    global treev
    # Criando TreeView
    lista_cabecalho = ['ID', 'PRODUTO', 'MODELO', 'VALOR', 'QUANTIDADE']

    treev = ttk.Treeview(frame_baixo, selectmode='extended', columns=lista_cabecalho, show='headings', height=12)

    # Posicionamento dos scrollbar
    vertical_scroll = ttk.Scrollbar(frame_baixo, orient='vertical', command=treev.yview())
    vertical_scroll.grid(row=1, column=1, sticky='ns')
    horizontal_scroll = ttk.Scrollbar(frame_baixo, orient='horizontal', command=treev.xview())
    horizontal_scroll.grid(row=2, column=0, sticky='ew')
    treev.configure(yscrollcommand=vertical_scroll, xscrollcommand=horizontal_scroll)
    treev.grid(row=1, column=0, columnspan=1, pady=5, padx=5, ipady=10)
    frame_baixo.grid_rowconfigure(0, weight=12)

    # Inserir títulos no cabeçalho da tabela
    hd = ['ce', 'ce', 'w', 'ce', 'ce']
    h = [100, 450, 450, 100, 100]
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

        valor = float(item[3])
        valor_formatado = f'{valor:.2f}'
        valor_tratado = valor_formatado.replace('.', ',')
        treev.insert('', 'end', values=(item[0], item[1], item[2], valor_tratado, item[4]))

    treev.bind('<Control-End>', ctrl_end)
    treev.bind('<Control-Home>', ctrl_home)


mostrar_tabela()

app.mainloop()

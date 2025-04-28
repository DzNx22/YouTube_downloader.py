import yt_dlp
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import PhotoImage
import threading
import time

# Lista para armazenar os links
links = []
pasta_destino = ""

def adicionar_link():
    link = link_entry.get().strip()
    if not link:
        exibir_mensagem("Por favor, insira a URL do vídeo.", "erro")
        return
    if len(links) >= 10:
        exibir_mensagem("Limite de 10 links atingido.", "erro")
        return
    links.append(link)
    link_entry.delete(0, tk.END)
    atualizar_lista()
    exibir_mensagem("Link adicionado com sucesso!", "sucesso")

def atualizar_lista():
    lista_links.delete(0, tk.END)
    for idx, link in enumerate(links, start=1):
        lista_links.insert(tk.END, f"{idx}. {link}")

def escolher_destino():
    global pasta_destino
    pasta_destino = filedialog.askdirectory(title="Escolha a pasta de destino")
    if pasta_destino:
        exibir_mensagem(f"Pasta de destino definida para: {pasta_destino}", "sucesso")
    else:
        exibir_mensagem("Pasta de destino não selecionada", "erro")

def baixar_todos():
    if not links:
        messagebox.showerror("Erro", "Nenhum link adicionado.")
        return

    if not pasta_destino:
        messagebox.showerror("Erro", "Por favor, escolha uma pasta de destino.")
        return

    for link in links:
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': f'{pasta_destino}/%(title)s.%(ext)s',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao baixar: {link}\n{e}")
            return

    messagebox.showinfo("Sucesso", "Todos os downloads foram concluídos!")
    links.clear()
    atualizar_lista()

def excluir_link():
    selecionado = lista_links.curselection()
    if not selecionado:
        exibir_mensagem("Selecione um link para excluir.", "erro")
        return
    indice = selecionado[0]
    del links[indice]
    atualizar_lista()
    exibir_mensagem("Link removido!", "sucesso")

def exibir_mensagem(texto, tipo):
    aviso.config(text=texto)
    if tipo == "sucesso":
        aviso.config(fg="green")
    else:
        aviso.config(fg="red")
    # Criar uma thread para apagar a mensagem depois de 3 segundos
    threading.Thread(target=limpar_mensagem, daemon=True).start()

def limpar_mensagem():
    time.sleep(3)
    aviso.config(text="")

# Cria a janela principal
app = tk.Tk()
app.title("Downloader de Vídeos do YouTube")
app.geometry("550x500")

# Texto de instrução
label = tk.Label(app, text="Insira a URL do vídeo do YouTube:")
label.pack(pady=10)

# Campo de entrada
link_entry = tk.Entry(app, width=60)
link_entry.pack(pady=5)

# Botão para adicionar link
add_button = tk.Button(app, text="Adicionar Link", command=adicionar_link)
add_button.pack(pady=5)

# Aviso para mensagens rápidas
aviso = tk.Label(app, text="", font=("Arial", 10))
aviso.pack()

# Lista de links adicionados
lista_links = tk.Listbox(app, width=75, height=10)
lista_links.pack(pady=10)

# Botões de excluir e baixar
frame_botoes = tk.Frame(app)
frame_botoes.pack(pady=10)

# Ícone de lixeira
try:
    trash_img = PhotoImage(file="trash.png")  # Você precisa ter uma imagem chamada "trash.png" na mesma pasta
    delete_button = tk.Button(frame_botoes, image=trash_img, command=excluir_link)
    delete_button.image = trash_img  # Para não perder referência
except:
    delete_button = tk.Button(frame_botoes, text="Excluir Link", command=excluir_link)

delete_button.grid(row=0, column=0, padx=10)

# Botão de baixar todos
download_all_button = tk.Button(frame_botoes, text="Baixar Todos", command=baixar_todos)
download_all_button.grid(row=0, column=1, padx=10)

# Botão para escolher a pasta de destino
choose_folder_button = tk.Button(app, text="Escolher Pasta de Destino", command=escolher_destino)
choose_folder_button.pack(pady=10)

# Rodar a aplicação
app.mainloop()

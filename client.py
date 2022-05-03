import tkinter as tk
from tkinter import messagebox
import socket
import threading

client = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080

window = tk.Tk()
window.title("Client")
username = " "
porta = " "

topFrame = tk.Frame(window)
lblName = tk.Label(topFrame, text = "Name:").pack(side=tk.LEFT)
entName = tk.Entry(topFrame)
entName.pack(side=tk.LEFT)

lblPort = tk.Label(topFrame, text = "Porta:").pack(side=tk.LEFT)
entPort = tk.Entry(topFrame)
entPort.pack(side=tk.LEFT)

btnConnect = tk.Button(topFrame, text="Connect", command=lambda : connect())
btnConnect.pack(side=tk.LEFT)

topFrame.pack(side=tk.TOP)

displayFrame = tk.Frame(window)
lblLine = tk.Label(displayFrame, text="---------------------------------------------------------------------").pack()
scrollBar = tk.Scrollbar(displayFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(displayFrame, height=20, width=55)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
tkDisplay.tag_config("tag_your_message", foreground="blue")
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F5F5F5", highlightbackground="grey", state="disabled")
displayFrame.pack(side=tk.TOP)

bottomFrame = tk.Frame(window)
tkMessage = tk.Text(bottomFrame, height=2, width=55)
tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
tkMessage.config(highlightbackground="grey", state="disabled")
tkMessage.bind("<Return>", (lambda event: getChatMessage(tkMessage.get("1.0", tk.END))))

bottomFrame.pack(side=tk.BOTTOM)

def receive_message_from_server(sck, m):
    while True:
        from_server = sck.recv(4096).decode()

        if not from_server:
            break

        texts = tkDisplay.get("1.0", tk.END).strip()
        tkDisplay.config(state=tk.NORMAL)

        if len(texts) < 1:
            tkDisplay.insert(tk.END, from_server)
        else:
            tkDisplay.insert(tk.END, "\n\n"+ from_server)

        tkDisplay.config(state=tk.DISABLED)
        tkDisplay.see(tk.END)

    sck.close()
    window.destroy()

def getChatMessage(msg):
    msg = msg.replace('\n', '')
    texts = tkDisplay.get("1.0", tk.END).strip()

    tkDisplay.config(state=tk.NORMAL)

    if len(texts) < 1:
        tkDisplay.insert(tk.END, "Voce >>>" + msg, "tag_your_message")
    else:
        tkDisplay.insert(tk.END, "\n\n" + "Voce >>>" + msg, "tag_your_message")

    tkDisplay.config(state=tk.DISABLED)

    send_mssage_to_server(msg)

    tkDisplay.see(tk.END)
    tkMessage.delete('1.0', tk.END)

def send_mssage_to_server(msg):
    client_msg = str(msg)
    client.send(client_msg.encode())
    if msg == "exit":
        client.close()
        window.destroy()
    print("Enviando Mensagem")

def connect_to_server(name,porta):
    global client, HOST_PORT, HOST_ADDR

    try:
        HOST_PORT = int(porta)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        client.send(name.encode())

        entName.config(state=tk.DISABLED)
        btnConnect.config(state=tk.DISABLED)
        tkMessage.config(state=tk.NORMAL)

        threading._start_new_thread(receive_message_from_server, (client, "m"))
    except Exception as e:
        tk.messagebox.showerror(title="[ERROR]", message="Nao foi possivel se conectar a: " + HOST_ADDR + " pela porta: " + str(HOST_PORT) + "\n")

def connect():
    global username, client,porta
    if len(entName.get()) < 1:
        tk.messagebox.showerror(title="[ERROR]", message="Voce deve escolher um nome")
    else:
        username = entName.get()
        porta = entPort.get()
        connect_to_server(username,porta)

window.mainloop()

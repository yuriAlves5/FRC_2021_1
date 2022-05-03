from socket import *
import tkinter as tk
import threading

server = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080
client_name = " "
clients = []
clients_names = []
Server_max_clients = 0
connected_clients = 0
Name_room = " "


gui = tk.Tk()
gui.title("Sever")

mainFrame = tk.Frame(gui)
labelMax = tk.Label(mainFrame, text = "Max:").pack(side=tk.LEFT)
entryMax = tk.Entry(mainFrame)
entryMax.pack(side=tk.LEFT)

labelServer = tk.Label(mainFrame, text = "Porta:").pack(side=tk.LEFT)
entryServer = tk.Entry(mainFrame)
entryServer.pack(side=tk.LEFT)

labelName = tk.Label(mainFrame, text = "Nome sala:").pack(side=tk.LEFT)
entryName = tk.Entry(mainFrame)
entryName.pack(side=tk.LEFT)

buttonStart = tk.Button(mainFrame, text="Connect", command=lambda : connectServer())
buttonStart.pack(side=tk.LEFT)

buttonStop = tk.Button(mainFrame, text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
buttonStop.pack(side=tk.LEFT)
mainFrame.pack(side=tk.TOP, pady=(5, 0))

middleFrame = tk.Frame(gui)
labelName = tk.Label(middleFrame, text = "sala: _UNDEFINED_")
labelName.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port: XXXX")
lblPort.pack(side=tk.LEFT)
labelMax = tk.Label(middleFrame, text = "Max pessoas: XX")
labelMax.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

clientFrame = tk.Frame(gui)
labelLine = tk.Label(clientFrame, text="--------- Client List ---------").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
display = tk.Text(clientFrame, height=15, width=30)
display.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=display.yview)
display.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))


# Conncect to server
def connectServer():
    global Server_max_clients, HOST_ADDR, HOST_PORT, Name_room

    if len(entryMax.get()) < 1:
        tk.messagebox.showerror(title="[ERROR]", message="Maximo de conexoes atingido")
    else:
        Name_room = entryName.get()
        HOST_PORT = int(entryServer.get())
        Server_max_clients = entryMax.get()
        start_server()


# Start server function
def start_server():
    global server, HOST_ADDR, HOST_PORT, Name_room, Server_max_clients

    buttonStart.config(state=tk.DISABLED)
    buttonStop.config(state=tk.NORMAL)

    server = socket(AF_INET, SOCK_STREAM)
    print(AF_INET)
    print(SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)

    threading._start_new_thread(accept_clients, (server, " "))

    labelName["text"] = "Sala: " + Name_room
    lblPort["text"] = "Port: " + str(HOST_PORT)
    labelMax["text"] = "Max pessoas: " + str(Server_max_clients)

def stop_server():
    global server
    buttonStart.config(state=tk.NORMAL)
    buttonStop.config(state=tk.DISABLED)

def accept_clients(the_server, client_connection):
    global connected_clients

    while int(Server_max_clients) >= connected_clients:
        connected_clients = connected_clients + 1
        client, addr = the_server.accept()
        clients.append(client)

        threading._start_new_thread(send_receive_client_message, (client, addr))

def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, clients_addr, connected_clients
    client_msg = " "

    client_name  = client_connection.recv(4096).decode()
    welcome_msg = "Bem-vindo " + client_name + ". Use 'exit' para sair\n"
    client_connection.send(welcome_msg.encode())

    Max_msg = "Maximo de participantes é " + Server_max_clients + " e você é o usuario numero " + str(connected_clients - 1) + "\n"
    client_connection.send(Max_msg.encode())

    Sala_msg = "Se conectou a sala -> " + Name_room
    client_connection.send(Sala_msg.encode())

    clients_names.append(client_name)

    update_client_names_display(clients_names)

    while True:
        data = client_connection.recv(4096).decode()

        if not data: break
        
        if data == "exit":
            connected_clients -= 1
            break

        client_msg = data

        i = get_client_index(clients, client_connection)
        sending_client_name = clients_names[i]

        for client in clients:
            if client != client_connection:
                server_msg = str(sending_client_name + "->" + client_msg)
                client.send(server_msg.encode())

    i = get_client_index(clients, client_connection)

    del clients_names[i]
    del clients[i]

    server_msg = "ATE MAIS!"
    client_connection.send(server_msg.encode())
    client_connection.close()

    update_client_names_display(clients_names)

def get_client_index(client_list, curr_client):
    idx = 0
    for client in client_list:
        if client == curr_client:
            break
        idx = idx + 1

    return idx

def update_client_names_display(name_list):
    display.config(state=tk.NORMAL)
    display.delete('1.0', tk.END)

    for client in name_list:
        display.insert(tk.END, client+"\n")

    display.config(state=tk.DISABLED)


gui.mainloop()

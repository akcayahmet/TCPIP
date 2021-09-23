import socket
import threading
import tkinter as tk
from server import*
from tkinter import *

root=tk.Tk()
root.geometry("1000x600")
root.title("METRO İSTANBUL ARGE TCP PROJESİ-SERVER")

name_var=tk.StringVar()
passw_var=tk.IntVar()
text_var=tk.StringVar()
text1_var=tk.StringVar()
text_var1=tk.StringVar()
text_var2=tk.StringVar()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def submit():
    host="127.0.0.1"
    port=passw_var.get()
    server.bind((host, port))
    server.listen()

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    return
    
def receive():
    while True:
        client, address = server.accept()
        txtMessages2.insert(END, "\n" + "connected to {} ".format(str(address)))
        
        
        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()	

passw_label = tk.Label(root, text = 'PORT', font = ('calibre',10,'bold'))
passw_entry=tk.Entry(root, textvariable = passw_var, font = ('calibre',10,'normal'))
sub_btn=tk.Button(root,text = 'listen', command = submit)

passw_label.grid(row=0,column=0)
passw_entry.grid(row=0,column=1)
sub_btn.grid(row=1,column=1)

txtYourMessage =tk.Entry(root, textvariable = text_var, font = ('calibre',10,'normal'))
txtYourMessage.insert(0,"")
txtYourMessage.grid(row=4, column=0)

txtYourMessage1 =tk.Entry(root, textvariable = text_var1, font = ('calibre',10,'normal'))
txtYourMessage1.insert(0,"")
txtYourMessage1.grid(row=5, column=0)

txtYourMessage2 =tk.Entry(root, textvariable = text_var2, font = ('calibre',10,'normal'))
txtYourMessage2.insert(0,"")
txtYourMessage2.grid(row=6, column=0)

txtMessages = tk.Text(root, width=50)
txtMessages.grid(row=2, column=0)
txtMessages1 = tk.Text(root, width=50)
txtMessages1.grid(row=2, column=1)
txtMessages2 = tk.Text(root, width=30)
txtMessages2.grid(row=2, column=2, padx=25, pady=10)

clients = []

def handle(client):
    while True:
        try:
            print("hi")
            message = client.recv(1024).decode("ascii")
            clients.append(client)
            txtMessages1.insert(1.0, message + "\n")
            broadcast(message)


        except:
            print("hello")
            clients.remove(client)
            client.close()
            break

def sendit():
    for client in clients: 
            thread = threading.Thread(target=handle, args=(client, ))
            thread.start()
            message = txtYourMessage.get()
            txtMessages.insert(1.0,  "You: "+ message + "\n")
            client.send(message.encode("ascii"))

def sendit1():
        for client in clients:
            thread = threading.Thread(target=handle, args=(client, ))
            thread.start()
            message = txtYourMessage1.get()
            txtMessages.insert(1.0,  "You: "+ message + "\n")
            client.send(message.encode("ascii"))
            
def sendit2():
        for client in clients:
            thread = threading.Thread(target=handle, args=(client, ))
            thread.start()
            message = txtYourMessage2.get()
            txtMessages.insert(1.0,  "You: "+ message + "\n")
            client.send(message.encode("ascii"))

def delete():
    txtMessages1.delete(1.0,END)
    txtMessages.delete(1.0,END)

sub_btn2=tk.Button(root,text = 'clear', command = delete)
sub_btn2.grid(row=1,column=3)
            

btnSendMessage = tk.Button(root, text="send", width=20, command=sendit)
btnSendMessage.grid(row=4, column=1)

btnSendMessage1 = tk.Button(root, text="send", width=20, command=sendit1)
btnSendMessage1.grid(row=5, column=1)

btnSendMessage2 = tk.Button(root, text="send", width=20, command=sendit2)
btnSendMessage2.grid(row=6, column=1)

def broadcast(message):
    for client in clients: 
        client.send(message.encode("ascii"))
        print(message)

root.mainloop()
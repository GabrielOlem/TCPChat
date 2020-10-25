import time
import socket
import _thread
import PySimpleGUI as sg
import tkinter as tk
from tkinter import messagebox
import pyglet


abigobal = 0
chats = {}
tipo = 'all'
name=""
HOST = socket.gethostname()
PORT = 22222            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

class Screen:
    def __init__(self, nome):
        sg.theme('DarkBrown1')
        self.name = nome
        self.tipo = 'all'
        self.layout = [
            [sg.Text('Name: ' + self.name, key = '__Name__')],
            [sg.Text('Tipo: ' + self.tipo, key = '__Type__', size=(20, 1))],
            [sg.Output(size=(80,20), key = '__Print__')],
            [sg.Text('Message:'), sg.Input(do_not_clear = False, key = '__Input__'), sg.Button('Send message', bind_return_key = True), sg.Button('Exit')]        
        ]
        self.screen = sg.Window("Chat", self.layout, return_keyboard_events = True)

    def changeChat(self, t):
        self.screen.Element('__Type__').Update(t)
        

    def clearInput(self):
        self.screen.Element('__Input__').Update('')

    def clearOutput(self):
        self.screen.Element('__Print__').Update('')
    
    def setOutput(self, c):
        self.screen.Element('__Print__').Update(c)

    def getContent(self):
        return self.screen.Element('__Print__').Get()
        

class Mensagem:
    def __init__(self, m):
        self.header = m[0]
        if len(m) == 3:
            self.name = m[1]
        elif len(m) == 7:
            self.name = m[1]
            self.ip = m[2]
            self.port = m[3]
            self.msg = m[4]
            self.time = m[5]
        elif len(m) == 8:
            self.name = m[1]
            self.ip = m[2]
            self.port = m[3]
            self.msg = m[4]
            self.time = m[5]
            self.dest = m[6]

def limpa(a):
    saida = ''
    if a[0] == '\n':
        a = a[1:]
    for i in range(len(a)):
        if i + 1 != len(a) and a[i] == '\n' and a[i+1] == '\n':
            i += 1
        else:
            saida += a[i]
    return saida        

def escuta():
    while 1:
        header = tcp.recv(2048)
        if not header: break
        header = header.decode().split('\r\n')
        message = Mensagem(header)
        global tipo
        global UI
        global chats

        if message.header == 'bye0':
            print('O usuario ' + message.name + ' desconectou')
        elif message.header == 'bye1':
            _thread.exit()
        elif message.header == 'list':
            print('Usuarios conectados no momento:')
            print(message.name, end = '')
        elif message.header == 'msg0':
            if tipo != 'all':
                chats[tipo] = limpa(UI.getContent())
                tipo = 'all'
                UI.changeChat('Tipo: ' + tipo)
                UI.setOutput(chats[tipo])
            print(message.ip + ':' + message.port + '/~' + message.name + ': ' + message.msg + ' ' + message.time)
        elif message.header == 'msg1':
            chats[tipo] = limpa(UI.getContent())
            tipo = message.name
            UI.changeChat('Tipo: ' + tipo)
            if tipo in chats:
                UI.setOutput(chats[tipo])
            else:
                UI.clearOutput()
            
            print('(pm)' + message.ip + ':' + message.port + '/~' + message.name + ': ' + message.msg + ' ' + message.time)
        elif message.header == 'msg2':
            chats[tipo] = limpa(UI.getContent())
            tipo = message.dest
            UI.changeChat('Tipo: ' + tipo)
            if tipo in chats:
                print(tipo)
                UI.setOutput(chats[tipo])
            else:
                UI.clearOutput()
            
            print('(pm)' + message.ip + ':' + message.port + '/~' + message.name + ': ' + message.msg + ' ' + message.time)
        elif message.header == 'erro':
            global abigobal
            abigobal = 1

def getInput(root,user_text):
    global tcp
    global name
    name=user_text.get()
    user_text.delete(0,tk.END)

    if " " in name:
        messagebox.showerror("ERRO","Nao eh permitido espacos! Insira o nome novamente:")
    elif name=="":
        messagebox.showerror("ERRO","Nome Vazio,  Insira o nome novamente:")
    else:
        tcp.send(name.encode())
    
        a = tcp.recv(2048)
        if a == b'0':
            messagebox.showerror("ERRO","Nome ja registrado, insira outro nome:")
        elif a == b'1':
            root.destroy()


#main

root=tk.Tk()
root.title("Chat app")
root.geometry("300x120")
root.resizable(0,0)
root.configure(background="#2c231f")

pyglet.font.add_file("fonts/omegaflight3d.ttf")

title_frame=tk.LabelFrame(root,padx=5,pady=5,bg="#493933",highlightbackground="#000000")
main_frame=tk.LabelFrame(root,padx=5,pady=5,bg="#493933",highlightbackground="#000000")

title=tk.Label(title_frame,text="Chat login",font=("Omega Flight 3D",20),bg="#493933",fg="#9C8529")
user_text=tk.Entry(main_frame,bg="#6d5c53",fg="#D5B638")
login_button=tk.Button(main_frame,text="Login",command=lambda: getInput(root,user_text),bg="#f7da68")
text1=tk.Label(main_frame,text="User name:",bg="#493933",fg="#9C8529")

user_text.bind("<Return>",lambda event: getInput(root,user_text))


title_frame.pack(pady=10)
main_frame.pack()

title.grid(row=0,column=0)
text1.grid(row=1,column=0)
user_text.grid(row=1,column=1)
login_button.grid(row=1,column=2,padx=5)
root.mainloop()


UI = Screen(name)

_thread.start_new_thread(escuta, ())
while 1:
    event, msg = UI.screen.Read()
    msg = msg['__Input__']
    if abigobal == 1:
        sg.popup_no_buttons('Usuario nao encontrado')
        abigobal = 0
    if event in ('Send message', ''):
        UI.clearInput()
        tempo = time.localtime()[0:5]
        tempo = str(tempo[3]) + 'h' + str(tempo[4]) + ' ' + str(tempo[2]) + '/' + str(tempo[1]) + '/' + str(tempo[0])
        novo = msg.split(' ')
        if novo[0] == 'bye' and len(novo) == 1:
            tcp.send('bye\r\n'.encode())
            quit()
        elif novo[0] == 'list' and len(novo) == 1:
            tcp.send('list\r\n'.encode())
        elif novo[0] == 'send' and len(novo) > 1:
            if novo[1] == '-all' and len(novo) > 2:
                tcp.send(('send\r\n-all\r\n'+ msg[10:] + '\r\n' + tempo + '\r\n').encode())
            elif novo[1] == '-user' and len(novo) > 3 and novo[2] != name:
                tcp.send(('send\r\n-user\r\n'+ novo[2] + '\r\n' + msg[11 + len(novo[2]):] + '\r\n' + tempo + '\r\n').encode())
            else:
                sg.popup_no_buttons('Codigo mal inserido')
        elif novo[0] == 'clear':
            UI.clearOutput()
        elif novo[0] == 'show':
            print(chats)
        else:
            sg.popup_no_buttons('Codigo mal inserido')
    elif event in ('Exit', sg.WIN_CLOSED):
        tcp.send(b'bye\r\n')
        quit()




tcp.close()

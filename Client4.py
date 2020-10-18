import time
import socket
import _thread
import pickle
import PySimpleGUI as sg

class Screen:
    def __init__(self, nome):
        sg.theme('DarkBrown1')
        layout = [
            [sg.Text('Name: ' + nome)],
            [sg.Output(size=(80,20))],
            [sg.Text('Message:'), sg.Input(do_not_clear = False), sg.Button('Send message', bind_return_key = True), sg.Button('Exit')]
        ]
        self.screen = sg.Window("Chat", layout, return_keyboard_events = True);

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

def escuta():
    while 1:
        header = tcp.recv(2048)
        if not header: break
        header = header.decode().split('\r\n')
        message = Mensagem(header)
    
        if message.header == 'bye0':
            print('O usuario ' + message.name + ' desconectou')
        elif message.header == 'bye1':
            _thread.exit()
        elif message.header == 'list':
            print('Usuarios conectados no momento:')
            print(message.name, end = '')
        elif message.header == 'msg0':
            print(message.ip + ':' + message.port + '/~' + message.name + ': ' + message.msg + ' ' + message.time)
        elif message.header == 'msg1':
            print('(pm)' + message.ip + ':' + message.port + '/~' + message.name + ': ' + message.msg + ' ' + message.time)
        elif message.header == 'erro':
            print('Usuario nao encontrado')

name = input('Insira seu nome:')
while 1:
    if ' ' in name:
        name = input('Nao eh permitido espacos! Insira o nome novamente:')
    else:
        break

HOST = socket.gethostname()
PORT = 22222            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
tcp.send(name.encode())

while 1:
    a = tcp.recv(2048)
    if a == b'0':
        name = input('Nome ja registrado, insira outro nome:')
        while 1:
            if ' ' in name:
                name = input('Nao eh permitido espacos! Insira o nome novamente:')
            else:
                break
        tcp.send(name.encode())
    elif a == b'1':
        break

UI = Screen(name)

_thread.start_new_thread(escuta, ())
while 1:
    event, msg = UI.screen.Read()
    msg = msg[0]

    if event in ('Send message', ''):
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
            elif novo[1] == '-user' and len(novo) > 3:
                tcp.send(('send\r\n-user\r\n'+ novo[2] + '\r\n' + msg[11 + len(novo[2]):] + '\r\n' + tempo + '\r\n').encode())
            else:
                print('Codigo mal inserido')
        elif msg == 'quit':
            quit()
        else:
            print('Codigo mal inserido')
    elif event in ('Exit', sg.WIN_CLOSED):
        tcp.send(b'bye\r\n')
        quit()
    


    
tcp.close()
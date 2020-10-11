import time
import socket
import _thread
import pickle
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
            data = tcp.recv(2048)
            data = pickle.loads(data)
            for x in data:
                print(x.decode())
        elif message.header == 'msg0':
            print(message.ip + ':' + message.port + '/~' + message.name + ': ' + message.msg + ' ' + message.time)
        elif message.header == 'msg1':
            print('(pm)' + message.ip + ':' + message.port + '/~' + message.name + ': ' + message.msg + ' ' + message.time)
        elif message.header == 'erro':
            print('Usuario nao encontrado')

name = input('Insert your name:')
HOST = socket.gethostname()
PORT = 22222            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
tcp.send(name.encode())

_thread.start_new_thread(escuta, ())
while 1:
    msg = input()
    if msg == "":
        continue
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
    


    
tcp.close()
import time
import socket
import _thread
import pickle


name = input('Insert your name:')
HOST = socket.gethostname()
PORT = 22222            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
tcp.send(name.encode())


def escuta():
    while 1:
        header = tcp.recv(4)
        if not header: break
        #data = tcp.recv(2048)
        #data = pickle.loads(data)
        if header == b'bye0':
            data = tcp.recv(2048)
            data = pickle.loads(data)
            print('O usuario ' + data.decode() + ' desconectou')
        elif header == b'bye1':
            _thread.exit()
        elif header == b'list':
            print('Usuarios conectados no momento:')
            data = tcp.recv(2048)
            data = pickle.loads(data)
            for x in data:
                print(x.decode())
        elif header == b'msg0':
            user = pickle.loads(tcp.recv(2048))
            msg = tcp.recv(2048)
            tempo = pickle.loads(tcp.recv(2048))
            print(user[1][0] + ':' + str(user[1][1]) + '/~' + user[0].decode() + ': ' + msg.decode() + ' ' + str(tempo[3]) + 'h' + str(tempo[4]) + ' ' + str(tempo[2]) + '/' + str(tempo[1]) + '/' + str(tempo[0]))
        elif header == b'msg1':
            user = pickle.loads(tcp.recv(2048))
            msg = tcp.recv(2048)
            tempo = pickle.loads(tcp.recv(2048))
            print('(pm)' + user[1][0] + ':' + str(user[1][1]) + '/~' + user[0].decode() + ': ' + msg.decode() + ' ' + str(tempo[3]) + 'h' + str(tempo[4]) + ' ' + str(tempo[2]) + '/' + str(tempo[1]) + '/' + str(tempo[0]))
        elif header == b'erro':
            print('Usuario nao encontrado')

_thread.start_new_thread(escuta, ())
msg = 'a'
while 1:
    msg = input()
    if msg == "":
        continue
    tempo = time.localtime()[0:5]
    novo = msg.split(' ')
    if novo[0] == 'bye' and len(novo) == 1:
        tcp.send('bye'.encode())
        quit()
    elif novo[0] == 'list' and len(novo) == 1:
        tcp.send('list'.encode())
    elif novo[0] == 'send' and len(novo) > 1:
        tcp.send('send'.encode())
        if novo[1] == '-all' and len(novo) > 2:
            tcp.send('-all'.encode())
            tcp.send(msg[10:].encode())
            tcp.send(pickle.dumps(tempo))
        elif novo[1] == '-user' and len(novo) > 3:
            tcp.send('-user'.encode())
            tcp.send(novo[2].encode())
            tcp.send(msg[11:].encode())
            tcp.send(pickle.dumps(tempo))
        else:
            print('Codigo mal inserido')
    elif msg == 'quit':
        quit()
    else:
        print('Codigo mal inserido')
    


    
tcp.close()
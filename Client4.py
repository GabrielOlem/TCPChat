import sys
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
        if header == b'bye':
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
        elif header == b'msg':
            user = tcp.recv(2048)
            user = pickle.loads(user)
            print(sys.getsizeof(user))
            print(user[0].decode())
            msg = tcp.recv(2048)
            print(msg.decode())
        #else:
            #print (data[0][0] + ':' + str(data[0][1]) + '/~' + data[1].decode() + ':' + data[2].decode())

        #result = pickle.loads(result)
        #

_thread.start_new_thread(escuta, ())
msg = 'a'
while msg != '\x18':
    msg = input()
    tcp.send (msg.encode())

    
tcp.close()
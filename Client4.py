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
        result = tcp.recv(2048)
        result = pickle.loads(result)
        print (result[0][0], ':', result[0][1], '/~', result[1].decode())


_thread.start_new_thread(escuta, ())
msg = 'a'
while msg != '\x18':
    msg = input()
    tcp.send (msg.encode())

    
tcp.close()
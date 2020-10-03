import socket
import _thread
import pickle


name = input('Insert your name:')
HOST = '179.106.3.142'
PORT = 5555            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)


def escuta():
    while 1:
        result = tcp.recv(2048)
        print (result)


_thread.start_new_thread(escuta, ())
msg = 'a'
while msg != '\x18':
    msg = input(HOST + ':' + 'porta' + '/~' + name + ': ')
    tcp.send (msg.encode())

    
tcp.close()
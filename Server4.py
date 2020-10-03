import socket
import _thread
import pickle

host = ''
port = 5555
usuarios = []

def conectado(con, cliente):
    print ('Conectado por', cliente)
    while 1:
        msg = con.recv(2048)
        if not msg: break
        print (cliente, msg)
        for x in usuarios:
            if x != con:
                #a = (cliente[0], cliente[1], msg)
                #teste = pickle.dumps(a)
                x.send(msg)
    print ('Finalizando conexao do cliente', cliente)
    #usuarios.remove(con)
    con.close()
    _thread.exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (host, port)

tcp.bind(orig)
tcp.listen(1)

while 1:
    con, cliente = tcp.accept()
    #con.send(pickle.dumps((cliente[0], cliente[1], )))
    usuarios.append(con)
    _thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
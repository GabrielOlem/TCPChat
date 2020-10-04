import socket
import _thread
import pickle

host = ''
port = 22222
amount = 0
usuarios = []

def conectado(user):
    print ('Conectado por', cliente)
    while 1:
        msg = user[0].recv(2048)
        if not msg: break
        for x in usuarios:
            if x != user:
                #a = (cliente[0], cliente[1], msg)
                #teste = pickle.dumps(a)
                x[0].send(pickle.dumps((cliente, msg)))
                print('Message sent by', x[2][0])
            
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
    recebe = con.recv(2048)
    #con.send(pickle.dumps((cliente[0], cliente[1], )))
    usuarios.append((con, recebe, cliente))
    _thread.start_new_thread(conectado, tuple([usuarios[amount]]))
    amount += 1

tcp.close()
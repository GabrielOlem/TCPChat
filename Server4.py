import socket
import _thread
import pickle

host = ''
port = 22222
amount = 0
usuarios = []



def conectado(user):
    print ('Conectado por', user[2])
    while 1:
        msg = user[0].recv(4)
        if not msg: break
        if msg == b'bye':
            print([a for (a, b, c) in usuarios])
            user[0].send(b'bye1')
            usuarios.remove(user)
            global amount
            amount -= 1
            for x in usuarios:
                x[0].send(b'bye')
                x[0].send(pickle.dumps(user[1]))
            print ('Finalizando conexao do cliente', user[2])
            user[0].close()
            _thread.exit()
        elif msg == b'list':
            user[0].send(b'list')
            print([b for (a, b, c) in usuarios])
            user[0].send(pickle.dumps([b for (a, b, c) in usuarios]))
        elif msg == b'send':
            msg = user[0].recv(4)
            if msg == b'-all':
                msg = user[0].recv(2048)
                for x in usuarios:
                    if x != user:
                        x[0].send(b'msg')
                        x[0].send(pickle.dumps([user[1], user[2]]))
                        x[0].send(msg)
        '''for x in usuarios:
            if x != user:
                #a = (cliente[0], cliente[1], msg)
                #teste = pickle.dumps(a)
                x[0].send(pickle.dumps((cliente, name, msg)))
                print('Message sent to', x[2][0])'''

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
    name = con.recv(2048)
    #con.send(pickle.dumps((cliente[0], cliente[1], )))
    usuarios.append((con, name, cliente))
    _thread.start_new_thread(conectado, tuple([usuarios[amount]]))
    amount += 1

tcp.close()
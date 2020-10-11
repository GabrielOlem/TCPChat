import socket
import _thread
import pickle

host = ''
port = 22222
amount = 0
usuarios = []
# Criar um dicionario para cada usuario, que a chave é a conexao Usuarios = {Con1:{'name': nome, 'cliente':cliente}}
# atentar para caso não exista

class Usuario:
    def __init__(self, co, n, cl):
        self.conexao = co
        self.name = n
        self.cliente = cl

def conectado(user):
    print ('Conectado por', user.cliente)
    while 1:
        msg = user.conexao.recv(4)
        if not msg: break
        if msg == b'bye':
            user.conexao.send(b'bye1')
            usuarios.remove(user)
            global amount
            amount -= 1
            for x in usuarios:
                x.conexao.send(b'bye0')
                x.conexao.send(pickle.dumps(user.name))
            print ('Finalizando conexao do cliente', user.cliente)
            user.conexao.close()
            _thread.exit()
        elif msg == b'list':
            user.conexao.send(b'list')
            user.conexao.send(pickle.dumps([x.name for x in usuarios]))
        elif msg == b'send':
            msg = user.conexao.recv(5)
            if msg == b'-all':
                msg = user.conexao.recv(2048)
                tempo = user.conexao.recv(2048)
                for x in usuarios:
                    if x != user:
                        x.conexao.send(b'msg0')
                        x.conexao.send(pickle.dumps([user.name, user.cliente]))
                        x.conexao.send(msg)
                        x.conexao.send(tempo)
            elif msg == b'-user':
                target = user.conexao.recv(10)
                msg = user.conexao.recv(2048)
                tempo = user.conexao.recv(2048)
                tUser = -1
                for x in usuarios:
                    if x.name == target:
                        tUser = x
                        break
                if tUser == -1:
                    user.conexao.send(b'erro')
                else:
                    tUser.conexao.send(b'msg1')
                    tUser.conexao.send(pickle.dumps([user.name, user.cliente]))
                    tUser.conexao.send(msg)
                    tUser.conexao.send(tempo)
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
    usuarios.append(Usuario(con, name, cliente))
    _thread.start_new_thread(conectado, tuple([usuarios[amount]]))
    amount += 1

tcp.close()
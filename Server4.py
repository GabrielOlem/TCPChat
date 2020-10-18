import socket
import _thread

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

class Mensagem:
    def __init__(self, msg):
        self.header = msg[0]
        if len(msg) == 5:
            self.tipo = msg[1]
            self.msg = msg[2]
            self.tempo = msg[3]
        if len(msg) == 6:
            self.tipo = msg[1]
            self.user = msg[2]
            self.msg = msg[3]
            self.tempo = msg[4]

def conectado(user):
    print ('Conectado por', user.cliente)
    while 1:
        msg = user.conexao.recv(2048)
        if not msg: break
        msg = msg.decode().split('\r\n')
        msg = Mensagem(msg)
        if msg.header == 'bye':
            user.conexao.send(b'bye1\r\n')
            usuarios.remove(user)
            global amount
            amount -= 1
            for x in usuarios:
                x.conexao.send(('bye0\r\n' + (user.name).decode() + '\r\n').encode())
            print ('Finalizando conexao do cliente', user.cliente)
            user.conexao.close()
            _thread.exit()
        elif msg.header == 'list':
            saida = ''
            for x in usuarios:
                saida += x.name.decode() + '\n'
            user.conexao.send(('list\r\n' + saida + '\r\n').encode())
            
        elif msg.header == 'send':
            if msg.tipo == '-all':
                for x in usuarios:
                    #if x != user:
                    x.conexao.send(('msg0\r\n' + (user.name).decode() + '\r\n' + str(user.cliente[0]) + '\r\n' + str(user.cliente[1]) + '\r\n' + msg.msg + '\r\n' + msg.tempo + '\r\n').encode())
            elif msg.tipo == '-user':
                tUser = -1
                for x in usuarios:
                    if x.name.decode() == msg.user:
                        tUser = x
                        break
                if tUser == -1:
                    user.conexao.send(b'erro\r\n')
                else:
                    tUser.conexao.send(('msg1\r\n' + (user.name).decode() + '\r\n' + str(user.cliente[0]) + '\r\n' + str(user.cliente[1]) + '\r\n' + msg.msg + '\r\n' + msg.tempo + '\r\n').encode())
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
    #confirmacao de nome
    while 1:
        name = con.recv(2048)
        if name in [x.name for x in usuarios]:
            con.send(b'0')
        else:
            con.send(b'1')
            break 

    #con.send(pickle.dumps((cliente[0], cliente[1], )))
    usuarios.append(Usuario(con, name, cliente))
    _thread.start_new_thread(conectado, tuple([usuarios[amount]]))
    amount += 1

tcp.close()
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle


clients = {}
addresses = {}

host = '127.0.0.1'
port = 8080
buffer_size = 1024
address = (host, port)

server = socket(AF_INET, SOCK_STREAM)
server.bind(address)


def accepting_connection():
    while True:
        connection, address = server.accept()
        addresses[connection] = address
        Thread(target=handle_client, args=(connection,)).start()


def handle_client(client):
    client.send(bytes('enter your name', 'utf8'))
    name = client.recv(buffer_size).decode('utf8')
    clients[client] = name
    broadcast(bytes(name+' joined the chat', 'utf8'), 'server')

    while True:
        message = client.recv(buffer_size)
        if not message:
            break
        if message == bytes('exit0', 'utf8'):
            client.close()
            del clients[client], addresses[client]
            broadcast(bytes(name+' left', 'utf8'))
            break

        else:
            broadcast(message, name)


def broadcast(message, sender=""):
    for client in clients:
        client.send(bytes(sender + ': ', 'utf8') + message)


if __name__ == '__main__':
    server.listen(10)
    print('server started')
    connection_acceptor = Thread(target=accepting_connection)
    connection_acceptor.start()
    connection_acceptor.join()
    server.close()
    print('server closed')
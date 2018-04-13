from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


clients = {}
addresses = {}

host = '127.0.0.1'
port = 8080
buffer_size = 1024
address = (host, port)

server = socket(AF_INET, SOCK_STREAM)
server.bind(address)


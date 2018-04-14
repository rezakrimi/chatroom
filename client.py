from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import filedialog


def receive():
    while True:
        try:
            message = client_socket.recv(buffer_size).decode('utf8')
            if not message: break
            msg_list.insert(tkinter.END, message)
        except:
            break


def send(event=None):
    message = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(message, 'utf8'))
    if message == 'exit0':
        client_socket.close()
        top.quit()


def on_closing(event=None):
    my_msg.set('exit0')
    send()


def send_file(event=None):
    name = filedialog.askopenfilename(filetypes=(("Text File", "*.txt"),("All Files","*.*"), ('python files', '*.py')),
                           title = "Choose a file."
                           )
    part = name.split('/')
    client_socket_file.send(bytes(part[-1], 'utf8'))
    try:
        with open(name, 'rb') as fs:
            # Using with, no file close is necessary,
            # with automatically handles file close
            client_socket_file.send(b'BEGIN')
            while True:
                data = fs.read(buffer_size)
                print('Sending data: ', data.decode('utf-8'))
                client_socket_file.send(data)
                print('Sent data: ', data.decode('utf-8'))
                if not data:
                    print('Breaking from sending data')
                    break
            client_socket_file.send(b'ENDED')  # I used the same size of the BEGIN token
            fs.close()
    except:
        print('cant open file')

top = tkinter.Tk()
top.title('chatroom')
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set('')
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

msg_list = tkinter.Listbox(messages_frame, height=30, width=80, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
top.protocol("WM_DELETE_WINDOW", on_closing)

send_file_button = tkinter.Button(top, text="Send File", command=send_file)
send_file_button.pack()

host = '127.0.0.1'
port = 8080
buffer_size = 1024
address = (host, port)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(address)
client_socket_file = socket(AF_INET, SOCK_STREAM)
client_socket_file.connect(address)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
print('salam')



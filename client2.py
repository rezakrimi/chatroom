from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


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

host = '127.0.0.1'
port = 8080
buffer_size = 1024
address = (host, port)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(address)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()



import socket
import threading

#Create globle variable to check if the message from self.
middle = ''



def connect():
    lock = threading.Lock()
    # create a socket object
    customer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serip = '192.168.1.238' #Server ip
    port = 23165
    host = customer.connect((serip, port))
    return customer

# send and receive data
def recv():
    while True:
        msg = customer.recv(1024)
        data = msg.decode()
        if data == middle:
            continue
        print('--------------')
        print(f"{data}")
        print('--------------')

def send():
    global middle
    serip = '192.168.1.238'
    while True:
        data = input()
        middle = serip +"send: \n"+data
        customer.send(middle.encode())


if __name__ == '__main__':
    customer = connect()
    t1 = threading.Thread(target=recv)
    t2 = threading.Thread(target=send)
    t1.start()
    t2.start()
import socket
import threading

serip = '192.168.1.238' #Server ip
port = 23165
#Create globle variable to check if the message from self.
middle = ''
username = str(input('Enter your name: '))
while len(username)==0:
    username = str(input('Enter your name: '))

def connect():
    lock = threading.Lock()
    # create a socket object
    customer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = customer.connect((serip, port))
    print(f'User {username} connected on {serip}, you can send exit to exit to program.')
    return customer

# send and receive data
def recv():
    try:
        while True:
            msg = customer.recv(1024)
            data = msg.decode()
            if data == middle:
                continue
            print(f"{data}")
            print('--------------')
    except (ConnectionAbortedError):
        print("You have successfully exited!")

def send():
    global middle

    while True:
        data = input()
        if data == "exit":
            customer.send(f'{username} exited!~'.encode())
            customer.close()
            break
        middle = username +" send: \n-->"+data
        customer.send(middle.encode())


if __name__ == '__main__':
    customer = connect()
    customer.send(f'{username} is online!'.encode())
    t1 = threading.Thread(target=recv)
    t2 = threading.Thread(target=send)
    t1.start()
    t2.start()
import socket
import threading

HOST = '192.168.1.238'  #put your own ip here
PORT = 23165

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1000)

#use set ensure the unqueness
customers = set()
print(f'Server started on {HOST}:{PORT}')


def send_all(data,address):
    global customers
    try:
        for customer in customers:
            customer.send(data)
    except(ConnectionResetError):
        print("User exit!")
        customers.remove(customer)    

def display_msg(customer, address):
    global customers
    customers.add(customer)
    while True:
        data = customer.recv(1024)
        if len(data) == 0:
            break
        send_all(data,address)

if __name__ == '__main__':
    while True:
        customer, address = server.accept()
        recv_thread = threading.Thread(target=display_msg,args=(customer,address))
        recv_thread.setDaemon(True)

        recv_thread.start()
import socket
import threading

HOST = '192.168.1.238'  #local ipv4
PORT = 23165

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1000)
print(f'Server started on {HOST}:{PORT}')
print('Waiting for clients connection--------')

#use set ensure the unqueness
customers = set()
userlist = list()

def send_all(data,address):
    global customers

    for customer in customers:
        customer.send(data)
           
#Handling message
def display_msg(customer, address):
    global customers
    customers.add(customer)
    k = 1
    try:
        while True:
            data = customer.recv(1024)
            if k==1: #Run only once for login
                login = data.decode()
                user = (login[:(len(login)-11)])
                userlist.append(user)
                print(f'{user} connected at {address}!')
                print(f'------Current active user{userlist}------')
                customer.sendall(f'------Current active user{userlist}------'.encode())
                k+=1  

                pass
            if len(data) == 0:
                break
            exitmsg = data.decode()
            if exitmsg[-1] == "~":
                exituser = (exitmsg[:(len(exitmsg)-9)])
                
            else:
                send_all(data,address)
    except (ConnectionResetError):
        print(f'{exituser} exited at {address}!')
        userlist.remove(exituser)
        if len(userlist) == 0:
            print("There is no active user right now")
        else:
            print(f'Current active user {userlist}')
        customers.remove(customer)
        for customer in customers:
            customer.send(f'{exituser} exited!'.encode())
      

if __name__ == '__main__':
    while True:
        customer, address = server.accept()
        recv_thread = threading.Thread(target=display_msg,args=(customer,address))
        recv_thread.daemon=True

        recv_thread.start()
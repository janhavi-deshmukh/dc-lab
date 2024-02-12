import socket
import json

# Server configuration
host = "127.0.0.1"  # localhost
port = 12345         # port to connect to

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

loggedin = False

while True:
    if not loggedin:
        print('Login:')
        print('Choose your role:\n1: Student\n2: Faculty\n3: Administrator\n\n')
        role = int(input('Enter role: '))
        id = int(input('Enter id: '))
        password = input('Enter password: ')
        message = json.dumps({'role': role, 'id': id, 'password': password})
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024).decode()
        print(f"Received data from server: {data}\n\n")
        if data == "Logged in successfully":
            loggedin = True
    elif role == 3:
        inp = int(input('What do you want to do?:\n\n1: Register a new teacher\n2: View all teachers\n3: Logout\n\n'))
        if inp == 1:
            name = input('Enter full name of the teacher: ')
            phone_no = input('Enter phone number: ')
            password = input('Enter password: ')
            message = json.dumps({'id': id, 'task': 1, 'name': name, 'phone_no': phone_no,'password': password})
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024).decode()
            print(f"Received data from server: {data}\n\n")
        elif inp == 2:
            message = json.dumps({'id': id, 'task': 2})
            client_socket.sendall(message.encode())
            data = json.loads(client_socket.recv(1024).decode())
            print("All teachers:")
            print(data)
            print('\n')
        elif inp == 3:
            loggedin = False
            message = json.dumps({'id': id, 'task': 3})
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024).decode()
            print(f"Received data from server: {data}\n\n")
    elif role == 2:
        inp = int(input('What do you want to do?:\n\n1: Add a new course\n2: View all your courses\n\n'))
        if inp == 1:
            course_name = input('Enter name of the course: ')
            course_code = input('Enter course code: ')
            message = json.dumps({'id': id, 'task': 4, 'course_name': course_name, 'course_code': course_code})
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024).decode()
            print(f"Received data from server: {data}\n\n")
        elif inp == 2:
            message = json.dumps({'id': id, 'task': 5})
            client_socket.sendall(message.encode())
            data = json.loads(client_socket.recv(1024).decode())
            print("All courses:")
            print(data)
            print('\n')
        # client_socket.sendall(message.encode())
        # data = client_socket.recv(1024).decode()
        
    

# Close the connection
client_socket.close()

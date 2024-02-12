import mysql.connector
import socket
import json
import bcrypt
import grpc
import teacher_pb2
import teacher_pb2_grpc
import Pyro5.api

# MySQL database configuration
host = "localhost"
user = "springstudent"
password = "springstudent"
database = "dc_exp2"


# session
admins = set()
loggedin_teachers = set()

course_dao = None

# Server configuration
host = "127.0.0.1"  # localhost
port = 12345         # port to bind to

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on {host}:{port}")

# Establishing the connection
try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        print("Connected to the database!")

        # Perform database operations here
        # For example, you can create a cursor and execute SQL queries
        cursor = connection.cursor()

        while True:
            # Wait for a client to connect
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            while True:
                # Receive and send back data
                rcvd_data = client_socket.recv(1024)
                send_message = "Functioning not implemented"
                data = json.loads(rcvd_data.decode())
                print(f"Received data: {data}")

                if data['id'] not in admins and data['id'] not in loggedin_teachers:
                    if 'role' not in data:
                        send_message = "Unauthorized access"
                    elif data['role'] != 1:
                        cursor.execute(
                            "select id, password, role from user where id=%s", (data['id'], ))
                        row = cursor.fetchone()
                        print('row:')
                        print(row)
                        if row is None:
                            send_message = "Invalid login"
                        elif bcrypt.checkpw(data['password'].encode(), bytes(row[1])):
                            if data['role'] == 2 and row[2] == 'faculty':
                                loggedin_teachers.add(row[0])
                                send_message = "Logged in successfully"
                            elif data['role'] == 3 and row[2] == 'administrator':
                                admins.add(row[0])
                                send_message = "Logged in successfully"
                            else:
                                send_message = "Invalid login"
                        else:
                            send_message = "Invalid login"
                elif data['task'] == 3:
                    if data['id'] in admins:
                        admins.remove(data['id'])
                    send_message = "Logged out successfully"
                elif data['task'] == 1:
                    # RPC to another server
                    with grpc.insecure_channel("localhost:50051") as channel:
                        stub = teacher_pb2_grpc.TeacherStub(channel)
                        request = teacher_pb2.TeacherData(name=data['name'], phone_no=data['phone_no'], password=data['password'])
                        send_message = stub.Register(request).message
                elif data['task'] == 2:
                    # RPC to another server
                    with grpc.insecure_channel("localhost:50051") as channel:
                        stub = teacher_pb2_grpc.TeacherStub(channel)
                        request = teacher_pb2.Temp()
                        teachers = stub.ShowAll(request).data
                        result = []
                        for i in teachers:
                            result.append({'id': i.id, 'name': i.name, 'phone_no': i.phone_no})
                        send_message = json.dumps(result)
                elif data['task'] == 4:
                    if course_dao is None:
                        course_dao = Pyro5.api.Proxy("PYRONAME:rmi.CourseDAO")   
                    send_message = course_dao.insert(name=data['course_name'], code=data['course_code'], faculty=data['id']) 
                elif data['task'] == 5:
                    if course_dao is None:
                        course_dao = Pyro5.api.Proxy("PYRONAME:rmi.CourseDAO")   
                    send_message = json.dumps(course_dao.show_all(faculty=data['id']))

                # Echo back the received data
                client_socket.sendall(send_message.encode())
            # close the connection
            client_socket.close()

except mysql.connector.Error as e:
    print(f"Error connecting to the database: {e}")

finally:
    if connection.is_connected():
        # Closing the connection in the finally block to ensure it's always closed
        connection.close()
        print("Connection closed.")

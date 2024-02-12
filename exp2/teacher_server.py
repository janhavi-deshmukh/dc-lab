from concurrent import futures
from sqlite3 import connect
import mysql.connector
import json
import bcrypt

import grpc
import teacher_pb2
import teacher_pb2_grpc

# MySQL database configuration
host = "localhost"
user = "springstudent"
password = "springstudent"
database = "dc_exp2"

class TeacherServicer(teacher_pb2_grpc.TeacherServicer):
    """Provides methods that implement functionality of Teacher server."""
    def __init__(self):
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if connection.is_connected():
                print("Connected to the database!")
                self.connection = connection
                self.cursor = connection.cursor()
        except mysql.connector.Error as e:
            print(f"Error connecting to the database: {e}")

    def Register(self, request, context):
        hash = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt()).hex()
        statement = f'insert into user (name, phone_no, role, password) values ("{request.name}", "{request.phone_no}", "faculty", X\'{hash}\')'
        self.cursor.execute(statement)
        self.connection.commit()
        teacher_id = self.cursor.lastrowid
        return teacher_pb2.RegisterResponse(message=f'Registered successfully with id {teacher_id}')

    def ShowAll(self, request, context):
        self.cursor.execute('select id, name, phone_no from user where role="faculty"')
        result = []
        for row in self.cursor:
            result.append(teacher_pb2.Teachers.TeacherData(id=row[0], name=row[1], phone_no=row[2]))
        return teacher_pb2.Teachers(data=result)
    
    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    teacher_pb2_grpc.add_TeacherServicer_to_server(TeacherServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
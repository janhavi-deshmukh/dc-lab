# saved as greeting-server.py
from shutil import copymode
from urllib.request import FancyURLopener
import Pyro5.api

import mysql.connector

# MySQL database configuration
host = "localhost"
user = "springstudent"
password = "springstudent"
database = "dc_exp2"


@Pyro5.api.expose
class CourseDAO(object):
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

    
    def insert(self, name='name', code='code', faculty=1):
        try:
            self.cursor.execute(f'insert into course (course_name, course_code, faculty) values ("{name}", "{code}", {faculty})')
            self.connection.commit()
            return f'Course inserted with ID {self.cursor.lastrowid}'
        except mysql.connector.errors.ProgrammingError as e:
            return e.msg
    
    def show_all(self, faculty=1):
        self.cursor.execute(f'select course_id, course_name, course_code from course where faculty={faculty}')
        result = []
        for row in self.cursor:
            result.append({'course_id': row[0], 'course_name': row[1], 'course_code': row[2]})
        return result
    
    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

daemon = Pyro5.server.Daemon()         # make a Pyro daemon
ns = Pyro5.api.locate_ns()             # find the name server
uri = daemon.register(CourseDAO)   # register the greeting maker as a Pyro object
ns.register("rmi.CourseDAO", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls
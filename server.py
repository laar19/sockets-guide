import socket
import pickle

from _thread import *

from library.functions import *
from library.employee import Employee

ServerSocket = socket.socket()
host         = "127.0.0.1"
port         = 62000
ThreadCount  = 0

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print("Waiting for Connections...")
ServerSocket.listen(5)

def threaded_client(connection):
    connection.send(str.encode("Welcome to the Server"))
    
    while True:
        data   = connection.recv(1024)
        option = pickle.loads(data)["option"]
        data   = pickle.loads(data)["data"]

        # Store employee
        if option == 1:
            employee = Employee(data["ci"], data["name"], data["age"], data["position"])

            # If the employee is not registered then we store it
            if employee.store():
                reply = "Registration succefull!!\n"
            else:
                reply = "ERROR. Employee already registered\n"
        # Take the survey
        elif option == 2:
            global employee_
            employee_ = Employee(data["ci"])

            # If the employee has not taked it
            if employee_.registered():
                if employee_.check_filled_survey():
                    reply = 2
                else:
                    reply = 0
            else:
                reply = 1
        elif option == 3:
            employee_.save_answers(employee_.ci, data)
            reply = "Answers stored. Thank you for your time!!"
        
        if not data:
            break
            
        connection.sendall(str.encode(str(reply)))
        
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print("Thread Number: " + str(ThreadCount))
ServerSocket.close()

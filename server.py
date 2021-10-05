import socket
import pickle
import json
import sys

from _thread  import *
from datetime import date

from library.employee  import Employee

# Load config file
with open("config.json", "r") as config_file:
    config_file = config_file.read()
config_file     = json.loads(config_file)
user_timeout    = int(config_file["user_timeout"])    # User timeout fill survey
display_timeout = int(config_file["display_timeout"]) # Display results
opening_date    = config_file["opening_date"]         # Opening date
date_timeout    = config_file["date_timeout"]         # Date tomeout

"""
date_timeout = date(date_timeout[0], date_timeout[1], date_timeout[2])
if date.today() > date_timeout:
    sys.exit("")
"""

ServerSocket = socket.socket()
host         = "127.0.0.1"
port         = 62000
ThreadCount  = 0

def threaded_client(connection):
    #connection.send(str.encode("Welcome to the Server"))
    data = {"user_timeout": user_timeout, "display_timeout": display_timeout}
    data = pickle.dumps(data)
    connection.send(data)
    
    while True:
        data   = connection.recv(1024)
        option = pickle.loads(data)["option"]
        data   = pickle.loads(data)["data"]

        # Store the employee
        if option == str(1):
            employee = Employee(data["ci"], data["name"], data["age"], data["position"])

            # If the employee is not registered then we store it
            if employee.store():
                reply = "Registration succesfull!!\n"
            else:
                reply = "ERROR. Employee already registered\n"
                
        # Take the survey
        elif option == str(2):
            global employee_
            employee_ = Employee(data["ci"])

            # If the employee is registered
            if employee_.registered():
                if employee_.check_filled_survey():
                    # Employee already filled the survey
                    reply = 2
                else:
                    # Employee has not filled the survey
                    reply = 0

            # If the employee is not registered
            else:
                reply = 1

        # Get the answers of the survey
        elif option == str(3):
            employee_.save_answers(employee_.ci, data)
            reply = "\nAnswers stored. Thank you for your time!!"
        
        if not data:
            break
            
        connection.sendall(str.encode(str(reply)))
        
    connection.close()

if __name__ == "__main__":
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print("Waiting for Connections...")
    ServerSocket.listen(5)

    while True:
        Client, address = ServerSocket.accept()
        print("Connected to: " + address[0] + ":" + str(address[1]))
        start_new_thread(threaded_client, (Client, ))
        ThreadCount += 1
        print("Thread Number: " + str(ThreadCount))
    ServerSocket.close()

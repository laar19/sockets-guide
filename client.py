import socket
import os
import sys

from library.functions import survey, send_data

ClientSocket = socket.socket()
host         = "127.0.0.1"
port         = 62000

try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))
try:
    Response = ClientSocket.recv(1024)
except OSError:
    os.system("cls" if os.name == "nt" else "clear")
    sys.exit("ERROR. The survey is not available at this time")

while True:
    Input = int(input("1) Register.\n2) Take the survey.\n"))

    if Input == 1:
        ci       = input("Ci: ")       # ID (cédula de identidad)
        name     = input("Name: ")     # Full name
        age      = input("Age: ")      # Age
        position = input("Position: ") # Position

        data = {"ci": ci, "name": name, "age": age, "position": position}
        """
        data = {"option": Input, "data": data}
        data = pickle.dumps(data)
        ClientSocket.send(data)
        """
        send_data(ClientSocket, Input, data)

        Response = ClientSocket.recv(1024)
        print(Response.decode("utf-8"))
    elif Input == 2:
        ci = input("Ci: ") # ID (cédula de identidad)

        data = {"ci": ci}
        """
        data = {"option": Input, "data": data}
        data = pickle.dumps(data)
        ClientSocket.send(data)
        """
        send_data(ClientSocket, Input, data)
        
        Response = ClientSocket.recv(1024)
        if int(Response.decode("utf-8")) == 0:
            answers = survey()
            send_data(ClientSocket, 3, answers)
        elif int(Response.decode("utf-8")) == 1:
            os.system("cls" if os.name == "nt" else "clear")
            print("ERROR. You must register first in order to take the survey\n")
        else:
            os.system("cls" if os.name == "nt" else "clear")
            print("ERROR. You already filled this survey\n")
    else:
        os.system("cls" if os.name == "nt" else "clear")
        print("ERROR. Wrong option!!\n")

ClientSocket.close()

import socket
import os
import sys
import time
import pickle

from library.functions import survey, send_data, get_input

ClientSocket = socket.socket()
host         = "127.0.0.1"
port         = 62000

if __name__ == "__main__":
    try:
        ClientSocket.connect((host, port))
    except socket.error as e:
        print(str(e))
    try:
        Response = ClientSocket.recv(1024)
    except OSError:
        os.system("cls" if os.name == "nt" else "clear")
        sys.exit("ERROR. Survey not available at this time")
    user_timeout    = pickle.loads(Response)["user_timeout"]
    display_timeout = pickle.loads(Response)["display_timeout"]

    while True:
        # Main menu
        Input = input("1) Register.\n2) Take the survey.\n")

        # Register
        if Input == str(1):
            # Get data
            ci       = get_input("Ci      : ", int) # ID (cédula de identidad)
            name     = get_input("Name    : ", str) # # Full name
            age      = get_input("Age     : ", int) # Age
            position = get_input("Position: ", str) # Position

            # Prepare data and send it
            data = {"ci": ci, "name": name, "age": age, "position": position}
            send_data(ClientSocket, str(Input), data)

            # Get reply from server
            Response = ClientSocket.recv(1024)
            os.system("cls" if os.name == "nt" else "clear")
            print(Response.decode("utf-8"))

        # Take the survey
        elif Input == str(2):
            # Get data
            os.system("cls" if os.name == "nt" else "clear")
            print("You have {} minutes to complete the survey\nonce your CI is checked!!\n".format(user_timeout/60))
            ci = get_input("Ci: ", int) # ID (cédula de identidad)

            # Prepare data and send it
            data = {"ci": ci}
            send_data(ClientSocket, str(Input), data)

            # Get reply from server
            Response = ClientSocket.recv(1024)

            # If haven't respond the survey before
            if int(Response.decode("utf-8")) == 0:
                answers = survey(user_timeout)
                send_data(ClientSocket, str(3), answers)

                Response = ClientSocket.recv(1024)
                print(Response.decode("utf-8"))
                
                print("\nSystem will exit automaticaly in 3 seconds\n")
                time.sleep(3)
                sys.exit()

            # If hasen't registered yet
            elif int(Response.decode("utf-8")) == 1:
                os.system("cls" if os.name == "nt" else "clear")
                print("ERROR. You must register first in order to take the survey\n")

            # If already filled the survey
            else:
                os.system("cls" if os.name == "nt" else "clear")
                print("ERROR. You already filled this survey\n")

        # Wrong option
        else:
            os.system("cls" if os.name == "nt" else "clear")
            print("ERROR. Wrong option!!\n")

    ClientSocket.close()

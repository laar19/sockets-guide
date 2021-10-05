import random
import os
import pickle
import time
import sys
import trace
import threading

import pandas as pd

# Colums of the .csv file ("database")
columns = {
    "ci"           : int, # ID (cédula de identidad)
    "name"         : str, # Full name
    "age"          : int, # Age
    "position"     : str, # Position
    "survey_filled": int, # If the employee filled the survey
    "token"        : str, # Token
    "question1"    : str, # Question 1
    "question2"    : str, # Question 2
    "question3"    : str, # Question 3
    "question4"    : str, # Question 4
    "question5"    : str  # Question 5
}

# Thread management
class thread_with_trace(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == "call":
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == "line":
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True

# Retrieve current .csv file where employees are stored, if exist
def get_database():
    csvfile = pd.read_csv("employees.csv", encoding="utf-8",
        dtype=columns)

    return csvfile

# Question of the survey
def survey(user_timeout):
    questions_list = {}
    questions_list["question1"] = ["Question: What is your current position?", None]
    questions_list["question2"] = ["Question: Are you happy with your current position?", None]
    questions_list["question3"] = ["Question: Do you like apply for other position?", None]
    questions_list["question4"] = ["Question: Do you like your working hours?", None]
    questions_list["question5"] = ["Question: Do you like to switch your working hours?", None]

    # Shuffle questions randomly
    key_list = list(questions_list)
    random.shuffle(key_list)
    questions_list2 = {}
    for key in key_list:
        questions_list2[key] = questions_list[key]

    # Countdown thread
    th_countdown = thread_with_trace(target=countdown, args=(user_timeout,))
    # Displays survey thread
    th_display_survey = thread_with_trace(target=display_survey, args=(questions_list2,th_countdown,))

    # Start threads
    th_display_survey.start()
    th_countdown.start()

    while True:
        if not th_countdown.is_alive():
            th_display_survey.kill()
            th_display_survey.join()
            break
            
    show_results(questions_list2)

    return questions_list2

# Display survey to the user
def display_survey(questions_list2, th_countdown_flag):
    for i in questions_list2:
        answer                = str(input(questions_list2[i][0] + "\nAnswer  : "))
        questions_list2[i][1] = "Answer  : " + answer

    th_countdown_flag.kill()
    th_countdown_flag.join()

# Send data to the server
def send_data(ClientSocket, input_, data_):
    # Prepare data
    data = {"option": input_, "data": data_}
    data = pickle.dumps(data)

    # Send data
    ClientSocket.send(data)

# Timeout to fill survey
def countdown(timeout):
    while timeout > 0:
        timeout -= 1
        time.sleep(1)
    os.system("cls" if os.name == "nt" else "clear")
    print("ERROR. Timeout!!")
    print("Press any key to continue")

# Show results
def show_results(questions_list2):
    os.system("cls" if os.name == "nt" else "clear")
    print("Your answers\n")
    for i in questions_list2:
        print("{}\n{}".format(questions_list2[i][0],
            questions_list2[i][1]))

# Return validated input
def get_input(input_, return_type):
    while True:
        try:
            Input = input(input_)
            return return_type(Input)
        except ValueError:
            print("ERROR. Please enter your data correctly!!")

import random
import os
import pickle

import pandas as pd

# Retrieve current .csv file where employees are stored, if exist
def get_database():
    csvfile = pd.read_csv("employees.csv", encoding="utf-8",
        dtype={
            "ci": int,
            "question1": str,
            "question2": str,
            "question3": str,
            "question4": str,
            "question5": str,
        })

    return csvfile

# Question of the survey
def survey():
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

    for i in questions_list2:
        answer                = input(questions_list2[i][0] + "\nAnswer  : ")
        questions_list2[i][1] = "Answer  : " + answer

    os.system("cls" if os.name == "nt" else "clear")
    print("Aswers")
    for i in questions_list2:
        print("{}\n{}".format(questions_list2[i][0],
            questions_list2[i][1]))
    return questions_list2

def send_data(ClientSocket, input_, data_):
    data = {"option": input_, "data": data_}
    data = pickle.dumps(data)
    ClientSocket.send(data)

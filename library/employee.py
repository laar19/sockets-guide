import pandas as pd

from library.functions import *

class Employee:
    def __init__(self, ci=None, name=None, age=None, position=None,
        survey_filled=1, token=None, question1=None, question2=None,
        question3=None, question4=None, question5=None):
            
        self.ci            = ci            # ID (cédula de identidad)
        self.name          = name          # Full name
        self.age           = age           # Age
        self.position      = position      # Position
        self.survey_filled = survey_filled # If the employee filled the survey
        self.token         = token         # Token
        self.question1     = question1     # Question 1
        self.question2     = question2     # Question 2
        self.question3     = question3     # Question 3
        self.question4     = question4     # Question 4
        self.question5     = question5     # Question 5

    # Check if the employee is already registered
    def registered(self):
        try:
            csvfile = get_database()
        except FileNotFoundError:
            return False
        
        if int(self.ci) in csvfile["ci"].values:
            return True
        return False

    # Check if the employee filled the survey
    def check_filled_survey(self):
        csvfile = get_database()

        employee = csvfile.loc[csvfile["ci"] == int(self.ci)]
        exist    = employee["survey_filled"] == 0
        if exist.bool():
            return True
        return False

    # Register a new employee
    def store(self):
        df = pd.DataFrame([
            [
                self.ci,
                self.name,
                self.age,
                self.position,
                self.survey_filled,
                self.token,
                self.question1,
                self.question2,
                self.question3,
                self.question4,
                self.question5
            ]
        ], columns=list(columns.keys()))

        # If the .csv file where employees are stored does not exist
        # then a new one is created
        try:
            csvfile = get_database()
            if self.registered():
                return False

            csvfile = csvfile.append(df, sort=False)
            csvfile.to_csv(r"employees.csv", index=False)
        except FileNotFoundError:
            csvfile = pd.DataFrame(columns=columns)
            csvfile = csvfile.append(df, sort=False)
            csvfile.to_csv(r"employees.csv", index=False)

            return True

    # Save answers into "database"
    def save_answers(self, ci, data):
        csvfile = get_database()

        # Find the stored information of the employee
        employee = csvfile.loc[csvfile["ci"] == int(ci)]

        # Get the row in order to delete it
        row = employee.index[employee["ci"] == int(ci)].tolist()[0]
        csvfile.drop(row, inplace=True)

        # Store the answers
        key = "question"
        for i in range(1, 6):
            employee.at[row, key+str(i)] = data[key+str(i)]

        # Change status of the employee
        employee.at[row, "survey_filled"] = 0

        # Update "database"
        csvfile = csvfile.append(employee, sort=False)
        csvfile.to_csv(r"employees.csv", index=False)

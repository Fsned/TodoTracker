from tkinter import *
import json
import datetime

window = Tk()
window.geometry('400x1000')

def createTaskEntriesFromJson(date):
    # This function looks up the taskDictionary.json, 
    # and creates a label in the UI for each entry
    a = 1


def addTaskToDictionary(date, task):
    # Add a new task to the dictionary
    a = 1


def removeTaskFromDictionary(date, task):
    # This function removes a task from the dictionary
    a = 1


currentDate = datetime.datetime.now()

dateLabel = Label(window, text=str(currentDate.strftime('%d/%m - %Y')))
previousDateButton = Button(window, text='<')
nextDateButton = Button(window, text='>')


dateLabel.pack()

pageButtons = {}



Label(window, text='Create new task').pack()

window.mainloop()
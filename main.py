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

dateLabel = Label(window, text=str(currentDate.strftime('%d/%m - %Y')), font='arial 15 bold')
dateLabel.place(x=140, y=10)
previousDateButton = Button(window, text='<')
nextDateButton = Button(window, text='>')

previousDateButton.place(x = 80, y = 10)
nextDateButton.place(x = 280, y = 10)




createTaskLabel = Label(window, text='Create new task', font = 'arial 13')
createTaskLabel.place(x=10, y=50)

newTaskHeadline = Entry(window, width= 32)
newTaskDescription = Entry(window, width = 32)

newTaskHeadline.place(x = 10, y = 80)
newTaskDescription.place( x = 10, y = 105)

window.mainloop()
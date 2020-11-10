from tkinter import *
import json
import datetime

window = Tk()
window.geometry('350x1000')

currentDate = datetime.datetime.now()
dateLabel = Label(window, text=str(currentDate.strftime('%d/%m - %Y')), font='arial 15 bold')
dateLabel.place(x=140, y=10)

taskLabels = {}
tasks = {}

def createTaskEntriesFromJson(date):
    # This function looks up the taskDictionary.json, 
    # and creates a label in the UI for each entry
    global taskLabels
    global tasks

    for a in taskLabels:
        taskLabels[a].destroy()
        tasks[a].destroy()

    with open('./taskDictionary.json', 'r') as taskDictionaryFile:
        taskDictionary = json.loads(taskDictionaryFile.read())
        
    for a in taskDictionary:
        if (str(a) == str(date.strftime('%d/%m - %Y'))):
            todaysTasks = taskDictionary[a]
            for enum, b in enumerate(todaysTasks):
                taskLabels[b] = Label(window, text='-', font = 'arial 14 bold')
                taskLabels[b].place(x = 10, y = 150 + (30*int(enum)))

                tasks[b] = Label(window, text=todaysTasks[b]['taskName'], font = 'arial 14')
                tasks[b].place(x = 110, y = 150 + (30*int(enum)))
            break


def addTaskToDictionary(date, taskName, taskDescription):
    # Add a new task to the dictionary
    #global currentDate

    with open('./taskDictionary.json', 'r') as taskDictionaryFile:
        taskDictionary = json.loads(taskDictionaryFile.read())

    print("TaskDictionary: " + str(taskDictionary))
    print("Date: " + str(date.strftime('%d/%m - %Y')))
    print(taskDictionary[date.strftime('%d/%m - %Y')])

    taskDictionary[date.strftime('%d/%m - %Y')][str(taskDictionary[date.strftime('%d/%m - %Y')].__len__())] = {
        'taskName': taskName,
        'taskDescription': taskDescription
    }

    #print(taskDictionary[date.strftime('%d/%m - %Y')])
    
    with open('./taskDictionary.json', 'w') as taskDictionaryFile:
        json.dump(taskDictionary, taskDictionaryFile)

    createTaskEntriesFromJson(currentDate)

def removeTaskFromDictionary(date, task):
    # This function removes a task from the dictionary
    a = 1


def changePage(date, deltaDays):
    global currentDate
    currentDate = date + datetime.timedelta(days=deltaDays)
    createTaskEntriesFromJson(currentDate)
    dateLabel.configure(text=str(currentDate.strftime('%d/%m - %Y')))
    createTaskEntriesFromJson(currentDate)


newTaskHeadlineVar = StringVar()
newTaskDescriptionVar = StringVar()

previousDateButton = Button(window, text='<', command=lambda : changePage(currentDate, -1))
nextDateButton = Button(window, text='>', command=lambda : changePage(currentDate, 1))
addTaskButton = Button(window, text='Add', command=lambda : addTaskToDictionary(currentDate, newTaskHeadlineVar.get(), newTaskDescriptionVar.get()), width = 6)
addTaskButton.place(x = 274, y = 75)

previousDateButton.place(x = 80, y = 10)
nextDateButton.place(x = 280, y = 10)

createTaskEntriesFromJson(currentDate)

createTaskLabel = Label(window, text='Create new task', font = 'arial 13')
createTaskLabel.place(x=10, y=50)

newTaskHeadline = Entry(window, width= 25, justify=LEFT, textvariable=newTaskHeadlineVar)
newTaskDescription = Entry(window, width = 37, textvariable=newTaskDescriptionVar)

newTaskHeadlineLabel = Label(window, text='Task name', justify=LEFT)
newTaskHeadlineLabel.place(x=10, y = 80)

newTaskDescriptionLabel = Label(window, text='Task description')
newTaskDescriptionLabel.place(x = 10, y = 110)

newTaskHeadline.place(x = 100, y = 80)
newTaskDescription.place( x = 100, y = 110)

window.mainloop()
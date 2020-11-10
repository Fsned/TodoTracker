from tkinter import *
import json
import datetime

window = Tk()
window.geometry('365x600')
#window.configure(bg='gray15')

def renderTasksToUI(date, frame, taskState):
    # This function looks up the taskDictionary.json, 
    # and creates a label in the UI for each entry
    global taskLabels
    global tasks

    global taskCompleteButtons
    global taskRemoveButtons

    for a in taskLabels:
        taskLabels[a].destroy()
    for a in tasks:
        tasks[a].destroy()

    for a in taskCompleteButtons:
        taskCompleteButtons[a].destroy()
        taskRemoveButtons[a].destroy()

    with open('./taskDictionary.json', 'r') as taskDictionaryFile:
        taskDictionary = json.loads(taskDictionaryFile.read())
    
    
    if (taskDictionary.get(date, None)) == None or (taskDictionary.get(date, None)) == {}:
        taskLabels['0'] = Label(window, text='No tasks, dance party!', font = 'arial 14 bold')
        taskLabels['0'].place(x = 10, y = 150)

    else:

        TASK_START_AT_Y = 45
        TASK_OFFSET_Y = 30

        bulletChar = '\u2219'

        doneTasks = 0
        todoTasks = 0

        todoFrame = Frame(window, height = 40, width = 365)
        todoFrame.pack_propagate(1)
        todoFrame.grid(row=2)

        todoFrame.place(x = 10, y = 150)
        
    
        doneFrame = Frame(window, height = 40, width = 365)
        doneFrame.pack_propagate(1)
        doneFrame.grid(row=3)
        doneFrame.place(x = 10, y = 300)

        doneLabel = Label(doneFrame, text = 'Done tasks', font = 'arial 16 bold')
        doneLabel.pack(side=LEFT)

        
        for enum, b in enumerate(taskDictionary[date]):
            if taskDictionary[date][b]['Done'] == False:
                print ("Making label!" + str(enum))
                if enum == 1:
                    toDoLabel = Label(todoFrame, text = 'To Do', font = 'arial 16 bold')
                    toDoLabel.grid(row = 0, column = 0)

            
                taskLabels[b] = Label(todoFrame, text=bulletChar, font = 'arial 14 bold')
                taskLabels[b].grid(row = enum, column = 0)

                tasks[b] = Label(todoFrame, text=taskDictionary[date][b]['taskName'], font = 'arial 14', justify=LEFT, bg='red')
                tasks[b].grid(row = enum, column = 2)

                taskCompleteButtons[b] = Button(todoFrame, text='\u2713', font='arial 8', width = 1, command = lambda b=b: completeTask(date, b))
                taskCompleteButtons[b].grid(row = enum, column = 3, sticky=E)

                taskRemoveButtons[b] = Button(todoFrame, text='\u274C', font='arial 8', width = 1, command = lambda b=b: removeTaskFromDictionary(date, b))
                taskRemoveButtons[b].grid(row = enum, column = 4, sticky=E)

            #taskLabels[b] = Label(frame, text=bulletChar, font = 'arial 14 bold')
            #taskLabels[b].place(x = 10, y = TASK_START_AT_Y + (TASK_OFFSET_Y*int(enum)))
#
            #tasks[b] = Label(frame, text=taskDictionary[date][b]['taskName'], font = 'arial 14')
            #tasks[b].place(x = 30, y = TASK_START_AT_Y + (TASK_OFFSET_Y*int(enum)))
#
            #taskCompleteButtons[b] = Button(frame, text='\u2713', font='arial 8', width = 1, command = lambda b=b: completeTask(date, b))
            #taskCompleteButtons[b].place(x=290, y = TASK_START_AT_Y + (TASK_OFFSET_Y*int(enum)))
#
            #taskRemoveButtons[b] = Button(frame, text='\u274C', font='arial 8', width = 1, command = lambda b=b: removeTaskFromDictionary(date, b))
            #taskRemoveButtons[b].place(x=325, y = TASK_START_AT_Y + (TASK_OFFSET_Y*int(enum)))





def addTaskToDictionary(date, taskName, taskDescription):
    if newTaskHeadlineVar.get() == '':
        return

    newTaskHeadlineVar.set('')
    newTaskDescriptionVar.set('')
        
    with open('./taskDictionary.json', 'r') as taskDictionaryFile:
        taskDictionary = json.loads(taskDictionaryFile.read())

    if taskDictionary.get(date, None) == None:
        taskDictionary[date] = {}

    taskDictionary[date][str(taskDictionary[date].__len__())] = {
        'taskName': taskName,
        'taskDescription': taskDescription,
        'Done': False
    }
    
    with open('./taskDictionary.json', 'w') as taskDictionaryFile:
        json.dump(taskDictionary, taskDictionaryFile)

    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), doneFrame, True)
    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), todoFrame, False)






def removeTaskFromDictionary(date, task):
    
    with open('./taskDictionary.json', 'r') as taskDictionaryFile:
        taskDictionary = json.loads(taskDictionaryFile.read())

    taskDictionary[date].pop(str(task))

    if taskDictionary[date].__len__() == 0:
        del taskDictionary[date]

    with open('./taskDictionary.json', 'w') as taskDictionaryFile:
        json.dump(taskDictionary, taskDictionaryFile)

    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), doneFrame, True)
    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), todoFrame, False)



def completeTask(date, task):
    with open('./taskDictionary.json', 'r') as taskDictionaryFile:
        taskDictionary = json.loads(taskDictionaryFile.read())

    taskDictionary[date][task]['Done'] = True

    with open('./taskDictionary.json', 'w') as taskDictionaryFile:
        json.dump(taskDictionary, taskDictionaryFile)


def changePage(deltaDays):
    global currentDate

    currentDate += datetime.timedelta(days=deltaDays)
    dateLabel.configure(text=str(currentDate.strftime('%d/%m - %Y')))
    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), doneFrame, True)
    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), todoFrame, False)


currentDate = datetime.datetime.now()

taskLabels = {}
tasks = {}
taskCompleteButtons = {}
taskRemoveButtons = {}

newTaskHeadlineVar = StringVar()
newTaskDescriptionVar = StringVar()

################################################################################################################
#   HEADER FRAME
# used for the current date and next/previous date buttons

headerFrame = Frame(window, width = 365, height = 20)
headerFrame.pack_propagate(1)
headerFrame.grid(row = 0)

previousDateButton = Button(headerFrame, text='<', command=lambda : changePage(-1))#, bg = 'gray15', fg = 'snow', activebackground = 'gray15', activeforeground = 'snow')
previousDateButton.pack(side=LEFT)
dateLabel = Label(headerFrame, text=str(currentDate.strftime('%d/%m - %Y')), font='arial 15 bold')#, bg = 'gray15', fg = 'snow', activebackground = 'gray15', activeforeground = 'snow')
dateLabel.pack(side=LEFT)
nextDateButton = Button(headerFrame, text='>', command=lambda : changePage(1))#, bg = 'gray15', fg = 'snow', activebackground = 'gray15', activeforeground = 'snow')
nextDateButton.pack(side=LEFT)

################################################################################################################
#   Headline FRAME
# used for a single headline
headlineFrame = Frame(window, width=365, height = 20)
#headlineFrame.pack_propagate(1)
headlineFrame.grid(row = 1)

createTaskLabel = Label(headlineFrame, text='Create new task', font = 'arial 13', width=15)
createTaskLabel.grid(column = 0)

################################################################################################################
#   Input FRAME
# used for all inputs and related labels
inputFrame = Frame(window, width = 365, height = 20)
inputFrame.grid(row = 2)

newTaskHeadlineLabel = Label(inputFrame, text='Task name', justify=LEFT)
newTaskHeadlineLabel.grid(row = 0, sticky = W)

newTaskDescriptionLabel = Label(inputFrame, text='Description')
newTaskDescriptionLabel.grid(row = 1, sticky = W)

newTaskHeadline = Entry(inputFrame, textvariable=newTaskHeadlineVar)
newTaskHeadline.grid(row = 0, column = 1, columnspan=2)

newTaskDescription = Entry(inputFrame, textvariable=newTaskDescriptionVar)
newTaskDescription.grid(row = 1, column = 1, columnspan=2)

addTaskButton = Button(inputFrame, text='Add', command=lambda : addTaskToDictionary(currentDate.strftime('%d/%m - %Y'), newTaskHeadlineVar.get(), newTaskDescriptionVar.get()), width = 6)
addTaskButton.grid(row = 1, column = 4, rowspan = 1, sticky = W+E+N+S)

################################################################################################################
#   Input FRAME
# used for all inputs and related labels
todoFrame = Frame(window, width = 365, height = 20, bg = 'yellow')
todoFrame.grid()

renderTasksToUI(currentDate.strftime('%d/%m - %Y'), doneFrame, False)

################################################################################################################
#   Input FRAME
# used for all inputs and related labels
doneFrame = Frame(window, width = 365, height = 20, bg = 'blue')
doneFrame.grid()

renderTasksToUI(currentDate.strftime('%d/%m - %Y'), doneFrame, True)

#renderTasksToUI(currentDate.strftime('%d/%m - %Y'))


window.mainloop()
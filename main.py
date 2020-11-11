from tkinter import *
import json
import datetime

window = Tk()
window.geometry('365x600')

def renderTasksToUI(date, frame, taskState):
    # This function looks up the taskDictionary.json, 
    ## and creates a label in the UI for each entry

    # Destroy all widgets in the current frame
    for widget in frame.winfo_children():
       widget.destroy()


    with open('./taskDictionary.json', 'r') as taskDictionaryFile:
        taskDictionary = json.loads(taskDictionaryFile.read())

    if taskDictionary.get(date, None) == None:
        taskDictionary[date] = {}

    elif taskDictionary.get(date, None).__len__() == 0:
        for widget in frame.winfo_children():
            widget.destroy()

    else:
        if taskState == True:
            doneLabel = Label(frame, text = 'Done tasks', font = 'arial 16 bold')
            doneLabel.grid(row = 0, column = 0, columnspan = 7) 
        
        elif taskState == False:
            todoLabel = Label(frame, text = 'ToDo', font = 'arial 16 bold')
            todoLabel.grid(row = 0, column = 0, columnspan = 7)

        for enum, b in enumerate(taskDictionary[date]):
            if taskDictionary[date][b].get('Done', None) == taskState:
                Label(frame, text='\u2219' + taskDictionary[date][b]['taskName'], font = 'arial 14', justify=LEFT).grid(row = enum+1, column = 0, columnspan = 5, sticky=N+S+E+W)
                Button(frame, text='\u2713', font='arial 8', width = 1, command = lambda b=b: completeTask(date, b)).grid(row = enum+1, column = 6, sticky=E)
                Button(frame, text='\u274C', font='arial 8', width = 1, command = lambda b=b: removeTaskFromDictionary(date, b)).grid(row = enum+1, column = 7, sticky=E)

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
    

    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), todoFrame, False)
    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), doneFrame, True)



def changePage(deltaDays):
    global currentDate

    if deltaDays == "startup":
        currentDate = datetime.datetime.now()
        
        with open('./taskDictionary.json', 'r') as taskDictionaryFile:
            taskDictionary = json.loads(taskDictionaryFile.read())

        
        if taskDictionary.get(currentDate.strftime('%d/%m - %Y'), None) == None:
            taskDictionary[currentDate.strftime('%d/%m - %Y')] = {}

        with open('./taskDictionary.json', 'w') as taskDictionaryFile:
            json.dump(taskDictionary, taskDictionaryFile)

        return

    currentDate += datetime.timedelta(days=deltaDays)
    dateLabel.configure(text=str(currentDate.strftime('%d/%m - %Y')))
    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), doneFrame, True)
    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), todoFrame, False)


changePage("startup")

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
#   todo FRAME
# used for all inputs and related labels
todoFrame = Frame(window, width = 365, height = 20)
todoFrame.grid_propagate(1)
todoFrame.grid()



################################################################################################################
#   done FRAME
# used for all inputs and related labels
doneFrame = Frame(window, width = 365, height = 20)
doneFrame.grid_propagate(1 )
doneFrame.grid()

renderTasksToUI(currentDate.strftime('%d/%m - %Y'), todoFrame, False)
renderTasksToUI(currentDate.strftime('%d/%m - %Y'), doneFrame, True)

window.mainloop()
from tkinter import *
import json
import datetime

window = Tk()
window.geometry('360x600')
window.iconphoto(False, PhotoImage(file='./icon.png'))
window.title('To-Do Tracker')


def renderTasksToUI(date, frames):
    # Destroy all widgets in both frames
    for frame in frames:
        for widget in frames[frame].winfo_children():
            widget.destroy()

    Label(frames['0'], text = 'ToDo', font = 'arial 16 bold').grid(row = 0, column = 0, columnspan = 7)
    Label(frames['1'], text = 'Done tasks', font = 'arial 16 bold').grid(row = 0, column = 0, columnspan = 7)

    with open('./taskDictionary.json', 'r') as taskDictionaryFile:
        taskDictionary = json.loads(taskDictionaryFile.read())

    if taskDictionary.get(date, None) == None:
        taskDictionary[date] = {}
        
        for frame in frames:
            for widget in frames[frame].winfo_children():
                widget.destroy()
        
        Label(frames['0'], text = 'No tasks, dance party!', font = 'arial 16 bold').grid(row = 2)

    elif taskDictionary.get(date, None).__len__() == 0:
        for frame in frames:
            for widget in frames[frame].winfo_children():
                widget.destroy()
        
        Label(frames['0'], text = 'No tasks, dance party!', font = 'arial 16 bold').grid(row = 2)
    
    else:
        for enum, task in enumerate(taskDictionary[date]):
            if taskDictionary[date][task]['Done'] == True:
                frame = '1'
                doneChar = '\u2191'
            else:
                frame = '0'
                doneChar = '\u2713'

            Label(frames[frame], text='\u2023' + taskDictionary[date][task]['taskName'], font = 'arial 14', justify=CENTER, wraplength = 280   ).grid(row = enum+1, column = 0, columnspan = 5, sticky=N+S+E+W)
            Button(frames[frame], text=doneChar, font='arial 8', width = 1, command = lambda b=task: completeTask(date, b)).grid(row = enum+1, column = 6, sticky=E)
            Button(frames[frame], text='\u274C', font='arial 8', width = 1, command = lambda b=task: removeTaskFromDictionary(date, b)).grid(row = enum+1, column = 7, sticky=E)    


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

    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), taskFrames)


def removeTaskFromDictionary(date, task):
    
    with open('./taskDictionary.json', 'r') as taskDictionaryFile:
        taskDictionary = json.loads(taskDictionaryFile.read())

    taskDictionary[date].pop(str(task))

    if taskDictionary[date].__len__() == 0:
        del taskDictionary[date]

    with open('./taskDictionary.json', 'w') as taskDictionaryFile:
        json.dump(taskDictionary, taskDictionaryFile)

    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), taskFrames)


def completeTask(date, task):
    with open('./taskDictionary.json', 'r') as taskDictionaryFile:
        taskDictionary = json.loads(taskDictionaryFile.read())

    taskDictionary[date][task]['Done'] = not taskDictionary[date][task]['Done']

    with open('./taskDictionary.json', 'w') as taskDictionaryFile:
        json.dump(taskDictionary, taskDictionaryFile)
    
    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), taskFrames)


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
    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), taskFrames)

changePage("startup")

newTaskHeadlineVar = StringVar()
newTaskDescriptionVar = StringVar()

################################################################################################################
#   HEADER FRAME
# used for the current date and next/previous date buttons
    
headerFrame = Frame(window, width = 365, height = 20)
headerFrame.pack_propagate(1)
headerFrame.grid(row = 0, columnspan = 4)

Button(headerFrame, text='<', command=lambda : changePage(-1)).grid(row = 0, column = 0)#, bg = 'gray15', fg = 'snow', activebackground = 'gray15', activeforeground = 'snow')
dateLabel = Label(headerFrame, text=str(currentDate.strftime('%d/%m - %Y')), font='arial 15 bold')
dateLabel.grid(row = 0, column = 1)
Button(headerFrame, text='>', command=lambda : changePage(1)).grid(row = 0, column = 2)

################################################################################################################
#   Input & etc FRAME
# used for a single headline
inputFrame = LabelFrame(window, width = 365, height = 20, text = 'Create new task')
inputFrame.grid(row = 1, columnspan = 8)

Label(inputFrame, text='Task name', justify=LEFT).grid(row = 0, sticky = W)
Label(inputFrame, text='Description').grid(row = 1, sticky = W)
Entry(inputFrame, textvariable=newTaskHeadlineVar).grid(row = 0, column = 1, columnspan=2)
Entry(inputFrame, textvariable=newTaskDescriptionVar).grid(row = 1, column = 1, columnspan=2)
Button(inputFrame, text='Add', command=lambda : addTaskToDictionary(currentDate.strftime('%d/%m - %Y'), newTaskHeadlineVar.get(), newTaskDescriptionVar.get()), width = 6).grid(row = 1, column = 4, rowspan = 1, sticky = W+E+N+S)

taskFrames = {}
######################################################
#   ['0'] == todoFrame      #      ['1'] == doneFrame
for a in range(2):
    taskFrames[str(a)] = Frame(window, width = 365, height = 20)
    taskFrames[str(a)].grid_propagate(1)
    taskFrames[str(a)].grid()

    spaceFrame = Frame(window, width = 365, height = 100)
    spaceFrame.grid_propagate(0)
    spaceFrame.grid()

renderTasksToUI(currentDate.strftime('%d/%m - %Y'), taskFrames)

window.mainloop()
from tkinter import *
import json
import datetime

window = Tk()
window.geometry('360x1060')
window.iconphoto(False, PhotoImage(file='./icon.png'))
window.title('To-Do Tracker')

def readDictionary():
    with open('./taskDictionary.json', 'r') as taskDictionaryFile:
        taskDictionary = json.loads(taskDictionaryFile.read())
    return taskDictionary
    
def writeDictionary(dictionary):
    with open('./taskDictionary.json', 'w') as taskDictionaryFile:
        json.dump(dictionary, taskDictionaryFile)
    return


def renderTasksToUI(date, frames):
    # Destroy all widgets in both frames
    for frame in frames:
        for widget in frames[frame].winfo_children():
            widget.destroy()

    Label(frames['0'], text = 'ToDo', font = 'arial 16 bold').grid(row = 0, column = 0, columnspan = 7)
    Label(frames['1'], text = 'Done tasks', font = 'arial 16 bold').grid(row = 0, column = 0, columnspan = 7)

    taskDictionary = readDictionary()

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

            Label(frames[frame], text = taskDictionary[date][task]['taskName'], font = 'arial 10', justify=LEFT, wraplength = 280   ).grid(row = enum+1, column = 1, columnspan = 4, sticky=W)
            Button(frames[frame], text=doneChar, font='arial 8', width = 1, command = lambda b=task: completeTask(date, b)).grid(row = enum+1, column = 6, sticky=E)
            Button(frames[frame], text='\u274C', font='arial 8', width = 1, command = lambda b=task: removeTaskFromDictionary(date, b)).grid(row = enum+1, column = 7, sticky=E)    


def toggleTask(date, task):
    taskDictionary = readDictionary()
    taskDictionary[date][task]['Done'] = not taskDictionary[date][task]['Done']
    writeDictionary(taskDictionary)
    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), taskFrames)


def addTaskToDictionary(date, taskName):
    if newTaskHeadlineVar.get() == '':
        return

    newTaskHeadlineVar.set('')
    taskDictionary = readDictionary()

    if taskDictionary.get(date, None) == None:
        taskDictionary[date] = {}

    taskDictionary[date][str(taskDictionary[date].__len__())] = {
        'taskName': taskName,
        'taskDescription': '',
        'Done': False
    }
    
    writeDictionary(taskDictionary)
    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), taskFrames)


def removeTaskFromDictionary(date, task):
    taskDictionary = readDictionary()
    taskDictionary[date].pop(str(task))
    
    if taskDictionary[date].__len__() == 0:
        del taskDictionary[date]

    writeDictionary(taskDictionary)
    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), taskFrames)


def completeTask(date, task):
    taskDictionary = readDictionary()
    taskDictionary[date][task]['Done'] = not taskDictionary[date][task]['Done']
    writeDictionary(taskDictionary)
    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), taskFrames)


def moveTasksToToday():
    today = datetime.datetime.now()
    taskDictionary = readDictionary()

    for a in taskDictionary:
        b = a.split()

        DicDate = datetime.date(year = int(b[2][0:4]), month = int(b[0][-2:]), day = int(b[0][0:2]))
        currDate = datetime.date(year = int(today.strftime('%Y')), month = int(today.strftime('%m')), day = int(today.strftime('%d')))

        if DicDate < currDate:
            for b in taskDictionary[a]:
                if taskDictionary[a][b]['Done'] == False:
                    taskDictionary[currDate.strftime('%d/%m - %Y')][str(taskDictionary[currDate.strftime('%d/%m - %Y')].__len__())] = {
                        'taskName': taskDictionary[a][b]['taskName'],
                        'taskDescription': '',
                        'Done': False
                    }

                    taskDictionary[a][b]['Done'] = True

    writeDictionary(taskDictionary)
    changePage(0)
    renderTasksToUI(today.strftime('%d/%m - %Y'), taskFrames)

                    
        

def changePage(deltaDays):
    global currentDate

    if deltaDays == "startup":
        currentDate = datetime.datetime.now()
        
        taskDictionary = readDictionary()

        if taskDictionary.get(currentDate.strftime('%d/%m - %Y'), None) == None:
            taskDictionary[currentDate.strftime('%d/%m - %Y')] = {}

        writeDictionary(taskDictionary)

        return

    if deltaDays == 0:
        currentDate = datetime.datetime.now()
        taskDictionary = readDictionary()

        if taskDictionary.get(currentDate.strftime('%d/%m - %Y'), None) == None:
            taskDictionary[currentDate.strftime('%d/%m - %Y')] = {}

        writeDictionary(taskDictionary)
        
    currentDate += datetime.timedelta(days=deltaDays)

    dayLabel.configure(text = str(currentDate.strftime('%d')))
    monthLabel.configure(text = str(currentDate.strftime('%b')))
    weekLabel.configure(text = str('W' + currentDate.strftime('%W')))
    yearLabel.configure(text = str(currentDate.strftime('%Y')))

    renderTasksToUI(currentDate.strftime('%d/%m - %Y'), taskFrames)

changePage("startup")

newTaskHeadlineVar = StringVar()

################################################################################################################
#   HEADER FRAME
# used for the current date and next/previous date buttons

headerFrame = Frame(window, width = 365, height = 20)
headerFrame.grid(row = 0, rowspan = 4)

spacerFrame1 = Frame(headerFrame, width = 360, height = 1)
spacerFrame1.grid(row = 0, column = 0, columnspan = 9)

spacerFrame2 = Frame(headerFrame, width = 360, height = 25)
spacerFrame2.grid(row = 5, column = 0, columnspan = 9)

dayLabel = Label(headerFrame, text = str(currentDate.strftime('%d')), font = 'arial 45 bold')
dayLabel.grid(row = 1, rowspan = 4, column = 0, sticky = W)

monthLabel = Label(headerFrame, text = str(currentDate.strftime('%b')), font = 'arial 14 bold')
monthLabel.grid(row = 1, column = 1, sticky = W)

yearLabel = Label(headerFrame, text = str(currentDate.strftime('%Y')), font = 'arial 14 bold')
yearLabel.grid(row = 2, column = 1, sticky = W)

weekLabel = Label(headerFrame, text = str('W' + currentDate.strftime('%W')), font = 'arial 14 bold')
weekLabel.grid(row = 3, column = 1, sticky = W)

prevDayButton = Button(headerFrame, text = '<', font = 'arial 16 bold', command = lambda : changePage(-1), width = 1)
prevDayButton.grid(row = 1, rowspan = 3, column = 5)
toDayButton = Button(headerFrame, text = 'O', font = 'arial 16 bold', command = lambda : changePage(0))
toDayButton.grid(row = 1, rowspan = 3, column = 6)
nextDayButton = Button(headerFrame, text = '>', font = 'arial 16 bold', command = lambda : changePage(1))
nextDayButton.grid(row = 1, rowspan = 3, column = 7)

################################################################################################################
#   Input & etc FRAME
# used for a single headline
inputFrame = LabelFrame(window, width = 365, height = 20, text = 'Create new task')
inputFrame.grid(row = 9, columnspan = 8)

Label(inputFrame, text='Name', justify=LEFT).grid(row = 0, sticky = W)
Entry(inputFrame, textvariable=newTaskHeadlineVar).grid(row = 0, column = 1, columnspan=2)
Button(inputFrame, text='Add', command=lambda : addTaskToDictionary(currentDate.strftime('%d/%m - %Y'), newTaskHeadlineVar.get()), width = 3).grid(row = 0, column = 4, sticky = W)
Button(inputFrame, text='\u27F3', command = lambda : moveTasksToToday()).grid(row = 0, column = 5, sticky = E)

######################################################
#   ['0'] == todoFrame      #      ['1'] == doneFrame

taskFrames = {}
for a in range(2):
    taskFrames[str(a)] = Frame(window, width = 365, height = 20)
    taskFrames[str(a)].grid_propagate(1)
    taskFrames[str(a)].grid()

    spaceFrame = Frame(window, width = 365, height = 100)
    spaceFrame.grid_propagate(0)
    spaceFrame.grid()

renderTasksToUI(currentDate.strftime('%d/%m - %Y'), taskFrames)
window.mainloop()

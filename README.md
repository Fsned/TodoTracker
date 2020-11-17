# TodoTracker

-- BUGS --------

-) 'ToDo' / 'Done tasks' -labels show up when there's just 1 task in either, and e.g. 'Done tasks' should only show if >=1 done tasks exist in current date

-- FEATURES --------
-) add scroller to the window
Tasks tend to pile up and grow out the bottom of the window :( 

  
-) Edit existing tasks
  To be able to correct or add to existing tasks, instead of re-creating
  
-) Calendar view
  I'd like to be able to pop open a small calender (browse months etc) with the following options:
  A) See a colored view (e.g. gray / white) if each day has unfinished tasks in them
  B) Click a day in the month to go to that day
  C) Browse between months
  
-) Popup when clicking a task
  When clicking a task, a window of same size as mainwindow should pop up to the right (sticky to original window) showing the task headline in a headline, and the task description. Similar to when opening a mail in Outlook. In here, could be space for more fields, e.g. 'Deadline', 'Responsible', 'Links', and more.

-) Change ToDo and 'Done'-frames to LabelFrames, and remove the headlines
  if this is done, the frame.winfo_children() can be used to destroy in case no tasks exist in each window:

  if frames[frame].winfo_children == []:
    frames[frame].grid_forget()           <----- maybe?
  
  ----) MAJOR FEATURE: -------- Remake in PyQt5
  PyQt5 seems like the shit regarding GUI in python
 
  


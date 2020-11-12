# TodoTracker

-- BUGS --------

-) 'ToDo' / 'Done tasks' -labels show up when there's just 1 task in either, and e.g. 'Done tasks' should only show if >=1 done tasks exist in current date

-) Add empty frame or label or something to the top of the Done and To Do-frames, to keep the width at max, so button always appear at far right


-- FEATURES --------
-) Fetch unfinished tasks <Button>
  A button to bring unfinished tasks from previous days, up to today would be nice.
  
-) Edit existing tasks
  To be able to correct or add to existing tasks, instead of re-creating
  
-) Return to current date
  In case i swapped a lot of pages around, and forgot (or got far away) from the current date, i'd like to be able to click a 'return' button or similar to with one click go back to today.
  
-) Calendar view
  I'd like to be able to pop open a small calender (browse months etc) with the following options:
  A) See a colored view (e.g. gray / white) if each day has unfinished tasks in them
  B) Click a day in the month to go to that day
  C) Browse between months
  

-) Change ToDo and 'Done'-frames to LabelFrames, and remove the headlines
  if this is done, the frame.winfo_children() can be used to destroy in case no tasks exist in each window:

  if frames[frame].winfo_children == []:
    frames[frame].grid_forget()           <----- maybe?
  
  ----) MAJOR FEATURE: -------- Remake in PyQt5
  PyQt5 seems like the shit regarding GUI in python
 
  


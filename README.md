This is intended to be a lightweight, efficient, and useful task management tool that is entirely terminal-based. To use, create a planner folder in the Applications directory and copy the two files given here into the newly created folder. Then, open terminal and run 

```
$ vim ~/.bashrc
```

and append these two lines at the end of the code:

```
alias plan="python3 /Applications/planner/planner.py"
alias notifiction="python3 /Applications/planner/notification &"
```

Now, you can type "plan" from any working directory in the terminal to quickly create a task, set a reminder, or add a note.

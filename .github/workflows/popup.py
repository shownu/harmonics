from tkinter import Tk, Label

def popup():
    dialog_box = Tk()
    dialog_box.geometry('160x50+1000+600')
    if bool_closing == True or bool_NA == True:
        if bool_closing == True: title = 'closing'
        if bool_NA == True: title = 'N/A'
        Label(dialog_box, text = '-----', fg = 'red', bg = 'red').place(x = 10, y = 10)
    if bool_CPA == True or bool_opening == True:
        if bool_CPA == True: title = 'CPA'
        if bool_opening == True: title = 'opening'
        Label(dialog_box, text = '-----', fg = 'limegreen', bg = 'limegreen').place(x = 10, y = 10)
    Label(dialog_box, text = title).place(x = 50, y = 10)
    return dialog_box.mainloop()

bool_CPA = False
bool_opening = False
bool_NA = True
bool_closing = False

popup()

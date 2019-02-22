import tkinter as tk

from gui.view.mainView import mainView as mainViewClass

mainView = mainViewClass()

def popupView(msg):
    popupWindow = tk.Tk()
    popupWindow.wm_title('Is a Sabertron up ?')
    label = tk.Label(popupWindow, text=msg, font=('Helvetica', 10))
    label.pack(side='top', fill='x', pady=10)
    B1 = tk.Button(popupWindow, text='Okay', command = popupWindow.destroy)
    B1.pack()
    popupWindow.mainloop()

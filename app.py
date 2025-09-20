import tkinter as tk
from model import Model
from view import View
from controller import Controller

def main():
    root = tk.Tk()
    root.title("Pre-Enrollment (MVC) - Tkinter")
    model = Model()              # สร้าง model 
    view = View(root)            # สร้าง view 
    controller = Controller(model, view)  # controller 
    root.mainloop()

if __name__ == "__main__":
    main()

from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

# install tkinter instructions: https://tkdocs.com/tutorial/install.html
class TrialPotGui:
    def show(self, figure):
        root = Tk()

        canvas = FigureCanvasTkAgg(figure, root)
        canvas.get_tk_widget().grid(row=0, column=0)

        def on_closing():
            #if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        root.mainloop()

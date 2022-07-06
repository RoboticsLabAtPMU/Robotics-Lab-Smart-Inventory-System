from tkinter import *
import retrainer

class App:
    def __init__(self):
        self.top = Tk()
        self.top.title("Retrain IMS")
        self.top.geometry("700x600")
        self.top.configure(bg = '#c7e1ff')
        self.top.resizable(False, False)

        self.make_screen()

    def make_screen(self):
        frame = Frame(self.top, bg = '#c7e1ff')
        frame.pack(padx=10, pady=10)
        frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        title_label = Label(frame, text = "RETRAIN IMS MODEL", font = ("Helvetica", 20), bg = '#c7e1ff')
        title_label.pack(padx=10, pady=10)

        prompt_label = Label(frame, text = "Please click on retrain you would like to retrain", font = ("Helvetica", 12), bg = '#c7e1ff', fg="red")
        prompt_label.pack(padx=10, pady=10)

        retrain_button = Button(frame, text = "Retrain IMS", bg = 'green', fg="white", command = lambda: self.retrain_ims(), width=10)
        retrain_button.pack(padx=10, pady=5)

        exit_button = Button(frame, text = "Exit", bg = 'red', fg="white", command = lambda: exit(), width=10)
        exit_button.pack(padx=10, pady=5)

    def retrain_ims(self):
        message = retrainer.retrainer()
        

if __name__ == "__main__":
    app = App()
    app.top.mainloop()
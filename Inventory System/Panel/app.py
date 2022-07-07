import os
from tkinter import *
import cv2
from PIL import Image
from PIL import Image, ImageTk
import time
import requests

import image_handler
import utils

class App:
    def __init__(self):
        self.top = Tk()
        self.top.title("Inventory Management System")
        self.top.geometry("700x600")
        self.top.configure(bg = '#c7e1ff')
        self.top.resizable(False, False)

        self.prompt_label= None
        
        self.capture_time_limit_new_item = 10
        self.capture_time_limit_predict = 1
        self.start_time = 0

        self.processify_look = False
        self.break_feed=False
        self.camera_feed_in_use = False
        self.panels = []
        self.panel_stream = 0

        self.item_name=""
        self.no_of_items = -1

        self.user_id = ""
        self.usb_path = "/media/gufran/GsHDD/Work/Projects/Robotics-Lab-Smart-Inventory-System/Inventory System/Panel"
        
        self.login_screen()

    def reset(self):
        try:
            for i in self.panels:i.destroy()
        except:
            print("lol")
        self.panels=[]
        self.top.destroy()
        self.top = Tk()
        self.top.title("Inventory Management System")
        self.top.geometry("700x600")
        self.top.configure(bg = '#c7e1ff')
        self.top.resizable(False, False)
        self.break_feed=False
        self.no_of_items = -1

    def main_menu(self):
        frame = Frame(self.top, bg = '#c7e1ff')
        frame.pack(side=TOP, expand=True, fill=BOTH)
        frame.place(relx=0.5, rely=0.4, anchor=CENTER)

        title = Label(frame, text="Inventory Management System", font=("Arial", 25), fg='black', bg = '#c7e1ff')
        title.pack()

        buttonFrame = Frame(frame, bg = '#c7e1ff')
        buttonFrame.pack()

        button_co = Button(buttonFrame, text="Take item", command=lambda: self.button_handler("main","Check out"), bg="green", fg="white", width=10)
        button_co.grid(row=0,column=0, padx=10, pady=10)

        button_ci = Button(buttonFrame, text="Return item", command=lambda: self.button_handler("main","Check in"), bg="green", fg="white", width=10)
        button_ci.grid(row=1,column=0, padx=10, pady=10)

        button_register = Button(buttonFrame, text="Register Item", command=lambda: self.button_handler("main","Register"), bg="Orange", fg="white", width=10)
        button_register.grid(row=0,column=1, padx=10, pady=10)

        # button_eject = Button(buttonFrame, text="Eject Data", command=lambda: self.button_handler("main","log out"), bg="Orange", fg="white", width=10)
        # button_eject.grid(row=0,column=1, padx=10, pady=10)
        
        # button_delete = Button(buttonFrame, text="Delete Data", command=lambda: self.button_handler("main","log out"), bg="red", fg="white", width=10)
        # button_delete.grid(row=1,column=1, padx=10, pady=10)

        button_lo = Button(buttonFrame, text="Log Out", command=lambda: self.button_handler("main","log out"), bg="red", fg="white", width=10)
        button_lo.grid(row=1,column=1, padx=10, pady=10)

        prompt_label = Label(frame, text="", font=("Arial", 12), fg='red', bg = '#c7e1ff')
        prompt_label.pack(padx=10, pady=20)

        if self.user_id != "1111":
            button_register["state"] = "disabled"
            # button_eject["state"] = "disabled"
            # button_delete["state"] = "disabled"
        
        if not os.path.exists(self.usb_path):
            title.config(text = "No USB detected. Log out and try again")
            button_co["state"] = "disabled"
            button_ci["state"] = "disabled"
        if not os.path.exists(self.usb_path+"/Images") or len(os.listdir(self.usb_path+"/Images"))<3 or not os.path.exists(self.usb_path+"/Model"):
            l = 0
            try:
                l = len(os.listdir(self.usb_path+"/Images"))
            except:
                l=0
            if 3-l > 0: prompt_label.config(text = "Model not ready. Please register "+str(3-l)+" more items")
            else: prompt_label.config(text = "Model not ready. Please train the model on Desktop Retrainer app")
            button_co["state"] = "disabled"
            button_ci["state"] = "disabled"
        
    def login_screen(self):
        frame = Frame(self.top, bg = '#c7e1ff')
        frame.pack()
        frame.place(relx=0.5, rely=0.5, anchor="center")

        self.prompt_label = Label(frame, text="Please enter your login details", font=("Arial", 12), fg='red', bg = '#c7e1ff')
        self.prompt_label.grid(row=0, column=0, padx=5, pady=5)

        rowFrame1 = Frame(frame, bg = '#c7e1ff')
        rowFrame1.grid(row=1, column=0, padx=10, pady=5)
        E1 = Entry(rowFrame1, bd =5)
        E1.insert(0,"Username")
        E1.pack()

        rowFrame2 = Frame(frame, bg = '#c7e1ff')
        rowFrame2.grid(row=2, column=0, padx=10, pady=5)
        E2 = Entry(rowFrame2, bd =5)
        E2.insert(0,"Password")
        E2.pack()

        rowFrame3 = Frame(frame, bg = '#c7e1ff')
        rowFrame3.grid(row=3, column=0, padx=10, pady=20)
        Button(rowFrame3, text='Login', command=lambda:self.button_handler("login screen", "login", [E1.get(), E2.get()]), width=10, bg="green", fg="white").pack(pady=5, padx = 10, side="left")

    def pre_register_screen(self):
        frame = Frame(self.top, bg = '#c7e1ff')
        frame.pack()
        frame.place(relx=0.5, rely=0.5, anchor="center")

        self.prompt_label = Label(frame, text="Please enter item name and amount", font=("Arial", 12), fg='red', bg = '#c7e1ff')
        self.prompt_label.grid(row=0, column=0, padx=10, pady=5)        

        rowFrame1 = Frame(frame, bg = '#c7e1ff')
        rowFrame1.grid(row=1, column=0, padx=10, pady=5)        
        E1 = Entry(rowFrame1, bd =5)
        E1.insert(0,"Item name")
        E1.pack()

        E2 = Entry(rowFrame1, bd =5)
        E2.insert(0,"Amount")
        E2.pack()

        Button(frame, text='Next', command=lambda:self.button_handler("pre register", "Register", [E1.get(), E2.get()]), width=10, bg="green", fg="white").grid(row=2, column=0, padx=10, pady=20)

    def instruction_screen(self, prev_page, action):
        if prev_page == "main":
            if "Check" in action: instructions = "Place item in center of camera view.\nAvoid any type of background interference\n"+\
                "Do not remove item until prompted.\nIf item is not identified after multiple tries, the item\nmight not be registerd."
            else: instructions = "The camera will take pictures for the next 30 seconds\nRotate the item and show every angle.\n"+\
                "If there are multiple ways to identify the data, click on the\n 'Add Identifier' button. Then, click on the 'Eject Data' button."

            frame = Frame(self.top, bg = '#c7e1ff')
            frame.pack()
            frame.place(relx=0.5, rely=0.5, anchor="center")
            Label(frame, text=instructions, font=("Arial", 15), fg='red', bg = '#c7e1ff').pack(side="top")

            buttonFrame = Frame(self.top, bg = '#c7e1ff', width=50)
            buttonFrame.pack(side="bottom")
            buttonFrame.place(relx=0.5,rely=0.7, anchor="center")
            Button(buttonFrame, text='Next', command=lambda:self.button_handler("instructions", action if action!="Register" else "get name"), width=10, bg="green", fg="white").pack(pady=20, padx = 10, side="left")
            Button(buttonFrame, text='Back', command=lambda:self.button_handler("instructions", "back"), width=10, bg="red", fg="white").pack(pady=20, padx=10, side="right")

    def camera_screen(self, action):
        self.break_feed=False
        self.camera_feed_in_use = False
        if action == "Register":
            break_time = self.capture_time_limit_new_item
            self.no_of_items = 0
        else: break_time = self.capture_time_limit_predict

        prompt_label = Label(self.top, text="", font=("Arial", 15), fg='red', bg = '#c7e1ff')
        prompt_label.pack()
        prompt_label.place(rely=0.05, relx=0.5, anchor="center")

        buttonFrame = Frame(self.top, bg = '#c7e1ff')
        buttonFrame.pack(side=BOTTOM, pady=10)

        add_identifier_button = Button(buttonFrame, text="Add Identifier", command=lambda:self.button_handler("camera screen", "add"), width=10, bg="orange", fg="white")
        if action == "Register": add_identifier_button.grid(row=0,column=0, padx=10, pady=0)
        action_button = Button(buttonFrame, text=action, command=lambda:self.button_handler("camera screen",action), width=10, bg="green", fg="white")
        action_button.grid(row=0,column=1, padx=10, pady=0)
        try_again_button = Button(buttonFrame, text="Start", command=lambda:self.button_handler("camera screen","again"), width=10, bg="green", fg="white")
        try_again_button.grid(row=0,column=2, padx=10, pady=0)
        back_button = Button(buttonFrame, text="Back", command=lambda:self.button_handler("camera screen","back"), width=10, bg="red", fg="white")
        back_button.grid(row=0,column=3, padx=10, pady=0)

        self.start_time = time.time()
        images = []
        cap = cv2.VideoCapture(2)

        action_button["state"] = "disabled"

        while True:
            img = cv2.flip(cap.read()[1], 1)
            processed_image = image_handler.process(img)

            if self.camera_feed_in_use:
                if action == "Register":prompt_label.config(text = "Capturing...")
                else: prompt_label.config(text = "Detecting item...")

                if try_again_button["text"] == "Start":try_again_button["text"] = "Try Again"

                images.append({
                    "name": self.item_name,
                    "id": len(images)+1,
                    "image": processed_image
                })

                if try_again_button["state"] == "normal":
                    action_button["state"] = "disabled"
                    try_again_button["state"] = "disabled"
                    add_identifier_button["state"] = "disabled"
                    back_button["state"] = "disabled"

            if time.time() - self.start_time > break_time and self.camera_feed_in_use:
                self.start_time=time.time()
                self.camera_feed_in_use = False

                if action != "Register": 
                    image_handler.save_images_from_check_io(images)
                    self.item_name = utils.predict()
                    if self.item_name == -1:
                        prompt_label.config(text = "Item not recognized")
                        try_again_button["state"] = "normal"
                    else:
                        prompt_label.config(text = "Item recognized as: " + self.item_name)
                        action_button["state"] = "normal"
                        try_again_button["state"] = "normal"
                        add_identifier_button["state"] = "normal"
                        back_button["state"] = "normal"
                else: 
                    prompt_label.config(text = "")
                    if self.no_of_items!=-1:self.no_of_items+=1
                    image_handler.save_images_from_register(images, self.no_of_items)
                    action_button["state"] = "normal"
                    try_again_button["state"] = "normal"
                    add_identifier_button["state"] = "normal"
                    back_button["state"] = "normal"
                
                images = []

            if self.processify_look: img = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            else: img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(img))

            if len(self.panels)!=2:
                self.panels.append(None)
                self.panels[len(self.panels)-1] = Label(self.top, image=img)
                self.panels[len(self.panels)-1].image = img
                self.panels[len(self.panels)-1].pack(side="top", fill="both", expand="yes")
                self.panels[len(self.panels)-1].place(relx=0.5, rely=0.5, anchor=CENTER)
            else:
                self.panels[0].destroy()
                del self.panels[0]

            if self.break_feed:
                self.reset()
                break
            else:self.top.update()
        self.main_menu()

    def button_handler(self,caller_page,action,extras=[]):
        if action == "login":
            self.user_id=extras[0]
            self.reset()
            self.main_menu()
            self.prompt_label = None
            # url = 'http://172.16.154.120:8000/'
            # data = {"id":extras[0],"password":extras[1]}
            # x = requests.post(url,data=data)

            # if x.text == "yes":
            #     self.user_id=extras[0]
            #     self.reset()
            #     self.main_menu()
            #     self.prompt_label = None
            # else:
            #     self.prompt_label.config(text = "no bro")
        elif action == "back" or action == "Register" and caller_page not in ["main","instructions","pre register"]:
            if caller_page == "camera screen":
                if self.no_of_items!=-1:
                    if action=="back":image_handler.handle_register_abort(self.item_name)
                    else: utils.register(self.item_name, self.register_item_amount)
                self.break_feed=True
            else: 
                self.reset()
                self.main_menu()
        elif caller_page == "main":
            if action != "log out":
                self.reset()
                self.instruction_screen(caller_page,action)
            else:
                self.reset()
                self.user_id=""
                self.login_screen()
        elif caller_page == "instructions" or caller_page == "pre register":
            if action == "back":self.main_menu()
            elif action == "get name":
                self.reset()
                self.pre_register_screen()
            else: 
                if action == "Register":
                    self.item_name=extras[0]
                    try:
                        if utils.check_item_existence(extras[0]) == "yes":
                            self.prompt_label.config(text = "Item exists!")
                            return
                        if len(extras[0])==0 or len(extras[1])==0:
                            self.prompt_label.config(text = "Enter all details")
                            return
                        else:
                            self.item_name = extras[0]
                            self.register_item_amount = int(extras[1])
                    except:
                        self.prompt_label.config(text = "Invalid details!")
                        return           
                self.camera_screen(action)
        elif action == 'again' or action  == 'add':
            self.camera_feed_in_use=True
            self.start_time = time.time()
            self.break_feed=False
            if action == 'again' and self.no_of_items != -1:
                self.no_of_items = max(0,self.no_of_items-1)
                if self.no_of_items!=0: image_handler.del_last_entry(self.item_name)
        elif ("Check" in action) and caller_page=="camera screen":
            if "in" in action: utils.check_in(self.user_id,self.item_name)
            else: utils.check_out(self.user_id,self.item_name)
            self.break_feed=True

if '__main__' == __name__:
    app = App()
    app.top.mainloop()
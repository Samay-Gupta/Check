from Additional.User_Data import UserData
from Additional.QR_Scanner import Scanner
import socket
import geocoder
from tkinter import *
import time
import threading

class Station:
    def __init__(self):
        self.serv = socket.socket()
        self.ct = ''
        self.route = "route_A"
        self.stop_name = "stopA2"
        self.scanner = Scanner()
        self.data_bank = UserData()
        self.window = Tk()
        self.window.configure(bg="white")
        self.window.geometry('192x1080+0+0')
        self.window.attributes("-fullscreen", True)
        self.frame = ""
        self.cur_user = ""
        self.result = False

    def get_location(self):
        return list(geocoder.ip('me').latlng)

    def scan(self):
        user_id = self.scanner.qr_live()
        print(user_id)
        valid = self.data_bank.check(user_id)
        if valid:
            return user_id
        else:
            return False

    def run(self, id_name):
        res = self.data_bank.calc(id_name, self.stop_name, self.route)
        self.disp(res)

    def amt(self, user_id, data):
        amt = int(str(data.get()))
        res = self.data_bank.load(user_id, amt)
        self.disp(res)
        
    def add(self, user_id):
        self.frame.destroy()
        self.frame = Frame(self.window, width=1920, height=1080)
        self.frame.pack()
        lg = "Logged in as {}".format(user_id)
        label = Label(self.frame, text=lg, fg="black", font=("Comic Sans", 30, "bold"), bg="white")
        label.grid(row=0, column=0, columnspan = 3)
        val_ent = Entry(self.frame, text="Amount", fg="black", font=("Comic Sans", 30, "bold"), bg="white", bd=2)
        val_ent.grid(row=1, column=0)
        cnf_cmd = lambda event, user_id=user_id: self.amt(user_id, val_ent)
        cnf_btn = Button(self.frame, text="CONFIRM", fg="black", font=("Comic Sans", 30, "bold"), bg="white")
        cnf_btn.bind("<Button-1>", cnf_cmd)
        cnf_btn.grid(row=1, column=1)
        window.update()

    def disp(self, res):
        if self.frame != "":
            self.frame.destroy()
        if res[0] == 0:
            color = 'red'
        elif res[0] >= 1:
            color = 'green'
        self.frame = Frame(self.window, width=1920, height=1080)
        self.frame.pack()
        label = Label(self.frame, text=res[1], fg=color, bg="white", font=("Comic Sans", 30, "bold"))
        label.pack(expand='yes')
        self.window.update()
        time.sleep(3)
        self.main_screen()

    def disable(self, user_id):
        print("DISABLE")
        res = self.data_bank.disable(user_id)
        self.disp(res)
        
    def main_screen(self):
        time.sleep(0.25)
        if self.frame != "":
            self.frame.destroy()
        self.frame = Frame(self.window, width=1920, height=1080, bg="white")
        self.frame.pack()
        label = Label(self.frame, text="Place code over camera", fg="black", font=("Comic Sans", 30, "bold"), bg="white")
        label.grid(row=0, column=0 ,columnspan = 3)
        self.result = False
        self.window.update()
        user_id = self.scan()
        self.result = True
        self.run(user_id)

        """
        mn_btn = Button(self.frame, text="OPTIONS", fg="black", font=("Comic Sans", 30, "bold"), bg="white", command=self.option_screen)
        mn_btn.grid(row=1, column=0)
        self.window.update()
        self.ct = threading.Thread(target=self.listener())
        self.ct.run()
        """



    def option_screen(self):
        time.sleep(0.25)
        if self.frame != "":
            self.frame.destroy()
        self.frame = Frame(self.window, width=1920, height=1080, bg="white")
        self.frame.pack()
        label = Label(self.frame, text="Place code over camera", fg="black", font=("Comic Sans", 30, "bold"), bg="white")
        label.grid(row=0, column=0, columnspan=3)
        self.window.update()
        user_id = self.scan()
        print(user_id, "usr")
        if user_id:
            self.show_options(user_id, label)
            
    def show_options(self, user_id, label):
        time.sleep(0.25)
        label.destroy()
        self.frame = Frame(self.window, width=1920, height=1080, bg="white")
        self.frame.pack()
        lg = "Logged in as {}".format(user_id)
        label = Label(self.frame, text=lg, fg="black", font=("Comic Sans", 30, "bold"), bg="white")
        label.grid(row=0, column=0, columnspan = 3)
        add_cmd = lambda event, user_id=user_id: self.add(user_id)
        add_btn = Button(self.frame, text="ADD", fg="black", font=("Comic Sans", 30, "bold"), bg="white")
        add_btn.bind("<Button-1>", add_cmd)
        add_btn.grid(row=1, column=0)
        del_cmd = lambda event, user_id=user_id: self.disable(user_id)
        del_btn = Button(self.frame, text="DEACTIVATE", fg="black", font=("Comic Sans", 30, "bold"), bg="white")
        del_btn.bind("<Button-1>", del_cmd)
        del_btn.grid(row=1, column=1)
        mn_btn = Button(self.frame, text="MAIN", fg="black", font=("Comic Sans", 30, "bold"), bg="white", command=self.main_screen)
        mn_btn.grid(row=1, column=2)
        self.window.mainloop()
        


    def load(self, amt):
        pass

    def new(self, name, phone_number, email):
        pass

    def travel(self):
        pass

st = Station()
st.main_screen()

import socket
from tkinter import *
from tkinter.font import Font
import random
from datetime import datetime
import re
import json
import easygui
import _thread


# import client_filetransfer_Gabriel_Yeager

def main():
    global IP, PORT
    ip = "76.120.32.88" or input("Input IP Address of Server: ")  # default 192.168.1.129 unless it changed
    port = 5005 or int(input("Input Port for Server: "))  # default 5005 and should remain constant
    IP = ip
    PORT = port
    ui_setup(ip, port)


def receive_messages(message_box, username, ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    while True:
        data = s.recv(1024).decode('utf-8')
        if data is not None and data != "Connected to chatroom":
            print(data)
            data = json.loads(data)
            if data.get("sender") != username.get():
                if data.get("Operation") == '1':
                    message_box.add_received_message(data)
                else:
                    message_box.add_received_file(data)


def ui_setup(ip, port):
    root = Tk()
    root.title("CS-3080 Final Project")
    root.geometry('900x500')
    # background canvas
    canvas = Canvas(root, width=900, height=500, bg='#141414', highlightthickness=0)
    canvas.place(x=0, y=0, anchor='nw')

    # container for message entry
    entry_canvas = Canvas(canvas, width=880, height=40, bg='#141414', highlightthickness=0)
    entry_canvas.place(x=450, y=490, anchor='s')
    round_rectangle(entry_canvas, 0, 0, 820, 40, fill='#444444')

    # text entry
    text = Text(entry_canvas, width=85, height=2, bg='#444444',
                highlightthickness=0, font=Font(family="Calibri", size=15), selectbackground='#666666')
    text.place(x=10, y=20, anchor='w')

    # Username and profile color variables
    username = StringVar()
    color = StringVar()
    color.set('#ff00f0')
    username.set(f"User-{random.randint(1, 1000)}")

    # send button
    entry_canvas.create_oval(830, 0, 870, 40, fill='#338edb', tags='send')
    entry_canvas.create_bitmap(852, 20, bitmap="@send_icon.xbm", tags='send')

    # attach button
    entry_canvas.create_bitmap(800, 20, bitmap="@attach_icon.xbm", tags='attach')

    messages = MessageFrame(canvas, 880, 430)
    messages.place(x=10, y=10, anchor='nw')

    entry_canvas.tag_bind('send', '<Button-1>', lambda e: send_message(e, text, messages, username, color, ip, port))
    entry_canvas.tag_bind('attach', '<Button-1>', lambda e: attach_file(e, text, messages, username, color, ip, port))

    menu = Menu(root)
    settings_menu = Menu(menu, tearoff=0)
    settings_menu.add_command(label="Profile", command=lambda: edit_profile(username, color))
    menu.add_cascade(label="Settings", menu=settings_menu)
    root.config(menu=menu)

    _thread.start_new_thread(receive_messages, (messages, username, ip, port))

    root.mainloop()


def attach_file(event, message_box, message_frame, sender, color, ip, port):
    path = easygui.fileopenbox()
    send_file(event, message_box, message_frame, sender, color, ip, port, path)


def send_file(event, message_box, message_frame, sender, color, ip, port, path):
    msg = message_box.get("1.0", 'end-1c')
    time = datetime.now().strftime("%m/%d/%y %I:%M %p")

    # home/documents/myfile.txt
    data = {"file_name": path, "sender": sender.get(), "time": time, "color": color.get(), "Operation": "2"}
    # client_filetransfer_Gabriel_Yeager.send_file(path, data)
    message_frame.add_sent_file(data)


def edit_profile(username_var, color_var):
    window = Tk()
    window.geometry("200x200")
    window.title("Edit Profile")
    window.config(bg="#141414")

    Label(window, text="Username", bg='#141414', fg='#ffffff').place(x=100, y=10, anchor='n')
    entry = Text(window, width=10, height=1, font=Font(family="Calibri", size=15))
    entry.place(x=100, y=40, anchor='n')
    entry.insert("end-1c", username_var.get())

    Label(window, text="Profile Hex Color", bg='#141414', fg='#ffffff').place(x=100, y=80, anchor='n')
    color_entry = Text(window, width=10, height=1, font=Font(family="calibri", size=15))
    color_entry.place(x=100, y=110, anchor='n')
    color_entry.insert("end-1c", color_var.get())

    save = Label(window, text="SAVE")
    save.place(x=100, y=160, anchor='n')
    save.bind("<Button-1>", lambda e: save_profile(username_var, color_var, entry, color_entry, window))


def save_profile(username_var, color_var, user_entry, color_entry, window):
    color = color_entry.get("1.0", "end-1c")
    if color[0] != '#':
        color.insert(0, '#')
    if re.fullmatch(r'#[0-9a-fA-F]{6}', color):
        username_var.set(user_entry.get("1.0", 'end-1c'))
        color_var.set(color)
        window.destroy()
    else:
        Label(window, text="Color must match '#xxxxxx'", fg='#ff0000',
              bg="#141414", font=Font(family="calibri", size=15)).place(x=100, y=135, anchor='n')


def send_message(event, message_box, message_frame, sender, color, ip, port):
    msg = message_box.get("1.0", 'end-1c')
    time = datetime.now().strftime("%m/%d/%y %I:%M %p")
    data = {"message": msg, "sender": sender.get(), "time": time, "color": color.get(), "Operation": "1"}
    message_frame.add_sent_message(data)
    message_box.delete("1.0", 'end')
    MESSAGE = bytes(json.dumps(data), encoding='utf-8')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(MESSAGE)
    resp = s.recv(1024)
    s.close()


def receive_file(file_name, ip, port):
    data = {"file_name": file_name, "Operation": "3"}
    print(data)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(bytes(json.dumps(data), encoding='utf-8'))

    # From Gabriel's server_file_transfer_Gabriel_Yeager.py

    print(s.recv(4096))

    while True:
        data_piece = s.recv(4096)
        if not data_piece:
            # file transmission is done
            break
        f = open(file_name, "ab+")
        f.write(data_piece)
        f.close()
    print("file open")

    s.close()


class MessageFrame(Frame):
    def __init__(self, parent, width, height):
        Frame.__init__(self, parent)
        self.width = width
        # Create canvas for everything to go on
        self.canvas = Canvas(self, borderwidth=0, background="#141414", width=width - 15, height=height,
                             highlightthickness=0)

        # place a frame and scrollbar
        self.frame = Frame(self.canvas, background="#141414", bd=0)
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview, bg='#141414')
        # attach scrollbar to canvas
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # put everything in the window
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window(0, 0, window=self.frame, anchor="nw",
                                  tags="self.frame")

        # This variable controls whether the canvas scrolls to most recent msg
        self.move_scrollbar = False

        # bind configuration changes
        self.frame.bind("<Configure>", self.on_frame_configure)

        # populate sample data. Uncomment for testing
        self.populate(width, height)

    def add_received_message(self, data):
        self.move_scrollbar = True
        padding_height = 30
        row_height = 15
        # height has a minimum threshold of 45px then add additional 15px per line
        height = padding_height + row_height + ((len(data.get("message")) // 92) * row_height)

        # Create canvas to place individual message on
        can = Canvas(self.frame, width=self.width - 30, height=height, borderwidth=0,
                     bd=0, bg="#141414", highlightthickness=0)

        # create rounded rectangle background for aesthetics
        round_rectangle(can, 0, 0, self.width - 180, height, fill="#444444")

        # username and timestamp
        user = Label(can, text=f"{data.get('sender'.strip())}  " + u"\u2022" + f"  {data.get('time').strip()}",
                     bg='#444444', font=Font(family="Calibri", size=9))
        user.place(x=50, y=3, anchor='nw')

        # label with message
        msg_label = Label(can, text=data.get("message").strip(), width=80, anchor='w',
                          bg=f"#444444", justify='left', wraplength=self.width - 240,
                          font=Font(family="Calibri"))
        msg_label.place(x=50, y=15, anchor='nw')

        # profile pic area
        pic = can.create_oval(40, 10, 10, 40, fill=data.get("color"), outline=data.get("color"))
        can.create_text(25, 25, text=data.get("sender")[0].upper())

        can.grid(row=self.frame.grid_size()[1], column=0, pady=4)

    def add_received_file(self, data):
        self.move_scrollbar = True

        padding_height = 30
        row_height = 15
        # height has a minimum threshold of 45px then add additional 15px per line
        height = padding_height + row_height + ((len(data.get("file_name")) // 92) * row_height)

        # Create canvas to place individual message on
        can = Canvas(self.frame, width=self.width - 30, height=height, borderwidth=0,
                     bd=0, bg="#141414", highlightthickness=0)

        # create rounded rectangle background for aesthetics
        round_rectangle(can, 0, 0, self.width - 180, height, fill="#444444")

        # username and timestamp
        user = Label(can, text=f"{data.get('sender'.strip())}  " + u"\u2022" + f"  {data.get('time').strip()}",
                     bg='#444444', font=Font(family="Calibri", size=9))
        user.place(x=95, y=3, anchor='nw')

        # label with message
        msg_label = Label(can, text=data.get("file_name").strip(), width=60, anchor='w',
                          bg=f"#444444", justify='left', wraplength=self.width - 240,
                          font=Font(family="Calibri"))
        msg_label.place(x=120, y=15, anchor='nw')

        # download btn
        b = can.create_bitmap(70, 25, bitmap="@download.xbm")
        can.tag_bind(b, "<Button-1>", lambda e: self.download_file(data.get("file_name")))

        # profile pic area
        pic = can.create_oval(40, 10, 10, 40, fill=data.get("color"), outline=data.get("color"))
        can.create_text(25, 25, text=data.get("sender")[0].upper())

        can.grid(row=self.frame.grid_size()[1], column=0, pady=4)



    def add_sent_file(self, data):
        self.move_scrollbar = True

        padding_height = 30
        row_height = 15
        height = padding_height + row_height + ((len(data.get("file_name")) // 92) * row_height)

        # wrapper canvas and colored blob
        can = Canvas(self.frame, width=self.width - 30, height=height, borderwidth=0, bd=0,
                     bg="#141414", highlightthickness=0)
        round_rectangle(can, 150, 0, self.width - 30, height, fill=f"#444444")

        # username and timestamp
        user = Label(can, text=f"You  " + u"\u2022" + f"  {data.get('time').strip()}", bg='#444444',
                     font=Font(family="Calibri", size=9))
        user.place(x=self.width - 125, y=3, anchor='ne')

        # label with message
        msg_label = Label(can, text=data.get("file_name").strip(), width=60, anchor='e',
                          bg=f"#444444", justify='left', wraplength=self.width - 240, font=Font(family="Calibri"))
        msg_label.place(x=self.width - 150, y=15, anchor='ne')

        # download btn
        d = can.create_bitmap(self.width - 105, 25, bitmap="@download.xbm")
        can.tag_bind(d, "<Button-1>", lambda e: self.download_file(data.get("file_name")))

        # profile pic area
        pic = can.create_oval(self.width - 70, 10, self.width - 40, 40, fill=data.get("color"),
                              outline=data.get("color"))
        can.create_text(self.width - 55, 25, text=data.get("sender")[0].upper())

        can.grid(row=self.frame.grid_size()[1], column=0, pady=4)

    def download_file(self, file_name):
        _thread.start_new_thread(receive_file, (file_name, IP, PORT))


    def add_sent_message(self, data):
        self.move_scrollbar = True
        c = hex(random.randint(0, 255))
        c = c[2:] if len(c[2:]) == 2 else '0' + c[2:]

        padding_height = 30
        row_height = 15

        height = padding_height + row_height + ((len(data.get("message")) // 92) * row_height)

        # wrapper canvas and colored blob
        can = Canvas(self.frame, width=self.width - 30, height=height, borderwidth=0, bd=0,
                     bg="#141414", highlightthickness=0)
        round_rectangle(can, 150, 0, self.width - 30, height, fill=f"#444444")

        # username and timestamp
        user = Label(can, text=f"You  " + u"\u2022" + f"  {data.get('time').strip()}", bg='#444444',
                     font=Font(family="Calibri", size=9))
        user.place(x=self.width - 80, y=3, anchor='ne')

        # label with message
        msg_label = Label(can, text=data.get("message").strip(), width=80, anchor='e',
                          bg=f"#444444", justify='left', wraplength=self.width - 240, font=Font(family="Calibri"))
        msg_label.place(x=self.width - 80, y=15, anchor='ne')

        # profile pic area
        pic = can.create_oval(self.width - 70, 10, self.width - 40, 40, fill=data.get("color"),
                              outline=data.get("color"))
        can.create_text(self.width - 55, 25, text=data.get("sender")[0].upper())

        can.grid(row=self.frame.grid_size()[1], column=0, pady=4)

    def populate(self, width, height):
        """Put in some fake data for testing"""
        for row in range(100):
            data = {"message": f"This is the {row} row of the messages", "sender": "Haberkorn",
                    "time": "01/12/2020 03:36 PM", "color": "#ff4512"}
            if row % 3 == 0:
                self.add_sent_message(data)
            else:
                self.add_received_message(data)

        data = {"message": f"This is the last row of the messages {'ahhh ' * 120}", "sender": "SHaberkorn",
                "time": "01/12/2020 03:36 PM", "color": "#554512"}
        self.add_received_message(data)

        data = {"file_name": "Hello.txt", "sender": "SHaberkorn", "time": "01/12/2020 03:36 PM", "color": "#554512"}
        self.add_sent_file(data)
        self.add_received_file(data)

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        if self.move_scrollbar:
            self.canvas.yview_moveto(1.0)
            self.move_scrollbar = False


def round_rectangle(master, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]

    return master.create_polygon(points, **kwargs, smooth=True)


if __name__ == '__main__':
    main()

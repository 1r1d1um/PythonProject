import socket
from tkinter import *
import helpers
from tkinter.font import Font
import random
from datetime import datetime


def main():
    root = Tk()
    root.title("CS-3080 Final Project")
    root.geometry('900x500')
    # background canvas
    canvas = Canvas(root, width=900, height=500, bg='#141414', highlightthickness=0)
    canvas.place(x=0, y=0, anchor='nw')

    # container for message entry
    entry_canvas = Canvas(canvas, width=880, height=40, bg='#141414', highlightthickness=0)
    entry_canvas.place(x=450, y=490, anchor='s')
    helpers.round_rectangle(entry_canvas, 0, 0, 820, 40, fill='#3c3f41')

    # text entry
    text = Text(entry_canvas, width=87, height=2, bg='#3c3f41',
                highlightthickness=0, font=Font(family="Calibri", size=15), fg='#ffffff')
    text.place(x=10, y=20, anchor='w')

    # send button
    entry_canvas.create_oval(830, 0, 870, 40, fill='#3c3f41', tags='send')
    entry_canvas.create_bitmap(852, 20, bitmap="@send_icon.xbm", tags='send')

    messages = MessageFrame(canvas, 880, 430)
    messages.place(x=10, y=10, anchor='nw')

    entry_canvas.tag_bind('send', '<Button-1>', lambda e: send_message(e, text, messages))

    root.mainloop()


def send_message(event, message_box, message_frame):
    msg = message_box.get("1.0", 'end-1c')
    sender = "haberkornsam"
    time = datetime.now().strftime("%m/%d/%y %I:%M %p")
    data = {"message": msg, "sender": sender, "time": time}
    message_frame.add_sent_message(data)
    message_box.delete("1.0", 'end')


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
        self.frame.bind("<Configure>", self.onFrameConfigure)

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
        helpers.round_rectangle(can, 0, 0, self.width - 180, height, fill="#444444")

        # username and timestamp
        l = Label(can, text=f"{data.get('sender'.strip())}  " + u"\u2022" + f"  {data.get('time').strip()}",
                  bg='#444444',
                  font=Font(family="Calibri", size=9))
        l.place(x=50, y=3, anchor='nw')

        # label with message
        l = Label(can, text=data.get("message").strip(), width=80, anchor='w',
                  bg=f"#444444", justify='left', wraplength=self.width - 240)
        l.place(x=50, y=15, anchor='nw')

        # profile pic area
        pic = can.create_oval(40, 10, 10, 40, fill='#ff00f0')
        can.create_text(25, 25, text=data.get("sender")[0].upper())

        can.grid(row=self.frame.grid_size()[1], column=0, pady=4)


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
        helpers.round_rectangle(can, 150, 0, self.width - 30, height, fill=f"#444444")

        # username and timestamp
        l = Label(can, text=f"You  " + u"\u2022" + f"  {data.get('time').strip()}", bg='#444444',
                  font=Font(family="Calibri", size=9))
        l.place(x=self.width - 80, y=3, anchor='ne')

        # label with message
        l = Label(can, text=data.get("message").strip(), width=80, anchor='e',
                  bg=f"#444444", justify='left', wraplength=self.width - 240)
        l.place(x=self.width - 80, y=15, anchor='ne')

        # profile pic area
        pic = can.create_oval(self.width - 70, 10, self.width - 40, 40, fill='#ff00f0')
        can.create_text(self.width - 55, 25, text=data.get("sender")[0].upper())

        can.grid(row=self.frame.grid_size()[1], column=0, pady=4)




    def populate(self, width, height):
        '''Put in some fake data'''
        for row in range(100):
            data = {"message": f"This is the {row} row of the messages", "sender": "Haberkorn",
                    "time": "01/12/2020 03:36 PM"}
            if row % 3 == 0:
                self.add_sent_message(data)
            else:
                self.add_received_message(data)

        data = {"message": f"This is the last row of the messages {'ahhh ' * 120}", "sender": "SHaberkorn",
                "time": "01/12/2020 03:36 PM"}
        self.add_received_message(data)


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        if self.move_scrollbar:
            self.canvas.yview_moveto(1.0)
            self.move_scrollbar = False




if __name__ == '__main__':
    main()

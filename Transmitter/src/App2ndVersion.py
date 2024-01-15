import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo
import datetime
import serial
import time

class TransmitterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.width = 900
        self.height = 600

        self.arduino = None

        self.title('Transmitter')
        self.geometry(f'{self.width}x{self.height}')
        self.center_window
        self.resizable(False, False)
        self.configure(bg="#051B37")

        custom_font = ("Arial Black", 11, "bold")  # Message text
        custom_font2 = ("Arial Black", 13, "bold")  # Label text
        custom_font3 = ("Arial Black", 14, "bold")  # Button text
        custom_font4 = ("Arial Black", 13, "bold")  # Chat text

        self.serial_port = 'COM5'
        self.baud_rate = 57600

        # Label
        self.label = Label(self, text='Transmitter App')
        self.label.config(font=custom_font2, bg='#051B37', fg='white')
        self.label.pack()

        # Frame to hold the chat widget
        chat_frame = Frame(self)
        chat_frame.pack(side='top', anchor='n', padx=20, pady=20)

        self.chat_text = Text(chat_frame, height=18, width=70, wrap=tk.WORD)
        self.chat_text.config(font=custom_font4, bg='#051B37', fg='white')
        self.chat_text.grid(row=0, column=0)
        self.chat_text.configure(state='disabled')

        # ScrollBar
        self.scroll_bar = Scrollbar(chat_frame, command=self.chat_text.yview)
        self.scroll_bar.grid(row=0, column=1, sticky='ns')
        self.chat_text.config(yscrollcommand=self.scroll_bar.set)

        # Frame to hold the message widget and the scrollbar
        text_frame = Frame(self)
        text_frame.pack(side='top', anchor='s', padx=10, pady=10)

        # Input area using Text widget
        self.input_text = Text(text_frame, height=3, width=90, wrap=tk.WORD)
        self.input_text.config(font=custom_font, bg='white')
        self.input_text.grid(row=2, column=0, sticky='s')  # Use grid layout

        # Configure grid column and row weights to make the text area expand
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        # Button
        self.button = Button(text_frame, height=2, width=16, text='Send', command=self.button_clicked)
        self.button.config(font=custom_font3, background='#0F3288')
        self.button.grid(row=2, column=1)  # Use grid layout

        
        self.connect_arduino()
      

        # Load previous messages
        self.chat_text.config(state='normal')
        f = open("messages.txt", "r")
        f.seek(0)
        for x in f:
            self.chat_text.insert(tk.END, x)
        f.close()
        self.chat_text.config(state='disabled')

    def write_message(self, message):
        f = open("messages.txt", "a")
        f.write(message)
        f.close()

    def button_clicked(self, Event=None):
        temp_message = self.input_text.get("1.0", END)
        self.chat_text.config(state='normal')
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S -> ")
        message = formatted_time + temp_message
        self.write_message(message)
        self.chat_text.insert(tk.END, message)
        self.chat_text.config(state='disabled')
        self.input_text.delete("1.0", tk.END)
        try:
            self.serial_send(temp_message)
        except serial.SerialException as e:
            showinfo("Information", e)

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2

        self.geometry(f'{self.width}x{self.height}+{x}+{y}')

    def connect_arduino(self):
        while True:
            try:
                self.arduino = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
                break
            except serial.SerialException as e:
                print("Couldn't connect to Arduino")
                print("Error ", e)
                time.sleep(2) 

    def serial_send(self, message):
        try:
            if self.arduino:  # Check if arduino is connected
                int_message = []
                checksum = 0
                for i in message:
                    int_message.append(ord(i))
                    checksum += ord(i)
                string_message = ""
                for i in int_message:
                    temp = ""
                    while i != 0:
                        i, remainder = divmod(i, 2)
                        temp = str(remainder) + temp
                    while len(temp) != 8:
                        temp = "0" + temp
                    string_message += temp
                string_checksum = ""  # adding 32-bit checksum
                while checksum != 0:
                    checksum, remainder = divmod(checksum, 2)
                    string_checksum = str(remainder) + string_checksum
                while len(string_checksum) < 32:
                    string_checksum = "0" + string_checksum
                for i in range(0, 37 - len(string_message)%38):
                    string_message =string_message + "0"
                #string_message += string_checksum
                #string_message = '0' + string_message
                print(string_message)
                print("here - ", string_message.encode())
                self.arduino.write(string_message.encode())
            else:
                showinfo("Information", "Arduino is not connected")
        except KeyboardInterrupt:
            print("Exiting program")
            if self.arduino:
                self.arduino.close()
            
        

if __name__ == "__main__":
    app = TransmitterApp()
    app.mainloop()
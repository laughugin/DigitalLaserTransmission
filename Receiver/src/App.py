import tkinter as tk
from tkinter import *
import datetime
import time
import serial
from tkinter.messagebox import showinfo
from Convert import Convert 
import threading

class ReceiverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.width = 900
        self.height = 600
        self.file_path = "receiverBinaryWordList.txt"
        self.arduino = None 
        self.test_flag = False  # Initial state

        self.title('Receiver App')
        self.geometry(f'{self.width}x{self.height}')
        self.resizable(False, False)
        self.configure(bg="#051B37")

        custom_font2 = ("Arial Black", 13, "bold")  # Label text
        custom_font4 = ("Arial Black", 13, "bold")  # Chat text

        # The same port as receiver arduino
        self.serial_port = 'COM6'
        self.baud_rate = 57600

        # Label
        self.label = Label(self, text='Receiver App')
        self.label.config(font=custom_font2, bg='#051B37', fg='white')
        self.label.pack()

        # Frame to hold the chat widget
        chat_frame = Frame(self)
        chat_frame.pack(side='top', anchor='n', padx=20, pady=20)

        self.chat_text = Text(chat_frame, height=21, width=70, wrap=tk.WORD)
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

        # Configure grid column and row weights to make the text area expand
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        # Configure drop-out menu
        self.menu = Menu(self, tearoff=0)
        self.config(menu=self.menu)

        # Add "Options" dropdown menu
        options_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Options", menu=options_menu)
        
        options_menu.add_command(label="Load Messages", command=self.read_previous)
        options_menu.add_checkbutton(label="Test Mode", command=self.toggle_test_flag)
        options_menu.add_separator()

        # Connect Arduino and start serial read in a separate thread
        self.connect_arduino()
        threading.Thread(target=self.serial_read).start()

    def toggle_test_flag(self):
        self.test_flag = not self.test_flag
        

    def connect_arduino(self):
        while True:
            try:
                self.arduino = serial.Serial(self.serial_port, self.baud_rate, timeout=10)
                break
            except serial.SerialException as e:
                print("Couldn't connect to Arduino")
                print("Error ", e)
                time.sleep(2) 
    
    def read_previous(self):
        if self.test_flag:
            self.chat_text.config(state='normal')
            f = open(r"messages.txt", "r")
            f.seek(0)
            for x in f:
                self.chat_text.insert(tk.END, x)
            f.close()
            self.chat_text.config(state='disabled')    

    def serial_read(self):
        while True:
            if self.arduino and self.arduino.in_waiting > 0:
                raw_data = self.arduino.readline()  
                data = raw_data.strip()
                path = ""
                if self.test_flag == False:
                    path = self.file_path
                else:
                    path = "binaryTest.txt"
                if data:
                    print(data.decode("utf-8"))
                    try:
                        with open(path, "ab") as file:
                            file.write(raw_data)  
                        if self.test_flag == False:
                            self.write_message(data.decode("utf-8"))
                    except Exception as e:
                        print(f"Error writing to file: {e}")

    def cut_bytes(self, input_string):
        new_length = len(input_string) - (len(input_string) % 8)
        cut_string = input_string[:new_length]
        return cut_string

    def write_message(self, message):
        try:
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S -> ")
            message = self.cut_bytes(message)
            binary_converter = Convert()
            message = binary_converter.binary_to_text(message)
            message = formatted_time + message

            # with open("messages.txt", "a") as file:
            #     file.write(message + "\n")

            # Insert the new message into the Tkinter Text widget
            self.chat_text.config(state='normal')
            self.chat_text.insert(tk.END, message + "\n")
            self.chat_text.config(state='disabled')
            self.chat_text.yview(tk.END)  # Scroll to the bottom to show the latest message

        except Exception as write_message_exception:
            print(f"Write Message Exception: {write_message_exception}")

if __name__ == "__main__":
    app = ReceiverApp()
    app.mainloop()

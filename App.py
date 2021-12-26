import sqlite3
import tkinter as tk
from os.path import exists
from initiate_db import initiate_db
from tkinter import ttk

class WelcomeFrame(ttk.Frame):
    def __init__(self, container, connection):
        super().__init__(container)

        #fetch all student
        self.welcome_cursor = connection.cursor()
        self.welcome_cursor.execute("SELECT * FROM students;")
        self.students_list = self.welcome_cursor.fetchall()
        self.students_list = {self.students_list[i][2]: self.students_list[i] for i in range(len(self.students_list))}

        #Initiate container variable for enter WelcomeFrame
        self.container = container

        #Label Instruction
        self.choose_instruction = ttk.Label(self, text="Pilih Siswa:")
        self.choose_instruction.pack(pady=10)

        #Choose Student ComboBox
        self.person_combobox = ttk.Combobox(self, state='readonly')
        self.person_combobox.pack()

        #ComboBox Inside
        self.person_combobox['values'] = [full_name for full_name in self.students_list.keys()]
        self.person_combobox.bind('<<ComboboxSelected>>', self.change_welcome_button_state)

        #button frame
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=10)
        
        #Choose Student Button
        self.choose_person_button_nd = ttk.Button(self.button_frame, text="Mulai Sesi Baru", command=lambda: self.move2deck(self.students_list[self.person_combobox.get()], True))
        self.choose_person_button_nd.pack()
        self.choose_person_button_nd["state"] = "disabled"
        self.choose_person_button_od = ttk.Button(self.button_frame, text="Mulai Sesi Lama", command=lambda: self.move2deck(self.students_list[self.person_combobox.get()], False))
        self.choose_person_button_od.pack(pady=5)
        self.choose_person_button_od["state"] = "disabled"
        
        #Pack frame to window
        self.pack(expand=True) 
    
    #Change button when combobox item selected function
    def change_welcome_button_state(self, event):
        if self.person_combobox.get():
            self.choose_person_button_nd["state"] = "normal"
            self.choose_person_button_od["state"] = "normal"
        else:
            self.choose_person_button_nd["state"] = "disabled"
            self.choose_person_button_od["state"] = "disabled"

    #Frame change (Welcome -> Deck) function
    def move2deck(self, student_tuple, decrease_days):
        self.destroy()
        DeckFrame(self.container, student_tuple, decrease_days)

class DeckFrame(ttk.Frame):
    def __init__(self, container, student_tuple, decrease_days):
        super().__init__(container)

        self.student_tuple = student_tuple
        # student_tuple = (id, nick_name, full_name, group_name, join_date)

        #fetch all student's deck name
        #self.deck_cursor = connection.cursor()
        #self.deck_cursor.execute("COMMAND")
        #self.deck_list = self.deck_cursor.fetchall()

        #Initiate container variable for enter DeckFrame
        self.container = container

        #Label Instruction
        self.greet = ttk.Label(self, text="Hi {}!".format(self.student_tuple[1]))
        self.greet.pack(pady=10)
        
        #Label Instruction
        self.choose_instruction = ttk.Label(self, text="Pilih Deck:")
        self.choose_instruction.pack(pady=10)

        #Deck Treeview
        self.columns = ("deck_name", "status")
        self.deck_tree = ttk.Treeview(self, columns=self.columns, show='headings')
        self.deck_tree.heading("deck_name", text="Nama Deck")
        self.deck_tree.heading("status", text="Status")
        self.deck_tree.pack(pady=10, expand=True)
        self.deck_tree.bind('<Button-1>', self.handle_manual_column_resize)
        self.deck_tree.bind('<Motion>', self.handle_manual_column_resize)

        #Choose Deck Button
        self.choose_deck_button = ttk.Button(self, text="Mulai Sesi")#, command=lambda: self.start_session(self.deck_combobox.get()))
        self.choose_deck_button.pack(pady=10)
        
        #Pack frame to window
        self.pack(expand=True)

    #Disable manual column resizing
    def handle_manual_column_resize(self, event):
        if self.deck_tree.identify_region(event.x, event.y) == "separator":
            return "break"
    
    #Frame change (Deck -> Session) function
    #def start_session(self):
    #    self.destroy()
    #    SessionFrame(self.container)

class SessionFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.student_tuple = student_tuple
        # student_tuple = (id, nick_name, full_name, group_name, join_date)

        #fetch all student's deck name
        #self.deck_cursor = connection.cursor()
        #self.deck_cursor.execute("COMMAND")
        #self.deck_list = self.deck_cursor.fetchall()

        #Initiate container variable for enter DeckFrame
        self.container = container

        #Label Instruction
        self.greet = ttk.Label(self, text="Hi {}!".format(self.student_tuple[1]))
        self.greet.pack(pady=10)
        
        #Label Instruction
        self.choose_instruction = ttk.Label(self, text="Pilih Deck:")
        self.choose_instruction.pack(pady=10)

        #Deck Treeview
        self.columns = ("deck_name", "status")
        self.deck_tree = ttk.Treeview(self, columns=self.columns, show='headings')
        self.deck_tree.heading("deck_name", text="Nama Deck")
        self.deck_tree.heading("status", text="Status")
        self.deck_tree.pack(pady=10, expand=True)
        self.deck_tree.bind('<Button-1>', self.handle_manual_column_resize)
        self.deck_tree.bind('<Motion>', self.handle_manual_column_resize)

        #Choose Deck Button
        self.choose_deck_button = ttk.Button(self, text="Mulai Sesi")#, command=lambda: self.start_session(self.deck_combobox.get()))
        self.choose_deck_button.pack(pady=10)
        
        #Pack frame to window
        self.pack(expand=True)
    
    #Frame change (Welcome -> Deck) function
    #def start_session(self, student_tuple, decrease_days):
    #    self.destroy()
    #    DeckFrame(self.container, student_tuple, decrease_days)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        #Window setting
        self.title('SRIG4SA')
        self.geometry('400x400')
        self.resizable(False, False)

if __name__ == "__main__":
    if not exists('data.db'):
        initiate_db()
    connection = sqlite3.connect('data.db')
    app = App()
    WelcomeFrame(app, connection)
    app.mainloop()
    connection.close()
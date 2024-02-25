import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import product


# UPDATE DIRECTORY PATH NOT WORKING !! fix that homes





class GUI:
    

    def __init__(self):
        self.WINDOW_WIDTH = 500
        self.WINDOW_HEIGHT = 500
        #conditions for translate button working
        self.file_selected = False
        self.directory_selected = False
        self.translating = False

        self.progress_bar_val = 0




        self.root = tk.Tk()
        self.root.title("Classical Chinese Translator")
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")

        self.label_title = tk.Label(self.root, text="Classical Chinese Translator V2")
        self.label_title.pack(anchor=tk.W)
        
        self.label_text = tk.Label(self.root, text="The purpose of this application is to allow the translation of Classical Chinese texts using OpenAI's AI translation tools. To make a translation, select a file, select a model, and finally click the translate button.", wraplength=self.WINDOW_WIDTH-10, justify=tk.LEFT)
        self.label_text.pack(anchor=tk.W)

        self.select_button = tk.Button(self.root, text = "Select file to translate", command=self.file_selection)
        self.select_button.pack(padx=10, pady=10, anchor=tk.W)

        self.destination_button = tk.Button(self.root, text = "Select destination folder", command=self.file_destination)
        self.destination_button.pack(padx=10, pady=10, anchor=tk.W)

        self.button = tk.Button(self.root, text="---TRANSLATE---", font=('Arial', 18), command=self.button_click)
        self.button.pack(padx=10, pady=10, anchor=tk.W)

        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=self.WINDOW_WIDTH, mode="determinate")
        self.progress_bar.pack(padx=10, pady=10)



        self.root.mainloop()

    def button_click(self):
        if self.file_selected is True and self.directory_selected is True and self.translating is False:
            self.translating = True

            print("Hello World")
            
            #product.translate_file(self.file_path, self.directory_path)
            
            # for i in range(100):
            #     self.progress_bar_val += 1
            #     self.progress_bar['value'] = self.progress_bar_val
            #     self.root.update_idletasks
    def update_progress_bar(self):
        self.progress_bar_val += 1
        self.progress_bar['value'] = self.progress_bar_val
        self.root.update_idletasks
                

    def file_selection(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            print("Selected file:", self.file_path)
            self.file_selected = True
            self.select_button.config(text=self.file_path)
        else:
            print("No file selected.")

    def file_destination(self):
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            print("Selected directory:", self.directory_path)
            self.directory_selected = True
            self.destination_button.config(text=self.directory_path)
            # Do something with the selected directory
        else:
            print("No directory selected.")



GUI()
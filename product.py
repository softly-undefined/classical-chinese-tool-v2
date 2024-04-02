import time
import subprocess, os
from openai import OpenAI
from tqdm import tqdm
from tkinter.filedialog import askopenfilename
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

DEBUG_MODE = True # will display the time taken for reading, translating, and file generation if True
USE_AI = True # will interact with the chosen AI model if True
CHUNK_SIZE = 100 #describes the number of characters per translated chunk
AI_MODEL = "gpt-3.5-turbo" # describes which OpenAI language model is being used
API_KEY = "" # input your OpenAI API key

# Eric Bennett, 1/7/24
#
# This program translates a given .txt document of Classical Chinese characters to English.
# The original document is read into a linked list of CHUNK_SIZE characters, which is then
# iterated through to translate into English, and then both the Chinese and English are 
# placed in a .txt document with markers for easy manuvering between Chinese and English.
#


client = OpenAI(api_key=API_KEY)

class GUI:
    

    def __init__(self):
        self.WINDOW_WIDTH = 500
        self.WINDOW_HEIGHT = 500
        #conditions for translate button working
        self.file_selected = False
        self.directory_selected = False
        self.translating = False
        self.aimodel = "gpt-3.5-turbo"
        


        def radio_button_selected():
            # Retrieve the selected value from the radio button variable
            selected_value = radio_var.get()
            self.aimodel = selected_value
            # Print the selected value
            print("Selected:", selected_value)


        self.root = tk.Tk()
        self.root.title("Classical Chinese Translator")
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")

        self.file_name = tk.StringVar()
        self.file_name.set("output")

        self.label_title = tk.Label(self.root, text="Classical Chinese Translator V2")
        self.label_title.pack(anchor=tk.W)
        
        self.label_text = tk.Label(self.root, text="The purpose of this application is to allow the translation of Classical Chinese texts using OpenAI's AI translation tools. To make a translation, select a file, select a model, change the output name if you want, and click the translate button.", wraplength=self.WINDOW_WIDTH-10, justify=tk.LEFT)
        self.label_text.pack(anchor=tk.W)

        self.save_button = tk.Entry(self.root, textvariable= self.file_name)
        self.save_button.pack()


        self.select_button = tk.Button(self.root, text = "Select file to translate", command=self.file_selection)
        self.select_button.pack(padx=10, pady=10, anchor=tk.W)

        self.destination_button = tk.Button(self.root, text = "Select destination folder", command=self.file_destination)
        self.destination_button.pack(padx=10, pady=10, anchor=tk.W)

        self.button = tk.Button(self.root, text="---TRANSLATE---", font=('Arial', 18), command=self.button_click)
        self.button.pack(padx=10, pady=10, anchor=tk.W)

        radio_var = tk.StringVar()

        radio_button1 = tk.Radiobutton(self.root, text="gpt-3.5-turbo", variable=radio_var, value="gpt-3.5-turbo", command=radio_button_selected)
        radio_button1.pack()

        radio_button2 = tk.Radiobutton(self.root, text="gpt-4              ", variable=radio_var, value="gpt-4", command=radio_button_selected)
        radio_button2.pack()

        self.root.mainloop()

        

    def button_click(self):
        if self.file_selected is True and self.directory_selected is True and self.translating is False:
            self.translating = True
            file_name = self.file_name.get()
            translate_file(self.file_path, self.directory_path, self.aimodel, file_name)
            self.translating = False
            
            # for i in range(100):
            #     self.progress_bar_val += 1
            #     self.progress_bar['value'] = self.progress_bar_val
            #     self.root.update_idletasks
                

    def file_selection(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            print("Selected file:", self.file_path)
            self.file_selected = True
            self.select_button.config(text=self.file_path)
        else:
            self.file_selected = False
            print("No file selected.")

    def file_destination(self):
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            print("Selected directory:", self.directory_path)
            self.directory_selected = True
            self.destination_button.config(text=self.directory_path)
            # Do something with the selected directory
        else:
            self.directory_selected = False
            print("No directory selected.")

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        #self.number = 0 # allows the nodes to see their indexes, not currently in use

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0 #represents total number of chunks (used for progress bar)

    def append(self, data):
        new_node = Node(data)
        self.length += 1
        #new_node.number = self.length
        if not self.head: #empty list
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

# takes the contents from the given file and puts every CHUNK_SIZE characters into a member of the linked list.
# does preprocessing to check if the document has consistent punctuation and splits the document using sentences
# instead of character lengths if that is true.
def list_from_file(file_path):
    if DEBUG_MODE: 
        start_time = time.time()
        print("-------------------------------------")
        print("begin reading file...")
    #.txt file preprocessing goes here 

    sentence_counter = 0
    char_counter = 0
    use_sentence = False

    with open(file_path, 'r') as file:
        for char in file.read():
            if char != '\n' and char != ' ':
                char_counter += 1
            if char == '。' or char == '!' or char == '?':
                sentence_counter += 1

    num_sentences = 0
    if (sentence_counter > 0):
        while (num_sentences*(char_counter/sentence_counter) < CHUNK_SIZE):
            num_sentences += 1
    
        if DEBUG_MODE:
            print("-------------------------------------")
            print("number of sentences: " + str(sentence_counter))
            print("number of characters: " + str(char_counter))
            print("avg char per sentence: " + str(char_counter/sentence_counter))
            print("num sentences per chunk size: " + str(num_sentences))
    
    

    # some analysis of whether it is worth it to use sentences needed here to decide if should flick on num_sentence

    # maybe do more analysis here? Right now if avg char/sentence is > 50 it will assume the document 
    # has inconsistent punctuation and use character CHUNK_SIZE based chunking instead of sentences.
    if (sentence_counter > 0):
        if (char_counter/sentence_counter < 50):
            use_sentence = True




    # reading chunks into linked_list
    linked_list = LinkedList()
    sentence_counter = 0

    with open(file_path, 'r') as file:
        chunk = ''
        
        for char in file.read():
            if char != '\n' and char != ' ':  # removes all spaces and new lines to hopefully save on some tokens
                if char == '。' or char == '!' or char == '?':
                    sentence_counter += 1
                chunk += char
            if (len(chunk) == CHUNK_SIZE and not use_sentence) or (use_sentence and num_sentences == sentence_counter):
                if linked_list.head is None:
                    linked_list.append(chunk)
                else:
                    linked_list.append(chunk)
                chunk = ''
                sentence_counter = 0
            
        if chunk:
            if linked_list.head is None:
                linked_list.append(chunk)
            else:
                linked_list.append(chunk)

    if DEBUG_MODE: 
        end_time = time.time()
        print(str(round(end_time - start_time)) + " seconds to read file")
        print("-------------------------------------")
    return linked_list

# creates a new "translated" linked list, iterating through the parameter
# untranslated text translating each chunk into English and placing the 
# result as a memnber of the new linked list.
def translate_list(untranslated_list, aimodel):
    if DEBUG_MODE: 
        print("begin translation...")
        start_time = time.time()

    translated_list = LinkedList()
    if untranslated_list.head is None:
        print("You gave an empty document!")
    else: #the list has elements within it
        traverse_node = untranslated_list.head
        with tqdm(total=untranslated_list.length) as pbar:
            while traverse_node is not None:
                translated_list.append(translate(traverse_node.data, aimodel))
                pbar.update(1) 
                traverse_node = traverse_node.next

    if DEBUG_MODE: 
        end_time = time.time()
        print(str(round(end_time - start_time)) + " seconds to complete translation")
    return translated_list



# takes a parameter string and uses the OpenAI API to translate it to English
# from Classical Chinese (if the USE_AI constant is set to True)
def translate(text, aimodel):
    if USE_AI:
        completion = client.chat.completions.create(
        model=aimodel,
        messages=[
            {
                "role": "system",
                "content": "You are an AI model trained to translate Classical Chinese to English, translate each given text to English"
            },
            {
                
                "role": "user",
                "content": text,
            },
        ],
        )
        return completion.choices[0].message.content
    else: 
        return "example translated text "




# takes the information stored in the untranslated and translated Linked Lists and 
# writes it to a .txt file, adding in markers [1p], [2p] throughout to allow for
# easy manuvering between the Chinese and the English translations.
def generate_txt(chinese_untranslated, english_translated, directory_path, aimodel, file_name):
    english_length = 0
    chinese_length = 0
    if DEBUG_MODE: 
        print("begin txt file generation...")
        start_time = time.time()

    write_path = os.path.join(directory_path, f"{file_name}.txt")
    if chinese_untranslated.head is not None and english_translated.head is not None:
        with open(write_path,"w") as file:

            file.write(f"Translation created with model: {aimodel} \n\n")


            #english section!!
            english_traverse_node = english_translated.head
            node_counter = 1
            while english_traverse_node is not None:
                file.write(english_traverse_node.data + '[' + str(node_counter) + "p]" + '\n')
                english_length += len(english_traverse_node.data)
                english_traverse_node = english_traverse_node.next
                node_counter +=1

            #intermediate section

            file.write("\n\nBelow is the original Chinese:\n\n\n")

            #chinese section!!
            chinese_traverse_node = chinese_untranslated.head
            node_counter = 1
            while chinese_traverse_node is not None:
                file.write(chinese_traverse_node.data + '[' + str(node_counter) + "p]" + '\n')
                chinese_length += len(chinese_traverse_node.data)
                chinese_traverse_node = chinese_traverse_node.next
                node_counter += 1

            if DEBUG_MODE: 
                print("\tEnglish characters: " + str(english_length))
                print("\tChinese length: " + str(chinese_length))
                print("\tTotal: " + str(chinese_length + english_length))
    else:
        print("your file is probably empty or something! Figure this out")

    if DEBUG_MODE:     
        end_time = time.time()
        print("-------------------------------------")
        print(str(round(end_time - start_time)) + " seconds to generate txt file")









# This will generate the pdf from the two linked lists which should
# already be created using translate_list and list_from_file
#12/28/23 Note that I am not using this for the moment too much processing time
# 1/6/24 poterntially use markdown instead? depends on if pdf generation is important
# CURRENTLY NOT IN USE BY THE PROGRAM
def generate_pdf(chinese_untranslated, english_translated):
    if DEBUG_MODE: 
        print("begin pdf generation...")
        start_time = time.time()
    if chinese_untranslated.head is not None and english_translated.head is not None:
        with open("output.tex","w") as file:
            #PREAMBLE
            file.write("\\documentclass{article}\n")
            file.write("\\usepackage[margin=1in]{geometry}\n")
            file.write("\\pagestyle{empty}\n")
            file.write("\\raggedright\n")
            file.write("\\sloppy\n")
            #file.write("\\usepackage{xeCJK}\n")

            file.write("\\begin{document}\n")

            #ENGLISH TRANSLATION SECTION
            print("\tbegin english section pdf generation...")
            english_traverse_node = english_translated.head
            node_counter = 1
            while english_traverse_node is not None:
                file.write(english_traverse_node.data + '[' + node_counter + "p]" + '\n') #adds the reference counter
                english_traverse_node = english_traverse_node.next
                node_counter += 1
                
                
            #print("\tfinished english pdf generation! contains " + str(english_length) + " characters")







            file.write("\n\n\nnow the chinese:\n\n\n")








            # Add the chinese to the document::
            # still need to figure out how to support chinese characters !!!!

            #styles['Normal'].fontName = "MingLiU"
            print("\tbegin chinese section pdf generation...")
            
            chinese_traverse_node = chinese_untranslated.head
            node_counter = 1
            while chinese_traverse_node is not None:
                file.write(chinese_traverse_node.data + '[' + node_counter + "p]" + '\n') #adds the reference counter
                chinese_traverse_node = chinese_traverse_node.next
                node_counter += 1
                

            #print("\tfinished chinese pdf generation! contains " + str(chinese_length) + " characters")



            file.write("\\end{document}\n")

        file_path = os.path.abspath("output.tex")
        child = subprocess.call(["pdflatex", file_path])
        if child != 0:
            print("Exit-code not 0, check result!")
    if DEBUG_MODE: 
        print("-------------------------------------")
        end_time = time.time()
        print(str(round(end_time - start_time)) + " seconds to generate pdf")

def translate_file(filepath, directory_path, aimodel, file_name):
    chinese_parse = list_from_file(filepath)
    english_translation = translate_list(chinese_parse, aimodel)
    generate_txt(chinese_parse, english_translation, directory_path, aimodel, file_name)





#actually doing things:


GUI()

#file_path = askopenfilename(title="Select the input .txt file containing Classical Chinese text: ")
#translate_file(file_path)
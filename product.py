from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import time
import subprocess, os

CHUNK_SIZE = 40
PRINT_SIZE = 500000
#chunk size * print size = section size (in characters)



class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.number = 0

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, data):
        new_node = Node(data)
        self.length += 1
        new_node.number = self.length
        if not self.head: #empty list
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
            

    def display(self):
        current_node = self.head
        while current_node:
            print(current_node.data)
            current_node = current_node.next

#takes the contents from the given file and puts every CHUNK_SIZE characters into a member of the linked list
def list_from_file(file_path):
    start_time = time.time()
    print("begin reading file...")
    #.txt file preprocessing goes here 

    # NEEDS TO BE ABLE TO DEAL WITH newline stuff !! rn it is calculated as a character?
    # what other preprocessing should be done ?


    # reading into linked_list
    linked_list = LinkedList()

    with open(file_path, 'r') as file:
        chunk = ''
        
        for char in file.read():
            chunk += char
            if len(chunk) == CHUNK_SIZE:
                #print("Here's one: ")
                #print(chunk)
                linked_list.append(chunk)
                chunk = ''
            
        if chunk:
            linked_list.append(chunk)
    end_time = time.time()
    print(str(round(end_time - start_time)) + " seconds to read file")
    return linked_list

def translate_list(untranslated_list):
    print("begin translation...")
    start_time = time.time()
    translated_list = LinkedList()
    if untranslated_list.head is None:
        print("You gave an empty document!")
    else:
        #the list has elements within it
        traverse_node = untranslated_list.head

        while traverse_node is not None:
            #translated_list.append(translate(traverse_node.data)) #adds the translated text to the translated list
            translated_list.append("example translated chunk")
            traverse_node = traverse_node.next

    #returns the list, now with translations
    end_time = time.time()
    print(str(round(end_time - start_time)) + " seconds to complete translation")
    return translated_list




def translate(text):
    translation = ''
    #here is where it should interact with the OpenAI API!







    return translation

# This will generate the pdf from the two linked lists which should
# already be created using translate_list and list_from_file
def generate_pdf(chinese_untranslated, english_translated):
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
            while english_traverse_node is not None:
                file.write(english_traverse_node.data + '\n')
                english_traverse_node = english_traverse_node.next
                
                
            #print("\tfinished english pdf generation! contains " + str(english_length) + " characters")







            file.write("\n\n\nnow the chinese:\n\n\n")








            # Add the chinese to the document::
            # still need to figure out how to support chinese characters !!!!

            #styles['Normal'].fontName = "MingLiU"
            print("\tbegin chinese section pdf generation...")
            
            chinese_traverse_node = chinese_untranslated.head
            while chinese_traverse_node is not None:
                file.write(chinese_traverse_node.data + '\n')
                chinese_traverse_node = chinese_traverse_node.next
                

            #print("\tfinished chinese pdf generation! contains " + str(chinese_length) + " characters")



            file.write("\\end{document}\n")

        file_path = os.path.abspath("output.tex")
        child = subprocess.call(["pdflatex", file_path])
        if child != 0:
            print("Exit-code not 0, check result!")
        end_time = time.time()
        print(str(round(end_time - start_time)) + " seconds to generate pdf")



#this grabs the info from the chinese-doc.txt document
chinese_parse = list_from_file("chinese-doc.txt") #make this a selectable file later on

english_translation = translate_list(chinese_parse)

#chinese_parse.display()
#english_translation.display()

generate_pdf(chinese_parse, english_translation)



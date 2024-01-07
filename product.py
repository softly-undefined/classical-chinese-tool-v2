import time
import subprocess, os
from openai import OpenAI
from tqdm import tqdm


DEBUG_MODE = False # will display the time taken for reading, translating, and file generation if True
USE_AI = True # will interact with the chosen AI model if True
CHUNK_SIZE = 100 #describes the number of characters per translated chunk
AI_MODEL = "gpt-3.5-turbo"
API_KEY = "YOUR_API_KEY"
#chunk size * print size = section size (in characters)

client = OpenAI(api_key=API_KEY)

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

#takes the contents from the given file and puts every CHUNK_SIZE characters into a member of the linked list
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
    while (num_sentences*(char_counter/sentence_counter) < CHUNK_SIZE):
        num_sentences += 1
    
    if DEBUG_MODE:
        print("-------------------------------------")
        print("number of sentences: " + str(sentence_counter))
        print("number of characters: " + str(char_counter))
        print("avg char per sentence: " + str(char_counter/sentence_counter))
        print("num sentences per chunk size: " + str(num_sentences))
    
    

    #some analysis of whether it is worth it to use sentences needed here to decide if should flick on num_sentence

    #maybe do more analysis here?
    if (char_counter/sentence_counter < 50):
        use_sentence = True



    #end section










    # reading into linked_list
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

def translate_list(untranslated_list):
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
                translated_list.append(translate(traverse_node.data))
                pbar.update(1) 
                traverse_node = traverse_node.next


    if DEBUG_MODE: 
        end_time = time.time()
        print(str(round(end_time - start_time)) + " seconds to complete translation")
    return translated_list




def translate(text):
    if USE_AI:
        completion = client.chat.completions.create(
        model=AI_MODEL,
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





def generate_txt(chinese_untranslated, english_translated):
    english_length = 0
    chinese_length = 0
    if DEBUG_MODE: 
        print("begin txt file generation...")
        start_time = time.time()
    if chinese_untranslated.head is not None and english_translated.head is not None:
        with open("output.txt","w") as file:

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

def translate_file(filepath):
    chinese_parse = list_from_file("chinese-doc.txt") #make this a selectable file later on
    english_translation = translate_list(chinese_parse)
    generate_txt(chinese_parse, english_translation)



translate_file("chinese-doc.txt")


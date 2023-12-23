import PyPDF2

CHUNK_SIZE = 50


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0

    def append(self, data):
        new_node = Node(data)
        self.length += 1
        if not self.head:
            self.head = new_node
        else:
            current_node = self.head
            while current_node.next:
                current_node = current_node.next
            current_node.next = new_node

    def display(self):
        current_node = self.head
        while current_node:
            print(current_node.data)
            current_node = current_node.next

#takes the contents from the given file and puts every 50 characters into a member of the linked list
def list_from_file(file_path):
    #NEEDS TO BE ABLE TO DEAL WITH newline stuff !! rn it is calculated as a character?



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
        
    return linked_list

def translate_list(untranslated_list):
    translated_list = LinkedList()
    if untranslated_list.head is None:
        print("You gave an empty document!")
    else:
        #the list has elements within it
        traverse_node = untranslated_list.head
        while traverse_node is not None:
            #translated_list.append(translate(traverse_node.data)) #adds the translated text to the translated list
            translated_list.append("an element!")
            traverse_node = traverse_node.next

    #returns the list, now with translations
    return translated_list

def translate(text):
    translation = ''
    #here is where it should interact with the OpenAI API







    return translation

# This will generate the pdf from the two linked lists which should
# already be created using translate_list and list_from_file
def generate_pdf(english_translated, chinese_untranslated):
    #This is where I need to do the stuff that interacts with the pypdf2 library
    with open("output.pdf", "wb") as output_file:
        pdf = PyPDF2.PdfFileWriter()
        pdf.addBlankPage()

        pdf.write(output_file)




    print("hello world!")




#this grabs the info from the chinese-doc.txt document
chinese_parse = list_from_file("chinese-doc.txt") #make this a selectable file later on

english_translation = translate_list(chinese_parse)

chinese_parse.display()
english_translation.display()



#generate_pdf(english_translation, chinese_parse)



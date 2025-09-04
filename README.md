# Classical Chinese Tool V2

This is the second iteration of a translation interface for batch translating Classical Chinese to English texts.

## Product.py

This is the main file to interact with the interface. This program translates a given .txt document of Classical Chinese characters to English. The original document is read into a linked list of CHUNK_SIZE characters, which is then iterated through to translate into English, and then both the Chinese and English are placed in a .txt document with markers for easy manuvering between Chinese and English.

## models.txt

This file provides a method to switch the current models without having to edit the code itself. This is an example of what one model looks like:

gpt-4.1|gpt-4.1 ($2.00 / 1M) (newest)

the model name is located to the left of the | character, to the right is a description that will be shown in the GUI.
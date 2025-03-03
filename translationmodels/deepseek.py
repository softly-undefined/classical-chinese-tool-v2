from langchain_ollama import ChatOllama
import os
import re

class DeepSeekTranslator:
    def __init__(self, model="deepseek-r1:7b", temperature=0):
        self.model = model
        self.temperature = temperature
        self.client = ChatOllama(model=self.model, temperature=self.temperature)

    def translate(self, text):
        try:
            response = self.client.invoke(f"Translate the following Classical Chinese text to English with a focus on accuracy. Only output the translation: {text}")
            final_answer = re.sub(r"<think>.*?</think>\s*", "", response.content, flags=re.DOTALL).strip()
            
            return final_answer #extracts just the actual text, skipping the thinking R1 does.
            #return response.content
        except Exception as e:
            print(f"Error during translation with DeepSeek: {e}")
            return None
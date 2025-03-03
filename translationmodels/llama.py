from langchain_ollama import ChatOllama
import os

class LlamaTranslator:
    def __init__(self, model="llama3.1", temperature=0):
        self.model = model
        self.temperature = temperature
        self.client = ChatOllama(model=self.model, temperature=self.temperature)

    def translate(self, text):
        try:
            response = self.client.invoke(f"Translate the following Classical Chinese text to English with a focus on accuracy, and no notes other than the translated text: {text}")
            return response.content  # Extracts text from the response
        except Exception as e:
            print(f"Error during translation with Llama: {e}")
            return None

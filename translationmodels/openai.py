from openai import OpenAI
import os

class OpenAITranslator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is missing. Set it as an environment variable or pass it as an argument.")
        
        self.client = OpenAI(api_key=self.api_key)

    def translate(self, text, model, max_tokens=1000, temperature=0):
        try:
            response = self.client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": "Translate the following Classical Chinese text to English with a focus on accuracy:"},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content  # Extract translated text
        except Exception as e:
            print(f"Error during translation: {e}")
            return None



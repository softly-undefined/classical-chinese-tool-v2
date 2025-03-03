import anthropic
import os

class AnthropicTranslator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key is missing. Set it as an environment variable or pass it as an argument.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def translate(self, text, model, max_tokens=1000, temperature=0):
        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system="Translate the following Classical Chinese text to English with a focus on accuracy. Only output the translation:",
                messages=[
                    {"role": "user", "content": [{"type": "text", "text": text}]}
                ]
            )
            return response.content[0].text  # Extract translated text
        except Exception as e:
            print(f"Error during translation: {e}")
            return None

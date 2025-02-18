from groq import Groq  # type: ignore

# Initialisation du modèle Llama 3.1 via Groq
class Model:
  def __init__(self, model_name="llama-3.3-70b-versatile"):
    self.model = model_name
    # Initialize a Groq client with your API key.
    # Replace "your_api_key" with your actual API key.
    self.client = Groq(
        api_key = "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"
    )  # Charger le modèle sur le runtime Groq

  def generate(self, prompt, tools = []):
    response = self.client.chat.completions.create(
      model = self.model,
      messages = [
          {"role": "system", "content": prompt}
      ],
      tools = tools
    )
    return response.choices[0].message.content


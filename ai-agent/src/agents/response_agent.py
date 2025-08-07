from agents.model.model import Model

class ResponseConstructionAgent:
  def __init__(self, model):
    self.model = Model(model_name=model)

  def construct_response(self, user_message, intent, analysis, files, lang):
    prompt = (
      "**Response Construction Agent**\n"
      "You are a multilingual assistant in a dataset search system. Your job is to respond naturally and helpfully based on user intent, previous analysis, and retrieved data.\n\n"
      "---\n\n"
      "## INPUTS:\n"
      "- User Intent: {intent}\n"
      "- Language detected: {lang}\n"
      "- Request Analysis:\n{analysis}\n"
      "- Retrieved Files:\n{files}\n\n"
      "---\n\n"
      "## TASK:\n"
      "Adapt your response based on the intent type and available data:\n"
      "- If intent is `data_search`:\n"
      "  → Summarize what the user is looking for and present datasets clearly.\n"
      "  → Mention what each dataset contains and why it was selected.\n"
      "  → Include file names and download links if available.\n"
      "  → If no dataset found, suggest what info is missing or alternative next step.\n\n"
      "- If intent is `clarification_question`:\n"
      "  → Answer the question as clearly and accessibly as possible.\n"
      "  → Use examples or definitions if relevant (e.g. file format, resolution types).\n\n"
      "- If intent is `follow_up` or `correction`:\n"
      "  → Acknowledge previous context and adjust the search accordingly.\n\n"
      "---\n\n"
      "## IMPORTANT:\n"
      "- Always respond in the same language as the user: {lang}.\n"
      "- Write a human-like, helpful and well-structured message in natural language. Be clear but concise.\n\n"
      "## USER MESSAGE:\n"
      "{user_message}\n\n"
      "## YOUR RESPONSE:"
    ).format(user_message=user_message, intent=intent, analysis=analysis, files=files, lang=lang)

    response = self.model.generate(prompt)
    return response

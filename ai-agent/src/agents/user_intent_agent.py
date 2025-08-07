from agents.model.model import Model
import json
import logging
import re
import langdetect # type: ignore
from iso639 import Lang # type: ignore

logger = logging.getLogger(__name__)

INTENT_CATEGORIES = [
  "data_search",
  "clarification_question",
  "follow_up",
  "chitchat",
  "gratitude",
  "correction",
  "general_question"
]

class UserIntentAgent:
  def __init__(self, model="llama-3.3-70b-versatile"):  # change selon ton provider
    self.model = Model(model_name=model)

  def detect_intent(self, user_message):
    detected_lang = self.detect_language(user_message)
    prompt = (
      "**Role**: You are an intent detection agent in a multi-agent data assistant system.\n\n"
      "**Task**: Given the user's message classify the user's intent.\n"
      "You must respond ONLY with a JSON object like this:\n"
      "{{\"intent\": \"<one of: data_search | clarification_question | follow_up | chitchat | gratitude | correction | general_question>\"}}\n\n"
      "**Examples**:\n"
      "- User: Hi, I'm looking for temperature anomalies in Europe in 2020 → intent: data_search\n"
      "- User: What resolutions are available for this kind of data? → intent: clarification_question\n"
      "- User: Thanks, that helps! → intent: gratitude"
      "- User: Can you be more specific about the dataset sources? → intent: follow_up\n"
      "- User: Sorry, I meant 2019 not 2020 → intent: correction\n"
      "- User: What is a netCDF file? → intent: general_question\n"
      "- User: How are you? → intent: chitchat\n\n"
      "**User message**: {user_message}\n"
      "Respond ONLY with a JSON object. Do not add explanations or comments."
    ).format(user_message=user_message)
    try:
      response = self.model.generate(prompt)
      logger.info("INTENT RAW: %s", response)
      match = re.search(r'\{.*\}', response.strip(), re.DOTALL)
      if match:
        json_block = match.group(0)
        parsed = json.loads(json_block)
        parsed["language"] = detected_lang
        logger.info("INTENT PARSED: %s", parsed)
        return parsed

      logger.warning("No JSON block found in LLM output.")
      return {"intent": "data_search", "lang": detected_lang}

    except Exception as e:
      logger.error("Intent detection failed: %s", e)
      return {"intent": "data_search", "lang": detected_lang}

  def detect_language(self, text):
    try:
      iso6391 = langdetect.detect(text)
      lang = Lang(iso6391)
      return lang.name
    except Exception as e:
      logger.warning("Language detection failed: %s", e)
      return "en"  # fallback default

from agents.model.model import Model

class QueryAnalystAgent:
  def __init__(self, model):
    self.model = Model(model_name=model)

  def process_query(self, user_query, intent, context, history, ontology):
    history_text = self.format_history(history)
    ontology_text = self.format_ontology(ontology)

    prompt = (
      "**INTERNAL AGENT: Query Analyst Agent**\n\n"
      "You are an internal reasoning agent for a data assistant system.\n"
      "You NEVER communicate directly with the user.\n\n"
      "---\n\n"
      "## GOAL:\n"
      "From the given user query, dialogue history, contextual data, and ontology:\n"
      "- Extract structured search criteria.\n"
      "- Use the ontology concepts to understand what is a dataset and its linked concepts.\n"
      "- Use the domain context which is relative to the user query.\n"
      "- Determine if the query is ready for dataset retrieval.\n"
      "- Suggest clarification questions if needed.\n"
      "- Provide notes to support dataset selection.\n\n"
      "---\n\n"
      "## INPUTS:\n"
      "- User Query: {query}\n"
      "- Intent Type: {intent}\n"
      "- Dialogue History: {messages}\n"
      "- Ontology Relative to Datasets Concepts and Properties: {ontology}\n"
      "- Domain Context: {context}\n"
      "---\n\n"
      "## RESPONSE FORMAT:\n\n"
      "### Extracted Criteria:\n"
      "- Theme / Topic: ...\n"
      "- Spatial coverage: ...\n"
      "- Temporal coverage: ...\n"
      "- Variable(s): ...\n"
      "- Format: ...\n"
      "- Producer: ...\n"
      "- Dataset / Source: ...\n\n"
      "### Detected User Intent:\n"
      "- data_search | clarification_question | correction | follow_up | general_inquiry | chitchat | gratitude\n\n"
      "### Missing / Ambiguous Information:\n"
      "- [List vague or missing parameters]\n\n"
      "### Suggested Follow-up Questions:\n"
      "- [One or two helpful questions to refine the request, if applicable]\n\n"
      "### Internal Notes for Dataset Matching:\n"
      "- [Keywords, concepts, hints for filtering/searching]\n\n"
      "### Action Strategy:\n"
      "- \"Proceed to dataset search (partial match allowed)\"\n"
      "- \"Ask user to clarify before continuing\"\n"
      "- \"Provide factual answer to a clarification\"\n"
      "- \"Friendly response, no data required\"\n"
      "- \"Wait for correction or additional input\"\n"
      "- \"Do NOT generate fake data or fabricate links.\"\n\n"
      "### Confidence Level:\n"
      "- High / Medium / Low"
    ).format(
      query=user_query,
      intent=intent,
      ontology=ontology_text,
      context=context,
      messages=history_text
    )

    analysis = self.model.generate(prompt)
    return analysis

  def format_history(self, messages, max_turns=3):
    """
    Transforme un historique de messages en texte utilisable dans un prompt d'agent.
    """
    cleaned = []
    recent_messages = messages[-max_turns:]

    for msg in recent_messages:
      role = "User" if msg["sender"] == "user" else "Bot"
      text = msg["text"].strip().replace("\n", " ").replace("  ", " ")
      cleaned.append(f"{role} : {text}")

    return "\n".join(cleaned)

  def format_ontology(self, ontology):
    def safe(val): return val or "N/A"

    def class_line(c):
      return f"- {safe(c['label'])}: {safe(c.get('description'))}"

    def prop_line(p):
      dom = safe(p.get('domain'))
      ran = safe(p.get('range'))
      label = safe(p['label'])
      desc = safe(p.get('description'))
      return f"- {label} ({dom} → {ran}): {desc}"

    sections = []

    if ontology.get("classes"):
      class_lines = "\n".join(class_line(c) for c in ontology["classes"])
      sections.append(f"### Classes\n{class_lines}")

    if ontology.get("objectProperties"):
      obj_lines = "\n".join(prop_line(p) for p in ontology["objectProperties"])
      sections.append(f"### Object Properties\n{obj_lines}")

    if ontology.get("dataProperties"):
      data_lines = "\n".join(prop_line(p) for p in ontology["dataProperties"])
      sections.append(f"### Data Properties\n{data_lines}")

    return "\n\n".join(sections)

import os
import json
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer, util, CrossEncoder
from bert_score import score

# ---------- Chargement des modèles ----------
embedder = SentenceTransformer("all-MiniLM-L6-v2")
nli_model = CrossEncoder("cross-encoder/nli-deberta-v3-base")

# ---------- Étape 1 : Proxy de pertinence ----------
def get_relevant_ids_proxy(query, retrieved_datasets, threshold=0.5):
  query_emb = embedder.encode(query, convert_to_tensor=True)
  relevant_ids = []
  for idx, dataset in enumerate(retrieved_datasets):
    text = dataset.get("description", "")
    if not text:
      continue
    dataset_emb = embedder.encode(text, convert_to_tensor=True)
    sim = util.cos_sim(query_emb, dataset_emb)
    if sim.item() >= threshold:
      relevant_ids.append(idx)
  return relevant_ids

# ---------- Étape 2 : Métriques IR ----------
def precision_at_k(relevant_ids, retrieved_ids, k):
  retrieved_k = retrieved_ids[:k]
  return len(set(retrieved_k) & set(relevant_ids)) / k if k > 0 else 0.0

def recall_at_k(relevant_ids, retrieved_ids, k):
  retrieved_k = retrieved_ids[:k]
  return len(set(retrieved_k) & set(relevant_ids)) / len(relevant_ids) if relevant_ids else 0.0

def mean_reciprocal_rank(relevant_ids, retrieved_ids):
  for rank, doc_id in enumerate(retrieved_ids, start=1):
    if doc_id in relevant_ids:
      return 1.0 / rank
  return 0.0

def average_precision(relevant_ids, retrieved_ids):
  score_val = 0.0
  hit_count = 0
  for rank, doc_id in enumerate(retrieved_ids, start=1):
    if doc_id in relevant_ids:
      hit_count += 1
      score_val += hit_count / rank
  return score_val / len(relevant_ids) if relevant_ids else 0.0

def ndcg_at_k(relevant_ids, retrieved_ids, k):
  def dcg(scores):
    return sum((2**rel - 1) / np.log2(idx+2) for idx, rel in enumerate(scores))
  scores = [1 if doc in relevant_ids else 0 for doc in retrieved_ids[:k]]
  ideal = sorted(scores, reverse=True)
  return dcg(scores) / dcg(ideal) if sum(ideal) > 0 else 0.0

# ---------- Étape 3 : BERTScore ----------
def compute_bertscore(candidates, references, lang="en"):
  P, R, F1 = score(candidates, references, lang=lang)
  return float(F1.mean())

# ---------- Étape 4 : NLI ----------
def nli_consistency(claim, evidence):
  pair = [(claim, evidence)]
  scores = nli_model.predict(pair)
  scores = F.softmax(torch.tensor(scores[0]), dim=0)
  return float(scores[-1])

# ---------- Étape 5 : Matching direct ----------
def match_reference(query, refs):
  for r in refs:
    if r["query"].strip().lower() == query.strip().lower():
      return r
  return None  # si non trouvé, on renvoie None

# ---------- Évaluation complète ----------
def evaluate_conversations(convo_dir, reference_file, output_csv="results_full_eval.csv", k=3):
  with open(reference_file, "r", encoding="utf-8") as f:
    reference_data = json.load(f)

  results = []

  for filename in os.listdir(convo_dir):
    print(f"Evaluation de la conversation : {filename}")
    if not filename.endswith(".json"):
      continue
    path = os.path.join(convo_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
      convo = json.load(f)

    messages = convo.get("messages", [])
    user_msg = next((m["text"] for m in messages if m["sender"] == "user"), None)
    bot_msg = next((m["text"] for m in messages if m["sender"] == "bot"), None)
    files = convo.get("files", [])

    if not user_msg or not bot_msg:
      continue

    ref_entry = match_reference(user_msg, reference_data)
    if not ref_entry:
      print(f"⚠️ Aucune référence trouvée pour {filename}")
      continue

    reference_response = ref_entry["reference_response"]

    # Proxy de pertinence
    relevant_ids = get_relevant_ids_proxy(user_msg, files, threshold=0.3)
    retrieved_ids = list(range(len(files)))

    # Calcul des métriques
    prec = precision_at_k(relevant_ids, retrieved_ids, k)
    rec = recall_at_k(relevant_ids, retrieved_ids, k)
    mrr = mean_reciprocal_rank(relevant_ids, retrieved_ids)
    ap = average_precision(relevant_ids, retrieved_ids)
    ndcg = ndcg_at_k(relevant_ids, retrieved_ids, k)
    bert = compute_bertscore([bot_msg], [reference_response])

    nli_scores = []
    for idx in relevant_ids:
      ds = files[idx]
      evidence = (ds.get("title", "") or "") + " " + (ds.get("description", "") or "")
      nli_scores.append(nli_consistency(bot_msg, evidence))
    nli_mean = np.mean(nli_scores) if nli_scores else 0.0

    results.append({
      "file": filename,
      "query": user_msg,
      "precision@k": prec,
      "recall@k": rec,
      "MRR": mrr,
      "AP": ap,
      "nDCG@k": ndcg,
      "BERTScore": bert,
      "NLI_consistency": nli_mean
    })

  df = pd.DataFrame(results)
  df.to_csv(output_csv, index=False)
  print(f"✅ Évaluation terminée — résultats enregistrés dans {output_csv}")
  return df

# ---------- Exécution ----------
if __name__ == "__main__":
  evaluate_conversations("conversations_eval", "eo_queries_200.json", output_csv="results_full_eval.csv", k=3)

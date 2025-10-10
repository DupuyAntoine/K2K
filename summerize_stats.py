import pandas as pd

def summarize_metrics(csv_file, output_summary="summary_stats.csv"):
  df = pd.read_csv(csv_file)

  # On isole uniquement les colonnes numériques (les métriques)
  metric_cols = [
    "precision@k",
    "recall@k",
    "MRR",
    "AP",
    "nDCG@k",
    "BERTScore",
    "NLI_consistency"
  ]
  df_metrics = df[metric_cols]

  # Calcul des stats principales
  summary = df_metrics.describe(percentiles=[0.25, 0.5, 0.75]).T
  summary.rename(columns={
    "mean": "Mean",
    "std": "Std",
    "min": "Min",
    "25%": "Q1",
    "50%": "Median",
    "75%": "Q3",
    "max": "Max"
  }, inplace=True)

  # Arrondi pour lisibilité
  summary = summary.round(4)

  # Sauvegarde CSV
  summary.to_csv(output_summary)
  print(f"📈 Statistiques globales enregistrées dans {output_summary}\n")
  print(summary)

  return summary

# Exemple d'utilisation :
if __name__ == "__main__":
  summarize_metrics("results_full_eval.csv", output_summary="summary_stats.csv")

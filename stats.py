import matplotlib.pyplot as plt
import numpy as np

# Moyennes extraites pour chaque modèle et chaque métrique (hors contextual relevancy)
models = ['LLaMA 3.3 70B', 'Mistral Saba 24B', 'Deepseek-R1 70B', 'Qwen 32B']
metrics = ['Answer Relevancy', 'Contextual Precision', 'Contextual Recall', 'Faithfulness']

# Ces valeurs sont issues des extractions précédentes
values = {
    'LLaMA 3.3 70B': [0.728, 0.891, 0.659, 0.722],
    'Mistral Saba 24B': [0.685, 0.825, 0.608, 0.716],
    'Deepseek-R1 70B': [0.735, 0.812, 0.618, 0.838],
    'Qwen 32B': [0.642, 0.934, 0.588, 0.783],
}

# Préparation des données pour le graphique
bar_width = 0.2
x = np.arange(len(metrics))

fig, ax = plt.subplots(figsize=(10, 6))

for i, model in enumerate(models):
    scores = values[model]
    ax.bar(x + i * bar_width, scores, width=bar_width, label=model)

# Mise en forme
ax.set_xlabel('Evaluation Metric')
ax.set_ylabel('Average Score')
ax.set_title('Comparison of LLM Agents by Metric')
ax.set_xticks(x + 1.5 * bar_width)
ax.set_xticklabels(metrics)
ax.set_ylim(0, 1.1)
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

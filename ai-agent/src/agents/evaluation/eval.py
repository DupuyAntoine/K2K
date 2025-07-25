from deepeval.test_case import LLMTestCase # type: ignore
from deepeval.metrics import ( # type: ignore
  ContextualRelevancyMetric,
  ContextualRecallMetric,
  ContextualPrecisionMetric,
  AnswerRelevancyMetric,
  FaithfulnessMetric
) 
from deepeval import evaluate # type: ignore


# Liste des requêtes de test et des attentes correspondantes
queries = [
    (
        "Quels jeux de données Sentinel-3 permettent d'analyser la température de surface des océans en 2023 ?",
        "Vérifier que le système sélectionne correctement les produits Sentinel-3 (SLSTR, OLCI) et explique leur résolution spatiale et temporelle."),
    (
        "Je veux étudier l’évolution du stock d’eau terrestre en France sur les 5 dernières années.",
        "Tester la récupération de données gravimétriques GRACE/GRACE-FO, humidité des sols SMOS, précipitations Météo-France et vérifier l’explication des liens entre ces données."
    ),
    (
        "Quels jeux de données sont disponibles pour analyser la concentration de CO₂ en France entre 2015 et 2023 ?",
        "Vérifier l’extraction correcte de Sentinel-5P (TROPOMI), OCO-2 et CAMS, et s’assurer que la justification mentionne leurs résolutions spatiales et spectrales."
    ),
    (
        "Je veux comparer l’évolution de la biomasse végétale et de l’humidité des sols en France. Quelles données puis-je utiliser ?",
        "Tester la combinaison de Sentinel-1 (radar biomasse), MODIS NDVI, SMOS humidité des sols et évaluer la clarté de la justification."
    ),
    (
        "Quels jeux de données Sentinel-2 et Landsat permettent de calculer l’évolution du NDVI en France depuis 2000 ?",
        "Vérifier la récupération des séries temporelles Sentinel-2 (depuis 2015) et Landsat (depuis 1982), et tester l’explication sur la pertinence des indices NDVI/EVI."
    ),
    (
        "Comment suivre l’évolution des anomalies de température en France ?",
        "Tester la récupération de données climatiques ERA5, MODIS LST, Météo-France, et s’assurer que la justification précise les échelles d’analyse."
    ),
    (
        "Quels jeux de données permettent d’étudier la relation entre précipitations et crues en France ?",
        "Vérifier la sélection de données satellites GPM/TRMM, hydrologiques Copernicus Climate Data Store, données in situ Vigicrues, et évaluer la pertinence des explications."
    ),
    (
        "Quels jeux de données Sentinel-5P permettent d’évaluer la pollution de l’air en France ?",
        "Vérifier la récupération des produits NO₂, SO₂, O₃, PM2.5 et s’assurer que l’explication couvre les limites et forces de ces données."
    ),
]

def run_tests(graph, iagent, eagent, ragent):
  print("Running tests...")
  results = []
  response_prompt = """La construction de la réponse est structurée de la façon suivante :
    **Agent de mise en forme des réponses**\n\n
    Tu es chargé de structurer et de formater la réponse pour l'utilisateur de manière claire et informative.\n\n

    **Données à traiter** :\n
    Jeux de données : [réponse de l'agent d'interaction]\n
    Fichiers extraits : [fichiers extraits]\n\n

    **Instructions** :\n
    1️ **Récapituler les critères de recherche** définis par l’utilisateur.\n
    2️ **Lister les jeux de données sélectionnés**, avec leurs noms et descriptions.\n
    3️ **Associer les fichiers disponibles** à chaque jeu de données, en indiquant leur nom et leur lien de téléchargement.\n
    4️ **Justifier pourquoi ces jeux de données ont été sélectionnés**, en se basant sur la requête de l'utilisateur.\n
    5️ **Adopter un ton clair et fluide**, en expliquant chaque élément pour assurer une bonne compréhension.\n\n
    **Critères de recherche récapitulés :**\n
    - **Thème** : [thème détecté]\n
    - **Période** : [période détectée]\n
    - **Zone géographique** : [zone géographique détectée]\n
    - **Autres filtres** : [autres critères éventuels]\n\n
    **Jeux de données sélectionnés :**\n
    [réponse de l'agent d'interaction]\n\n

    **Fichiers associés et téléchargements :**\n
    [fichiers extraits]\n\n

    **Justification de la sélection :**\n
    Ces jeux de données ont été sélectionnés car ils correspondent aux critères suivants...\n\n

    Fournis une réponse bien rédigée, informative et facile à lire."""

  for query, expected_answer in queries:
    i = 0
    while i < 25:
      iagent.context = []
      interaction = iagent.process_query(query, graph)
      files = eagent.extract_files(interaction, graph)
      response = ragent.construct_response(interaction, files)
      contextual_precision = ContextualPrecisionMetric()
      contextual_recall = ContextualRecallMetric()
      contextual_relevancy = ContextualRelevancyMetric()
      answer_relevancy = AnswerRelevancyMetric(threshold=0.8)
      faithfulness = FaithfulnessMetric()
      test_case = LLMTestCase(
      input=query,
      actual_output=response,
      expected_output=expected_answer + response_prompt,
      retrieval_context=[expected_answer, response_prompt],
      )

      evaluation = evaluate(test_cases=[test_case], metrics=[answer_relevancy, contextual_precision, contextual_recall, contextual_relevancy, faithfulness])

      with open("results_eval.txt", "a") as f:
        for test_result in evaluation.test_results:
            for metric_data in test_result.metrics_data:
              f.write(metric_data.name + " : " + str(metric_data.score) + "\n")

      results.append(evaluation)
      i += 1

  return results

def run_tests_noagent(graph, noagent):
  print("Running tests...")
  results = []
  i = 0
  while i < 25:
    for query, expected_answer in queries:
      response = noagent.generate_response(graph, query)
      contextual_precision = ContextualPrecisionMetric()
      contextual_recall = ContextualRecallMetric()
      answer_relevancy = AnswerRelevancyMetric(threshold=0.8)
      faithfulness = FaithfulnessMetric()
      test_case = LLMTestCase(
      input=query,
      actual_output=response,
      expected_output=expected_answer,
      retrieval_context=[graph, expected_answer],
      )
      evaluation = evaluate(test_cases=[test_case], metrics=[answer_relevancy, contextual_precision, contextual_recall, faithfulness])
      with open("results_eval.txt", "a") as f:
        for test_result in evaluation.test_results:
            for metric_data in test_result.metrics_data:
              f.write(metric_data.name + " : " + str(metric_data.score) + "\n")

      results.append(evaluation)
      i += 1

  return results

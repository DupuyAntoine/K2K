from deepeval.test_case import LLMTestCase # type: ignore
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric # type: ignore
from deepeval import evaluate # type: ignore

# Liste des requêtes de test et des attentes correspondantes
queries = [
    ("Quels jeux de données Sentinel-3 permettent d'analyser la température de surface des océans en 2023 ?", "Vérifier que le système sélectionne correctement les produits Sentinel-3 (SLSTR, OLCI) et explique leur résolution spatiale et temporelle."),
    ("Je veux étudier l’évolution du stock d’eau terrestre en France sur les 5 dernières années.", "Tester la récupération de données gravimétriques GRACE/GRACE-FO, humidité des sols SMOS, précipitations Météo-France et vérifier l’explication des liens entre ces données."),
    ("Quels jeux de données sont disponibles pour analyser la concentration de CO₂ en France entre 2015 et 2023 ?", "Vérifier l’extraction correcte de Sentinel-5P (TROPOMI), OCO-2 et CAMS, et s’assurer que la justification mentionne leurs résolutions spatiales et spectrales."),
    ("Je veux comparer l’évolution de la biomasse végétale et de l’humidité des sols en France. Quelles données puis-je utiliser ?", "Tester la combinaison de Sentinel-1 (radar biomasse), MODIS NDVI, SMOS humidité des sols et évaluer la clarté de la justification."),
    ("Quels jeux de données Sentinel-2 et Landsat permettent de calculer l’évolution du NDVI en France depuis 2000 ?", "Vérifier la récupération des séries temporelles Sentinel-2 (depuis 2015) et Landsat (depuis 1982), et tester l’explication sur la pertinence des indices NDVI/EVI."),
    ("Comment suivre l’évolution des anomalies de température en France ?", "Tester la récupération de données climatiques ERA5, MODIS LST, Météo-France, et s’assurer que la justification précise les échelles d’analyse."),
    ("Quels jeux de données permettent d’étudier la relation entre précipitations et crues en France ?", "Vérifier la sélection de données satellites GPM/TRMM, hydrologiques Copernicus Climate Data Store, données in situ Vigicrues, et évaluer la pertinence des explications."),
    ("Quels jeux de données Sentinel-5P permettent d’évaluer la pollution de l’air en France ?", "Vérifier la récupération des produits NO₂, SO₂, O₃, PM2.5 et s’assurer que l’explication couvre les limites et forces de ces données."),
]

def run_tests(graph, iagent, eagent, ragent):
    results = []
    for query, expected_keywords in queries:
        interaction = iagent.process_query(query, graph)
        files = eagent.extract_files(interaction, graph)
        response = ragent.construct_response(interaction, files)
        test_case = LLMTestCase(
          input=query,
          actual_output=response,
          expected_output=expected_keywords
        )
        evaluation = evaluate(test_cases=[test_case], metrics=[AnswerRelevancyMetric()])
        results.append(evaluation)
        print(f"Test pour la requête '{query}' : {evaluation}")
    return results

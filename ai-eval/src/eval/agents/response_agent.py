from agents.model.model import Model

class ResponseConstructionAgent:
    def __init__(self, model):
        self.model = Model(model_name=model)

    def construct_response(self, interaction_response, extracted_files):
        """
        Construit la réponse utilisateur avec les jeux de données et leurs fichiers associés.
        
        :param data_results: Résultats des jeux de données sélectionnés
        :param graph: Graphe RDF contenant les fichiers associés
        :param interaction_response: Réponse générée par l'agent d'interaction
        :return: Réponse formatée avec fichiers et explications
        """

        # 🔍 Étape 1 : Extraction des fichiers liés aux jeux de données

        # 📌 Création du prompt mis à jour
        prompt = (
            "**Agent de mise en forme des réponses**\n\n"
            "Tu es chargé de structurer et de formater la réponse pour l'utilisateur de manière claire et informative.\n\n"
            
            "**Données à traiter** :\n"
            "Jeux de données : {interaction_response}\n"
            "Fichiers extraits : {extracted_files}\n\n"
            
            "**Instructions** :\n"
            "1️ **Récapituler les critères de recherche** définis par l’utilisateur.\n"
            "2️ **Lister les jeux de données sélectionnés**, avec leurs noms et descriptions.\n"
            "3️ **Associer les fichiers disponibles** à chaque jeu de données, en indiquant leur nom et leur lien de téléchargement.\n"
            "4️ **Justifier pourquoi ces jeux de données ont été sélectionnés**, en se basant sur la requête de l'utilisateur.\n"
            "5️ **Adopter un ton clair et fluide**, en expliquant chaque élément pour assurer une bonne compréhension.\n\n"

            "**Critères de recherche récapitulés :**\n"
            "- **Thème** : [thème détecté]\n"
            "- **Période** : [période détectée]\n"
            "- **Zone géographique** : [zone géographique détectée]\n"
            "- **Autres filtres** : [autres critères éventuels]\n\n"

            "**Jeux de données sélectionnés :**\n"
            "{interaction_response}\n\n"
            
            "**Fichiers associés et téléchargements :**\n"
            "{extracted_files}\n\n"
            
            "**Justification de la sélection :**\n"
            "Ces jeux de données ont été sélectionnés car ils correspondent aux critères suivants...\n\n"
            
            "Fournis une réponse bien rédigée, informative et facile à lire."
        ).format(interaction_response=interaction_response, extracted_files=extracted_files)

        response = self.model.generate(prompt)
        return response

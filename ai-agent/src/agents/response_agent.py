from agents.model.model import Model

class ResponseConstructionAgent:
    def __init__(self, model):
        self.model = Model(model_name=model)

    def construct_response(self, analysis, files):
        """
        Construit la réponse utilisateur avec les jeux de données et leurs fichiers associés.
        
        :param analysis: Résultats de l'analyse du QueryAnalystAgent
        :param files: Résultats des fichiers identifiés par le DataIdentificationAgent
        :return: Réponse formatée avec fichiers et explications
        """

        # 🔍 Étape 1 : Extraction des fichiers liés aux jeux de données

        # 📌 Création du prompt mis à jour
        prompt = (
            "**Agent de mise en forme des réponses**\n\n"
            "Tu es chargé de structurer et de formater la réponse pour l'utilisateur de manière claire et informative.\n"

            "**Données à traiter** :\n"
            "Analyse de la demande et proposition de données d'intérêt : {analysis}\n"
            "Fichiers extraits : {files}\n\n"
            
            "**Instructions** :\n"
            "1️ **Récapituler les critères de recherche** définis par l’utilisateur.\n"
            "2️ **Analyser la demande de l'utilisateur et lister les jeux de données sélectionnés**, avec leurs noms et descriptions.\n"
            "3️ **Associer les fichiers disponibles** à chaque jeu de données, en indiquant leur nom et leur lien de téléchargement.\n"
            "4️ **Justifier pourquoi ces jeux de données ont été sélectionnés**, en se basant sur la requête de l'utilisateur.\n"
            "5️ **Adopter un ton clair et fluide**, en expliquant chaque élément pour assurer une bonne compréhension.\n\n"

            "**Critères de recherche récapitulés :**\n"
            "- **Thème** : [thème détecté]\n"
            "- **Période** : [période détectée]\n"
            "- **Zone géographique** : [zone géographique détectée]\n"
            "- **Autres filtres** : [autres critères éventuels]\n\n"
            "Il s'agit d'exemples, si l'analyse indique d'autres critères, fais les apparaître.\n\n"

            "**Analyse de la demande et proposition de données d'intérêt :**\n"
            "{analysis}\n\n"
            
            "**Fichiers associés et téléchargements :**\n"
            "{files}\n\n"
            
            "**Justification de la sélection :**\n"
            "Ces jeux de données ont été sélectionnés car ils correspondent aux critères suivants...\n\n"
            
            "Fournis une réponse bien rédigée, informative et facile à lire."
        ).format(analysis=analysis, files=files)

        response = self.model.generate(prompt)
        return response

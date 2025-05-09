from agents.model.model import Model

class FileExtractionAgent:
    def __init__(self, model):
        self.model = Model(model_name=model)

    def extract_files(self, interaction_response, graph):
        """
        Analyse le graphe RDF et extrait les fichiers pertinents en fonction de la réponse de l'agent d'interaction.

        :param graph: Graphe RDF contenant les jeux de données et fichiers associés
        :param interaction_response: Réponse de l'agent d'interaction (texte)
        :return: Liste des fichiers avec leurs noms et URLs
        """

        prompt = (
            "**Agent d'extraction de fichiers**\n\n"
            "Tu es spécialisé dans l'extraction de fichiers associés aux jeux de données. "
            "À partir du graphe RDF fourni, identifie les fichiers pertinents en fonction de la requête traitée.\n\n"
            
            "**Données à analyser** :\n"
            "Graphe RDF : {graph}\n"
            "Réponse de l'agent d'interaction : '{interaction_response}'\n\n"

            "**Processus d'extraction** :\n"
            "1️- Identifier les jeux de données mentionnés dans la réponse de l'agent d'interaction.\n"
            "2️- Lister les fichiers associés à ces jeux de données.\n"
            "3️- Extraire les noms des fichiers et leurs URLs de téléchargement.\n\n"

            "Fournis une liste formatée avec le nom du fichier et son lien de téléchargement."
        ).format(graph=graph, interaction_response=interaction_response)

        files = self.model.generate(prompt)
        return files

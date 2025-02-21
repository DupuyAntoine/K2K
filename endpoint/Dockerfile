FROM tenforce/virtuoso:latest

# Copier le dossier contenant les ontologies dans le conteneur
COPY ontologies/ /data/ontologies/

# Copier le script d'initialisation dans le dossier prévu à cet effet
COPY load_ontologies.sh /docker-entrypoint-initdb.d/load_ontologies.sh
RUN chmod +x /docker-entrypoint-initdb.d/load_ontologies.sh

# Exposer le port du SPARQL endpoint et le port isql pour l'administration
EXPOSE 8890 1111

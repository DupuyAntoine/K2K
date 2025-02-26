FROM openlink/virtuoso-opensource-7

# Définir la variable d'environnement
ENV DBA_PASSWORD=dba

# Copier le contenu local dans l'image
COPY data/ /database/data/
COPY scripts/ /opt/virtuoso-opensource/initdb.d/

# Exposer les ports utilisés par Virtuoso
EXPOSE 1111 8890

# La commande de démarrage est déjà définie dans l'image de base

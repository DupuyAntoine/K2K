#!/bin/bash
echo "Loading..."

# Attendre quelques secondes pour que Virtuoso soit opérationnel
sleep 10

# Charger tous les fichiers du dossier des ontologies dans le graphe spécifié
isql-v 1111 <<EOF
ld_dir_all('/data/ontologies', '*', 'http://k2000.org/ontology');
rdf_loader_run();
exit;
EOF

echo "Ontologies loaded."

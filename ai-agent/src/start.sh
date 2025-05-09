#!/bin/bash

echo "Configuration de DeepEval avec le modèle local..."
python setup_deepeval.py

echo "Lancement de l’application Flask..."
exec python main.py

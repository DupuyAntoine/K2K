# K2K

Ce projet intègre un frontend en React, un backend en Node.js, des agents IA (application Flask), ainsi qu'un endpoint SPARQL Virtuoso pour la gestion des ontologies.

## Prérequis

Avant d'installer et de lancer le projet, assurez-vous d'avoir les éléments suivants installés :

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Node.js](https://nodejs.org/) (Recommandé : v18+)
- [Yarn](https://yarnpkg.com/) ou npm

## Installation

### 1. Cloner le projet
```sh
git clone https://github.com/DupuyAntoine/K2K.git
cd K2K
```

### 2. Configuration des variables d'environnement
Créez un fichier `.env` à la racine du projet et ajoutez-y les variables nécessaires pour chaque module (remplacez les valeurs par vos propres paramètres) :

```env
#########################
### Agents Settings   ###
#########################

AGENT_URL=http://ai-agent:5000
GROQ_API_KEY=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

#########################
### Endpoint Settings ###
#########################

ENDPOINT_URL=http://endpoint:8890/sparql/
```

### 3. Démarrage des services avec Docker

Tous les services (backend, frontend, agents IA, Virtuoso) sont gérés via **Docker Compose**.

```sh
docker-compose up --build
```

> **Remarque :** Le premier démarrage peut prendre du temps, car les images doivent être construites et les dépendances installées.

### 4. Accéder aux différents services

| Service       | URL                              |
|--------------|---------------------------------|
| Frontend     | [http://localhost:3000](http://localhost:3000) |
| Backend      | [http://localhost:4000](http://localhost:4000) |
| Agents IA    | [http://localhost:5000](http://localhost:5000) |
| SPARQL (Virtuoso) | [http://localhost:8890](http://localhost:8890) |

## Développement et Mise à Jour

### Démarrer le backend et le frontend en mode développement
Si vous souhaitez travailler sur le frontend ou le backend sans Docker, démarrez-les manuellement :

#### Backend (Node.js)
```sh
cd backend
yarn install  # ou npm install
yarn start    # ou npm start
```

#### Frontend (React)
```sh
cd frontend
yarn install  # ou npm install
yarn dev      # ou npm run dev
```

## Arrêter et nettoyer les conteneurs

### Arrêter les services
```sh
docker-compose down
```

### Supprimer les volumes (Attention : supprime les données stockées)
```sh
docker-compose down -v
```

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d’informations.


# Étape 1 : Construction de l'application avec Node
FROM node:18-alpine AS builder
WORKDIR /app

# Copier les fichiers de configuration et installer les dépendances
COPY package*.json ./
RUN npm install

# Copier le reste de l'application et lancer la construction
COPY . .
RUN npm run build

# Étape 2 : Serveur de production avec Nginx
FROM nginx:alpine
# Copier les fichiers générés par Vite (généralement dans le dossier "dist")
COPY --from=builder /app/dist /usr/share/nginx/html

# Exposer le port 80
EXPOSE 80

# Lancer Nginx
CMD ["nginx", "-g", "daemon off;"]

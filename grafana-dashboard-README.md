# Dashboard Grafana pour SEMJUST

Ce document explique comment configurer et utiliser le dashboard Grafana pour visualiser les données de distribution des semences dans le projet SEMJUST.

## Prérequis

- Docker et Docker Compose installés
- L'application SEMJUST en cours d'exécution avec les services Prometheus et Grafana
- Des données de test chargées dans la base de données PostgreSQL

## Configuration du Dashboard

### Étape 1: Accéder à Grafana

1. Assurez-vous que tous les services sont en cours d'exécution avec Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. Accédez à l'interface Grafana à l'adresse suivante:
   ```
   http://localhost:3000
   ```

3. Connectez-vous avec les identifiants par défaut:
   - Utilisateur: `admin`
   - Mot de passe: `admin`

### Étape 2: Configurer la source de données Prometheus

1. Dans le menu latéral, cliquez sur "Configuration" (icône d'engrenage) puis "Data sources"
2. Cliquez sur "Add data source"
3. Sélectionnez "Prometheus"
4. Configurez la source de données avec les paramètres suivants:
   - Name: `prometheus`
   - URL: `http://prometheus:9090`
   - Access: `Server (default)`
5. Cliquez sur "Save & Test" pour vérifier la connexion

### Étape 3: Importer le Dashboard

1. Dans le menu latéral, cliquez sur "+" puis "Import"
2. Cliquez sur "Upload JSON file"
3. Sélectionnez le fichier `grafana-dashboard.json` créé précédemment
4. Assurez-vous que la source de données Prometheus est sélectionnée
5. Cliquez sur "Import"

## Utilisation du Dashboard

Le dashboard SEMJUST comprend plusieurs visualisations pour analyser la distribution des semences:

### 1. Allocation de semences par type

Ce graphique montre la quantité totale de chaque type de semence (mil, maïs, arachide, riz) allouée dans l'ensemble du pays.

### 2. Allocation par région

Ce graphique à barres montre la quantité totale de semences allouée à chaque région du Sénégal.

### 3. Carte des allocations

Cette carte interactive montre la distribution géographique des allocations de semences. Chaque point représente un département, et la taille du point est proportionnelle à la quantité de semences allouée.

### 4. Répartition par type de semence

Ce graphique en camembert montre la répartition des allocations par type de semence en pourcentage du total.

### 5. Allocation par département (Top 3 régions)

Ce graphique à barres montre les allocations détaillées par département et par type de semence pour les trois principales régions (Dakar, Thiès, Saint-Louis).

## Personnalisation

Vous pouvez personnaliser le dashboard selon vos besoins:

1. Pour modifier une visualisation, cliquez sur le titre du panneau puis sur "Edit"
2. Pour ajouter un nouveau panneau, cliquez sur "Add panel" en haut à droite
3. Pour modifier la plage de temps, utilisez le sélecteur de temps en haut à droite

## Dépannage

Si les données ne s'affichent pas correctement:

1. Vérifiez que Prometheus est correctement configuré pour collecter les métriques de l'API
2. Assurez-vous que les données de test ont été chargées dans la base de données
3. Vérifiez les logs de Prometheus et Grafana pour détecter d'éventuelles erreurs

```bash
docker-compose logs prometheus
docker-compose logs grafana
```

4. Vérifiez que les métriques sont disponibles dans Prometheus en accédant à:
   ```
   http://localhost:9090/graph
   ```
   Et en recherchant `allocation_quantity` dans la barre de recherche.
#!/bin/bash

# Script pour redémarrer les services après les modifications de configuration

echo "Redémarrage des services Prometheus et Grafana..."

# Arrêter les services
echo "Arrêt des services..."
docker-compose stop prometheus grafana

# Redémarrer les services
echo "Redémarrage des services..."
docker-compose up -d prometheus grafana

# Attendre que Grafana soit disponible
echo "Attente du démarrage de Grafana..."
until curl -s http://localhost:3000 > /dev/null; do
    echo "Attente du démarrage de Grafana..."
    sleep 5
done

# Importer les dashboards
echo "Importation des dashboards..."
./import-dashboard.sh

echo "Services redémarrés avec succès!"
echo ""
echo "=== INSTRUCTIONS POUR ACCÉDER AUX DASHBOARDS ==="
echo "1. Accédez à Grafana à l'adresse: http://localhost:3000"
echo "2. Connectez-vous avec les identifiants par défaut: admin/admin"
echo "3. Allez dans le menu 'Dashboards' pour voir les dashboards disponibles"
echo ""
echo "Si les dashboards n'ont pas été importés automatiquement, suivez ces étapes:"
echo "1. Dans Grafana, allez dans 'Dashboards' > 'Import'"
echo "2. Cliquez sur 'Upload JSON file' et sélectionnez:"
echo "   - grafana-dashboard.json (pour le dashboard principal)"
echo "   - grafana-alerts-dashboard.json (pour le dashboard d'alertes)"
echo "3. Sélectionnez 'prometheus' comme source de données"
echo "4. Cliquez sur 'Import'"
echo ""
echo "=== VÉRIFICATION DES ALERTES ==="
echo "Pour vérifier les alertes configurées dans Prometheus:"
echo "1. Accédez à Prometheus à l'adresse: http://localhost:9090"
echo "2. Allez dans 'Alerts' pour voir les alertes configurées"
echo "3. Consultez le dashboard 'SEMJUST - Alertes et Équité' dans Grafana"
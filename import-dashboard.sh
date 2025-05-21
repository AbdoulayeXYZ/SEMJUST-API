#!/bin/bash

# Script pour importer automatiquement le dashboard Grafana

echo "Importation du dashboard Grafana pour SEMJUST..."

# Vérifier que Grafana est en cours d'exécution
echo "Vérification de la disponibilité de Grafana..."
until curl -s http://localhost:3000 > /dev/null; do
    echo "Attente du démarrage de Grafana..."
    sleep 5
done

# Attendre quelques secondes supplémentaires pour s'assurer que Grafana est prêt
sleep 5

# Créer un fichier de configuration temporaire pour curl avec les identifiants
CURL_CONFIG_FILE=$(mktemp)
echo "user = \"admin:admin\"" > $CURL_CONFIG_FILE

# Vérifier si la source de données Prometheus existe déjà
echo "Vérification de la source de données Prometheus..."
DATASOURCE_EXISTS=$(curl -s -K $CURL_CONFIG_FILE http://localhost:3000/api/datasources/name/prometheus)

# Si la source de données n'existe pas, la créer
if [[ $DATASOURCE_EXISTS == *"Data source not found"* ]]; then
    echo "Création de la source de données Prometheus..."
    curl -X POST -H "Content-Type: application/json" -K $CURL_CONFIG_FILE -d '{
        "name":"prometheus",
        "type":"prometheus",
        "url":"http://prometheus:9090",
        "access":"proxy",
        "basicAuth":false
    }' http://localhost:3000/api/datasources
else
    echo "La source de données Prometheus existe déjà."
fi

# Importer le dashboard
echo "Importation du dashboard..."
DASHBOARD_JSON=$(cat grafana-dashboard.json)

# Tenter d'importer le dashboard avec authentification
IMPORT_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -K $CURL_CONFIG_FILE -d "{
    \"dashboard\": $DASHBOARD_JSON,
    \"overwrite\": true,
    \"inputs\": [{
        \"name\": \"DS_PROMETHEUS\",
        \"type\": \"datasource\",
        \"pluginId\": \"prometheus\",
        \"value\": \"prometheus\"
    }]
}" http://localhost:3000/api/dashboards/import)

# Vérifier si l'importation a réussi ou échoué
if [[ $IMPORT_RESPONSE == *"Invalid username or password"* ]]; then
    echo "AVERTISSEMENT: Problème d'authentification lors de l'importation du dashboard."
    echo "Vous devrez peut-être importer manuellement le dashboard via l'interface Grafana."
    echo "1. Accédez à Grafana: http://localhost:3000"
    echo "2. Connectez-vous avec les identifiants admin/admin"
    echo "3. Allez dans Dashboards > Import"
    echo "4. Chargez le fichier grafana-dashboard.json"
    echo "5. Sélectionnez la source de données 'prometheus'"
    echo "6. Cliquez sur 'Import'"
else
    echo "Dashboard importé avec succès!"
fi

# Supprimer le fichier de configuration temporaire
rm $CURL_CONFIG_FILE

echo "Accédez à votre dashboard à l'adresse: http://localhost:3000/d/semjust-seeds/semjust-distribution-des-semences"
# Vérifie si Docker est installé
try {
    docker --version
    Write-Host "Docker est installé." -ForegroundColor Green
} catch {
    Write-Host "Docker n'est pas installé. Veuillez installer Docker." -ForegroundColor Red
    exit 1
}

# Vérifie si le fichier docker-compose.yml existe
if (-Not (Test-Path "./docker-compose.yml")) {
    try {
        # Télécharge le fichier docker-compose.yml
        Write-Host "Téléchargement de docker-compose.yml depuis GitHub..."
        Invoke-WebRequest -Uri "https://github.com/milvus-io/milvus/releases/download/v2.4.0-rc.1/milvus-standalone-docker-compose.yml" -OutFile "docker-compose.yml"
        Write-Host "Le fichier docker-compose.yml a été téléchargé avec succès." -ForegroundColor Green
    } catch {
        Write-Host "Échec du téléchargement du fichier docker-compose.yml." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Le fichier docker-compose.yml existe déjà." -ForegroundColor Green
}

# Vérifie si l'application Docker est déjà en cours d'exécution
try {
    $runningContainers = docker-compose ps -q
    if ($runningContainers) {
        Write-Host "L'application Docker est déjà en cours d'exécution." -ForegroundColor Green
    } else {
        # Lance Docker Compose
        Write-Host "Lancement de Docker Compose..."
        docker-compose up -d
        Write-Host "Docker Compose a démarré les conteneurs avec succès." -ForegroundColor Green
    }
} catch {
    Write-Host "Échec lors de la vérification ou du démarrage des conteneurs Docker." -ForegroundColor Red
    exit 1
}

# Vérifie si pip est installé
try {
    pip --version
    Write-Host "Pip est installé." -ForegroundColor Green
} catch {
    Write-Host "Pip n'est pas installé. Veuillez installer pip." -ForegroundColor Red
    exit 1
}

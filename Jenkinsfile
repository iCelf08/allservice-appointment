pipeline {
    agent any

    environment {
        PROJECT_DIR = "${WORKSPACE}"  // Le répertoire de travail de Jenkins où le projet est cloné
        VENV_DIR = "${PROJECT_DIR}/venv"
        DJANGO_SETTINGS_MODULE = 'PriseRendez.settings.production'  // Remplace par ton module de settings Django
        POSTGRES_IMAGE = 'postgres:latest'
        POSTGRES_CONTAINER_NAME = 'pgsql-dev'
        POSTGRES_USER = 'postgres'
        POSTGRES_PASSWORD = '123456'
        POSTGRES_DB = 'allservice_db'
        POSTGRES_PORT = '5432'
    }

    stages {
        stage('Checkout') {
            steps {
                // Cloner le projet depuis GitHub
                git branch: 'master', url: 'https://github.com/iCelf08/allservice-appointment.git'
            }
        }

        stage('Start PostgreSQL Container') {
            steps {
                script {
                    // Démarrer le conteneur PostgreSQL
                    sh """
                    docker run --name ${POSTGRES_CONTAINER_NAME} -e POSTGRES_USER=${POSTGRES_USER} \
                    -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -e POSTGRES_DB=${POSTGRES_DB} \
                    -p ${POSTGRES_PORT}:${POSTGRES_PORT} -d ${POSTGRES_IMAGE}
                    """
                    // Attendre que PostgreSQL démarre
                    sh 'sleep 10'
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    // Créer et activer l'environnement virtuel
                    sh 'python3 -m venv ${VENV_DIR}'
                    sh '. ${VENV_DIR}/bin/activate'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Installer les dépendances Python depuis requirements.txt
                    sh '. ${VENV_DIR}/bin/activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Run Migrations') {
            steps {
                script {
                    // Appliquer les migrations
                    sh '. ${VENV_DIR}/bin/activate && python manage.py migrate'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Exécuter les tests unitaires
                    sh '. ${VENV_DIR}/bin/activate && python manage.py test'
                }
            }
        }

        stage('Build and Run Django Container') {
            steps {
                script {
                    // Construire et démarrer l'image Docker pour Django
                    sh """
                    docker build -t allservice-appointment .
                    docker run --name django-dev --link ${POSTGRES_CONTAINER_NAME}:db -p 8000:8000 -d allservice-appointment
                    """
                    // Attendre que Django soit prêt
                    sh 'sleep 10'
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                script {
                    // Déployer via Docker (ou toute autre méthode)
                    // Assure-toi que tes conteneurs sont liés et correctement configurés
                    sh 'docker-compose down && docker-compose up -d'
                }
            }
        }
    }

    post {
        always {
            // Actions à exécuter après chaque exécution
            echo 'Pipeline terminé.'
        }
        success {
            // Actions en cas de succès
            echo 'Déploiement réussi !'
        }
        failure {
            // Actions en cas d'échec
            echo 'Le déploiement a échoué.'
            // Stopper les conteneurs en cas d'échec
            sh 'docker stop django-dev pgsql-dev'
            sh 'docker rm django-dev pgsql-dev'
        }
    }
}

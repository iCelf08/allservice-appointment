pipeline {
    agent any

    environment {
        PROJECT_DIR = "${WORKSPACE}"
        VENV_DIR = "${PROJECT_DIR}/venv"
        DJANGO_SETTINGS_MODULE = 'PriseRendez.settings.production'
        POSTGRES_CONTAINER_NAME = 'pgsql-dev'
        POSTGRES_USER = 'postgres'
        POSTGRES_PASSWORD = '123456'
        POSTGRES_DB = 'allservice_db'
        POSTGRES_PORT = '5432'
        NETWORK_NAME = 'mynetwork'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/iCelf08/allservice-appointment.git'
            }
        }

        stage('Setup Network') {
            steps {
                script {
                    sh 'docker network ls | grep -wq mynetwork || docker network create mynetwork'
                }
            }
        }

        stage('Start PostgreSQL Container') {
            steps {
                script {
                    sh """
                    docker ps -q -f name=${POSTGRES_CONTAINER_NAME} | xargs -r docker stop | xargs -r docker rm
                    docker run --name ${POSTGRES_CONTAINER_NAME} --network ${NETWORK_NAME} \
                      -e POSTGRES_USER=${POSTGRES_USER} \
                      -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
                      -e POSTGRES_DB=${POSTGRES_DB} \
                      -p ${POSTGRES_PORT}:5432 -d postgres
                    """
                }
            }
        }

        stage('Build and Run Django Container') {
            steps {
                script {
                    sh """
                    docker ps -q -f name=django-dev | xargs -r docker stop | xargs -r docker rm
                    docker build -t allservice-appointment .
                    docker run --name django-dev --network ${NETWORK_NAME} \
                      -p 8001:8000 -d allservice-appointment
                    """
                    // Attendre que Django démarre
                    sh 'sleep 10'
                    sh 'docker logs django-dev | tail -n 10'
                }
            }
        }

        stage('Run Migrations and Create Superuser') {
            steps {
                script {
                    sh """
                    docker exec django-dev python manage.py migrate
                    docker exec -it django-dev python manage.py createsuperuser --noinput || true
                    """
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                script {
                    // Si docker-compose est utilisé
                    sh 'docker-compose down || true'
                    sh 'docker-compose up -d'
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminé.'
        }
        success {
            echo 'Déploiement réussi !'
        }
        failure {
            echo 'Le déploiement a échoué.'
            sh 'docker stop django-dev || true'
            sh 'docker stop pgsql-dev || true'
            sh 'docker rm django-dev || true'
            sh 'docker rm pgsql-dev || true'
        }
    }
}

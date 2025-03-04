pipeline {
    agent any

    environment {
        PROJECT_DIR = "${WORKSPACE}"
        VENV_DIR = "${PROJECT_DIR}/venv"
        DJANGO_SETTINGS_MODULE = 'PriseRendez.settings.production'
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
                git branch: 'master', url: 'https://github.com/iCelf08/allservice-appointment.git'
            }
        }

        stage('Stop and Remove Existing Containers') {
            steps {
                script {
                    // Clean up existing containers to avoid conflicts
                    sh 'docker ps -q -f name=django-dev | xargs -r docker stop | xargs -r docker rm'
                }
            }
        }



        stage('Build and Run Django Container') {
            steps {
                script {
                    sh """
                    docker build -t allservice-appointment .
                    docker run --name django-dev --link ${POSTGRES_CONTAINER_NAME}:db -p 8000:8000 -d allservice-appointment
                    """
                    // Wait for Django container to be ready
                    sh 'sleep 10'
                    // Optionally check if Django is ready
                    sh 'docker logs django-dev | tail -n 10'
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                script {
                    // Optionally use docker-compose to manage multiple containers
                    sh 'docker-compose down && docker-compose up -d'
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
            sh 'docker stop django-dev pgsql-dev'
            sh 'docker rm django-dev pgsql-dev'
        }
    }
}

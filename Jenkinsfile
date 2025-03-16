pipeline {
    agent any
    
    stages {
        stage('Cleanup') {
            steps {
                sh '''
                 if docker ps -a | grep -q django-appointement; then
                docker stop django-appointement || true
                docker rm django-appointement || true
                else
                        echo "Container django-appointement does not exist. Skipping cleanup."
                fi
                '''
            }
        }
        
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/iCelf08/allservice-appointment.git'
            }
        }
        
        stage('Check Network and Database') {
            steps {
                sh '''
                # Vérifier si le réseau existe, sinon le créer
                docker network inspect mynetwork >/dev/null 2>&1 || docker network create mynetwork
                
                # Vérifier si le conteneur PostgreSQL existe, sinon afficher un message
                docker inspect pgsql-dev >/dev/null 2>&1 || echo "ATTENTION: Le conteneur PostgreSQL 'pgsql-dev' n'existe pas. Veuillez le créer d'abord."
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'docker-compose -f docker-compose.yaml up -d --build web'
            }
        }
    }
    
    post {
        failure {
            sh 'docker-compose -f docker-compose.yaml down || true'
        }
    }
}

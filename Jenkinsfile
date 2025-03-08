pipeline {
    agent any
    environment {
        NETWORK_NAME = 'mynetwork'
    }
    stages {
        stage('Cleanup') {
            steps {
                sh '''
                docker stop django-dev pgsql-dev || true
                docker rm django-dev pgsql-dev || true
                docker network rm ${NETWORK_NAME} || true
                '''
            }
        }
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/iCelf08/allservice-appointment.git'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker network create ${NETWORK_NAME} || true'
                sh 'docker-compose down --remove-orphans || true'
                sh 'docker-compose up -d --build'
            }
        }
    }
    post {
        failure {
            sh 'docker-compose down || true'
        }
    }
}

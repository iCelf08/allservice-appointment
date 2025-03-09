pipeline {
    agent any
    stages {
        stage('Cleanup') {
            steps {
                sh '''
                docker stop django-dev || true
                docker rm django-dev || true
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
                sh 'docker network inspect mynetwork >/dev/null 2>&1 || docker network create mynetwork'
                sh 'docker-compose -f docker-compose.yml down --remove-orphans || true'
                sh 'docker-compose -f docker-compose.yml up -d --build'
            }
        }
    }
    post {
        failure {
            sh 'docker-compose -f docker-compose.django.yml down || true'
        }
    }
}

pipeline {
    agent any

    environment {
        PROJECT_DIR = "${WORKSPACE}"
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
                sh 'docker network create ${NETWORK_NAME} || true'
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh 'docker-compose down || true'
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

pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {}
        }
        stage('Build') {
            steps {
                sh 'echo Test build' 
            }
        }
        stage('Testing') {
            parallel {
                stage('SECURITY CHECKS') {
                    steps {
                        echo "CHECK SECURITY PACKAGES" 
                        sh 'echo security done'
                    }
                }
                stage('API TESTING') {
                    steps {
                        echo 'CHECKING APIs FUNCTIONALITY'
                        sh 'echo api works'
                    }
                }
            }
        }
    }
}
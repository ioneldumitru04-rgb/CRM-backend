pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'echo Test build' 
            }
        }
        stage('Testing') {
            parallel {
                steps {
                    echo "INTERPRETATOR TESTING"
                    sh 'echo interpreted'
                    sh 'echo exit succesfully'
                }
                steps {
                    echo "API testing"
                    sh 'echo api interpreted'
                    sh 'echo exit succesfully'
                }
            }
        }
    }
}
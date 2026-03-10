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
                    label: "TESTARE 1",
                    sh "TESTAREA DE LA 1"
                    sh "TESTAREA DE LA 1 x1"
                    sh "TESTAREA DE LA 1 x2"
                }
                steps {
                    label: "TESTARE 2",
                    sh "TESTAREA DE LA 2"
                    sh "TESTAREA DE LA 2 x1"
                    sh "TESTAREA DE LA 2 x2"
                }
            }
        }
    }
}
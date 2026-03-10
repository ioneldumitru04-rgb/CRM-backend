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
                    sh label: "TESTARE 1",
                    script "echo TESTAREA DE LA 1",
                    script "echo TESTAREA DE LA 1 x1",
                    script "echo TESTAREA DE LA 1 x2"
                }
                steps {
                    sh label: "TESTARE 2",
                    script "echo TESTAREA DE LA 2",
                    script "echo TESTAREA DE LA 2 x1",
                    script "echo TESTAREA DE LA 2 x2"
                }
            }
        }
    }
}
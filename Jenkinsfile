pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                echo "Get latest revision"
            }
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
                        sh "git clone ${REPO}"
                        sh '''
                        [[ -d scm/ ]] && rm -rfd scm
                        git clone https://github.com/ioneldumitru04-rgb/scm
                        python3 scm/tests/run_tests.py --security_tests
                        '''
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
        stage('Delivery') {
            steps {
                sh 'echo Delivery' 
            }
        }
    }
}
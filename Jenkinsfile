pipeline {
    agent any
    options {
        ansiColor('xterm')
    }
    stages {
        stage('Checkout product') {
            steps {
                echo "Get latest revision"
            }
        }
        stage('Clone scm repo') {
            steps {
                sh 'echo Cloning'
                sh "git clone ${REPO}"
                sh '''
                [[ -d scm/ ]] && rm -rfd scm
                git clone https://github.com/ioneldumitru04-rgb/scm
                ''' 
            }
        }
        stage('Testing') {
            parallel {
                stage('Unit Tests Security') {
                    steps {
                        echo "CHECK SECURITY PACKAGES"
                        sh '''
                        set -eo pipefail
                        python3 scm/tests/run_tests.py --security_tests
                        '''
                    }
                }
                stage('Unit Tests API') {
                    steps {
                        echo 'CHECKING APIs FUNCTIONALITY'
                        sh '''
                        set -eo pipefail
                        python3 scm/tests/run_tests.py --functionality_tests
                        '''
                    }
                }
            }
        }
        stage('Automated Security Checks') {
            steps {
                echo "BANDIT STARTED"
                sh '''
                set -eo pipefail
                python3 scm/tests/run_tests.py --automated_security_tests
                '''
            }
        }
        stage('Delivery') {
            steps {
                sh 'echo Delivery' 
            }
        }
    }
}
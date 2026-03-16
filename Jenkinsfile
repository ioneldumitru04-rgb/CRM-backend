pipeline {
    agent any
    options {
        ansiColor('xterm')
    }
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
                stage('Unit Tests Security') {
                    steps {
                        echo "CHECK SECURITY PACKAGES"
                        sh "git clone ${REPO}"
                        sh '''
                        set -eo pipefail
                        [[ -d scm/ ]] && rm -rfd scm
                        git clone https://github.com/ioneldumitru04-rgb/scm
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
pipeline {
    agent none
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'web_app:latest'
                }
            }
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'web_app/latest'
                }
            }
            steps {
                sh 'python3 -m unittest'
            }
            post {
                always {
                    junit 'test-reports/*.xml'
                }
            }
        }
    }
}

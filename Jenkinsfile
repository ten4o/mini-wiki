pipeline {
    agent { dockerfile true }
    stages {
        stage('Build') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Test') {
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

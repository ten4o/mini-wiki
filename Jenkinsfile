pipeline {
    agent { dockerfile true }
    stages {
        stage('Build') {
            steps {
                sh 'echo TODO'
            }
        }
        stage('Test') {
            steps {
                sh 'py.test --junitxml test-reports/results.xml'
            }
            post {
                always {
                    junit 'test-reports/*.xml'
                }
            }
        }
    }
}

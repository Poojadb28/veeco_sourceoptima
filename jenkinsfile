pipeline {
    agent any

    environment {
        HEADLESS = "true"
        BASE_URL = "https://testing.sourceoptima.com/"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Poojadb28/veeco_sourceoptima'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'pytest'
            }
        }

        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: 'reports/report.html', allowEmptyArchive: true
            }
        }
    }
}
pipeline {
    agent any

    environment {
        HEADLESS = 'false'
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat """
                "C:\\Users\\Dell\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version
                "C:\\Users\\Dell\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install --upgrade pip
                "C:\\Users\\Dell\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install -r requirements.txt
                """
            }
        }

        stage('Prepare Folders') {
            steps {
                bat "if not exist reports mkdir reports"
            }
        }

        stage('Run Tests') {
            steps {
                // bat "\"C:\\Users\\Dell\\AppData\\Local\\Programs\\Python\\Python313\\python.exe\" -m pytest tests/test_e2e_flow.py -v --html=reports/report.html"
                bat "\"C:\\Users\\Dell\\AppData\\Local\\Programs\\Python\\Python313\\python.exe\" -m pytest -v --html=reports/report.html"
            }
        }
    }

    post {
        always {
            publishHTML([
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Test Report',
                keepAll: true,
                alwaysLinkToLastBuild: true,
                allowMissing: true
            ])
        }
    }
}


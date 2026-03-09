pipeline {
    agent {
        node {
            customWorkspace '/workspace'
        }
    }

    options {
        timestamps()
    }

    stages {
        stage('Cleanup') {
            steps {
                sh 'rm -rf allure-results'
                sh 'mkdir -p allure-results'
                sh 'docker compose --profile ci rm -sf autotests selenoid selenoid-ui || true'
            }
        }

        stage('Run UI tests in Docker') {
            steps {
                script {
                    def exitCode = sh(
                        script: 'docker compose --profile ci up --build --abort-on-container-exit --exit-code-from autotests autotests selenoid selenoid-ui',
                        returnStatus: true
                    )

                    sh 'docker cp sdet_autotests:/app/allure-results/. allure-results || true'
                    sh 'docker compose --profile ci rm -sf autotests selenoid selenoid-ui || true'

                    if (exitCode != 0) {
                        error("Autotests failed with exit code ${exitCode}")
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'docker compose --profile ci rm -sf autotests selenoid selenoid-ui || true'
            archiveArtifacts artifacts: 'allure-results/**/*', allowEmptyArchive: true
        }
    }
}

pipeline {
    agent any

    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch')
        choice(name: 'RUN_ENV', choices: ['cicd', 'local'], description: 'Environment config')
        choice(name: 'HEADLESS', choices: ['true', 'false'], description: 'Headless mode')
        string(name: 'TESTS_PATH', defaultValue: 'web_ui/ui_tests', description: 'Path to tests')
        string(name: 'HOST', defaultValue: '', description: 'Override PROJECT_HOST if needed')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: "${params.BRANCH}",
                    credentialsId: 'github-token',
                    url: 'https://github.com/Famik85/test_jenkins.git'
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    rm -rf venv reports allure-results
                    python3 -m venv venv
                    . venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Install Playwright Browsers') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m playwright install
                '''
            }
        }

        stage('Cross-browser tests') {
            parallel {
                stage('Chromium') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                            sh '''
                                . venv/bin/activate
                                ./scripts/run_tests.sh chromium ${RUN_ENV} ${HEADLESS} ${TESTS_PATH} "${HOST}"
                            '''
                        }
                    }
                }

                stage('Firefox') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                            sh '''
                                . venv/bin/activate
                                ./scripts/run_tests.sh firefox ${RUN_ENV} ${HEADLESS} ${TESTS_PATH} "${HOST}"
                            '''
                        }
                    }
                }

                stage('WebKit') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                            sh '''
                                . venv/bin/activate
                                ./scripts/run_tests.sh webkit ${RUN_ENV} ${HEADLESS} ${TESTS_PATH} "${HOST}"
                            '''
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/*.xml'

            allure(
                commandline: 'Allure',
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            )

            archiveArtifacts artifacts: 'reports/**, allure-results/**, test-results/**', allowEmptyArchive: true
        }

        unsuccessful {
            echo 'Some tests failed. Check JUnit and Allure reports.'
        }
    }
}

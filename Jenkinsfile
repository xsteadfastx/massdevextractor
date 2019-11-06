pipeline {
        agent {
                docker {
                        image 'xsteadfastx/tox-python:minimal'
                }
        }
        environment {
                TOX_WORK_DIR = '/tmp'
        }
        stages {
                stage('Test') {
                        steps {
                                sh 'sudo apk add --no-cache gcc musl-dev'
                                sh 'tox -v -e py37'
                                sh 'tox -v -e flake8'
                                sh 'tox -v -e pylint'
                                sh 'tox -v -e mypy'
                                sh 'tox -v -e black-only-check'
                        }
                }
                stage('Coverage') {
                        steps {
                                sh 'tox -e coverage'
                                publishHTML(
                                        [
                                                allowMissing: false,
                                                alwaysLinkToLastBuild: false,
                                                keepAll: false,
                                                reportDir: 'htmlcov',
                                                reportFiles: 'index.html',
                                                reportName: 'HTML Report',
                                                reportTitles: ''
                                        ]
                                )
                        }
                }
        }
}

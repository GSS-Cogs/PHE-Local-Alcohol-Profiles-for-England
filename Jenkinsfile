pipeline {
    agent {
        label 'master'
    }
    triggers {
        upstream(upstreamProjects: '../Reference/ref_alcohol',
                 threshold: hudson.model.Result.SUCCESS)
    }
    stages {
        stage('Clean') {
            steps {
                sh 'rm -rf out'
            }
        }
        stage('Transform') {
            agent {
                docker {
                    image 'cloudfluff/databaker'
                    reuseNode true
                }
            }
            steps {
                sh "jupyter-nbconvert --output-dir=out --ExecutePreprocessor.timeout=None --execute 'LocalAlcoholProfilesforEngland county.ipynb'"
                sh "jupyter-nbconvert --output-dir=out --ExecutePreprocessor.timeout=None --execute 'LocalAlcoholProfilesforEngland district.ipynb'"
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'cloudfluff/csvlint'
                    reuseNode true
                }
            }
            steps {
                script {
                    ansiColor('xterm') {
                        error "Needs review"
                        sh "csvlint -s schema.json"
                    }
                }
            }
        }
        stage('Upload draftset') {
            steps {
                script {
                    jobDraft.replace()
                    uploadTidy(['out/alcoholprofilescounty.csv', 'out/alcoholprofilesdistrict.csv'],
                               'https://github.com/ONS-OpenData/ref_alcohol/raw/master/columns.csv')
                }
            }
        }
        stage('Publish') {
            steps {
                script {
                    jobDraft.publish()
                }
            }
        }
    }
    post {
        always {
            script {
                archiveArtifacts 'out/*'
                updateCard "5b4f3bcc9d6d58290a30762f"
            }
        }
        success {
            build job: '../GDP-tests', wait: false
        }
    }
}

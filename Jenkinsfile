pipeline {
    agent any

    environment {
        REGISTRY = 'alexsoftav72'
        APP_NAME = 'superset'
        IMAGE_TAG = "${BUILD_NUMBER}"
        // ID credentials для kubeconfig (который вы успешно настроили)
        KUBECONFIG_CRED_ID = 'minikube-full-kubeconfig'
        // URL репозитория с манифестами
        GITOPS_REPO = 'https://github.com/alexsoftav72/superset-gitops.git'
        GITOPS_CREDENTIALS = 'github-token'
    }

    stages {
        stage('Build & Push Image') {
            steps {
                script {
                    docker.withRegistry('', 'docker-hub-credentials') {
                        def customImage = docker.build("${REGISTRY}/${APP_NAME}:${IMAGE_TAG}")
                        customImage.push()
                        customImage.push('latest')
                    }
                }
            }
        }

        // Обновляем тег образа в GitOps-репозитории
      stage('Update GitOps Repo') {
            steps {
                script {
                    // Используем withCredentials для доступа к GitHub
                    withCredentials([usernamePassword(
                        credentialsId: GITOPS_CREDENTIALS,
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_TOKEN'
                    )]) {
                        sh '''
                            # Используем токен для клонирования
                            git clone https://${GIT_USER}:${GIT_TOKEN}@github.com/alexsoftav72/superset-gitops.git gitops
                            cd gitops
                            
                            # Обновляем тег образа
                            sed -i "s|image: alexsoftav72/superset:.*|image: alexsoftav72/superset:${IMAGE_TAG}|" deployment.yaml
                            
                            # Настраиваем git
                            git config user.email "jenkins@jenkins.local"
                            git config user.name "Jenkins"
                            
                            # Коммитим и пушим
                            git add deployment.yaml
                            git commit -m "Update image to version ${IMAGE_TAG}" || echo "No changes to commit"
                            git push https://${GIT_USER}:${GIT_TOKEN}@github.com/alexsoftav72/superset-gitops.git main
                        '''
                    }
                }
            }
        }

        // Деплой в Minikube
        stage('Deploy to Minikube') {
            steps {
                withKubeConfig([credentialsId: 'minikube-full-kubeconfig']) {
                    sh '''
                        kubectl apply -f deployment.yaml -n superset
                        kubectl apply -f service.yaml -n superset
                        kubectl apply -f ingress.yaml -n superset
                        kubectl rollout status deployment/superset -n superset
                    '''
                }
            }
        }
    }

    post {
        always {
            deleteDir()
        }
    }
}

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
            withCredentials([sshUserPrivateKey(credentialsId: 'ssh-gitops-key', 
                                               keyFileVariable: 'SSH_KEY')]) {
                sh '''
        ssh-keyscan github.com >> $HOME/.ssh/known_hosts
        
        # 4. Клонируем репозиторий
        git clone git@github.com:alexsoft72/superset-gitops.git gitops
        cd gitops
        
        # 5. Обновляем тег образа
        sed -i "s|image: alexsoftav72/superset:.*|image: alexsoftav72/superset:${IMAGE_TAG}|" deployment.yaml
        
        # 6. Пуш в GitOps
        git config user.email "jenkins@jenkins.local"
        git config user.name "Jenkins"
        git add deployment.yaml
        git commit -m "Update image to version ${IMAGE_TAG}"
        git push origin main
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

pipeline {
    agent any

    environment {
        REGISTRY = 'alexsoftav72'
        APP_NAME = 'superset'
        IMAGE_TAG = "${BUILD_NUMBER}"
        KUBECONFIG_CRED_ID = 'minikube-full-kubeconfig'
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

        stage('Update GitOps Repo') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'ssh-gitops-key', 
                                                       keyFileVariable: 'SSH_KEY')]) {
                        sh '''
                            ssh-keyscan github.com >> $HOME/.ssh/known_hosts
                            
                            git clone git@github.com:Alexsoft72/superset-gitops.git gitops
                            cd gitops
                            
                            sed -i "s|image: alexsoftav72/superset:.*|image: alexsoftav72/superset:${IMAGE_TAG}|" deployment.yaml
                            
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

        stage('Init Superset') {
    steps {
        withKubeConfig([credentialsId: 'minikube-full-kubeconfig']) {
            sh '''
                # 1. Проверяем, существует ли секрет
                kubectl -n superset get secret superset-secrets || kubectl -n superset create secret generic superset-secrets --from-literal=secret-key='121212121223453625735'

                # 2. Проверяем, существует ли Job
                kubectl -n superset get job superset-init || kubectl -n superset create job superset-init --image=alexsoftav72/superset:latest -- sh -c "superset db upgrade && superset fab create-admin --username admin --password admin --firstname Admin --lastname Admin --email admin@superset.com"
                                
                # Инициализация базы данных
                kubectl -n superset create job superset-init --image=alexsoftav72/superset:latest -- sh -c "superset db upgrade && superset fab create-admin --username admin --password admin --firstname Admin --lastname Admin --email admin@superset.com"
                
                # Проверяем, что под готов
                kubectl -n superset wait --for=condition=ready pod -l app=superset
            '''
        }
    }
}
        
        stage('Deploy to Minikube') {
            steps {
                withKubeConfig([credentialsId: 'minikube-full-kubeconfig']) {
                    sh '''
                        kubectl create namespace superset
                        kubectl apply -f gitops/deployment.yaml -n superset
                        kubectl apply -f gitops/service.yaml -n superset
                        kubectl apply -f gitops/ingress.yaml -n superset
                        kubectl apply -f gitops/configmap.yaml -n superset
                        kubectl apply -f gitops/persistentvolumeclaim.yaml -n superset
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

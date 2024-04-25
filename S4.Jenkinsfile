pipeline {
    agent any
    environment {
        INSTANCE_NAME = "aparking-backend-s4"
        PROJECT = "aparking-g11-s3"
        GIT_REPO = "https://github.com/Aparking/AparKing_Backend.git"
        GIT_BRANCH = "deploy/s4"
    }
    stages {
        stage('Clone Repository') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: "*/${GIT_BRANCH}"]], userRemoteConfigs: [[url: "${GIT_REPO}"]]])
            }
        }
        stage('Prepare Environment') {
            steps {
                script {
                    sh """
                    echo "EMAIL_HOST_USER=aparking.g11@gmail.com" > .env
                    echo "EMAIL_HOST_PASSWORD=${env.EMAIL_HOST_PASSWORD}" >> .env
                    """
                }
            }
        }
        stage('Deploy to App Engine') {
            steps {
                script {
                    cp ./docker/backend.Dockerfile ./Dockerfile
                    // Configura el proyecto de GCP
                    sh "gcloud config set project ${PROJECT}"
                    // Despliega la aplicación
                    sh "gcloud app deploy app.yaml --quiet"
                    rm ./Dockerfile
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            mail to: 'juancarlosralop@gmail.com, sergiosantiago0403@gmail.com, maria-vico@hotmail.es',
                subject: "Despliegue Completado: ${INSTANCE_NAME}",
                body: "El despliegue de ${INSTANCE_NAME} en App Engine ha sido completado exitosamente. Puedes verificar la aplicación en la consola de Google Cloud."
        }
        failure {
            mail to: 'juancarlosralop@gmail.com, sergiosantiago0403@gmail.com, maria-vico@hotmail.es',
                subject: "Despliegue Fallido: ${INSTANCE_NAME}",
                body: "El despliegue de ${INSTANCE_NAME} en App Engine ha fallado."
        }
    }
}
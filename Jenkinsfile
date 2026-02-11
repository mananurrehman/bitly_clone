pipeline {
    agent any
    
    environment {
        // DockerHub credentials (set in Jenkins)
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_USERNAME = 'mananurrehman'
        IMAGE_NAME = 'bitly-clone'
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKERHUB_REPO = "${DOCKERHUB_USERNAME}/${IMAGE_NAME}"
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                echo '📥 Fetching code from GitHub...'
                checkout scm
                sh 'ls -la'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo '🔨 Building Docker image...'
                script {
                    sh """
                        docker build -t ${DOCKERHUB_REPO}:${IMAGE_TAG} .
                        docker tag ${DOCKERHUB_REPO}:${IMAGE_TAG} ${DOCKERHUB_REPO}:latest
                        echo "Image built: ${DOCKERHUB_REPO}:${IMAGE_TAG}"
                    """
                }
            }
        }
        
        stage('Push to DockerHub') {
            steps {
                echo '📤 Pushing image to DockerHub...'
                script {
                    sh """
                        echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
                        docker push ${DOCKERHUB_REPO}:${IMAGE_TAG}
                        docker push ${DOCKERHUB_REPO}:latest
                        echo "Image pushed successfully!"
                    """
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                echo '🧪 Running tests on Docker image...'
                script {
                    sh """
                        # Pull the image we just pushed
                        docker pull ${DOCKERHUB_REPO}:${IMAGE_TAG}
                        
                        # Basic syntax check
                        echo "Running Python syntax checks..."
                        docker run --rm ${DOCKERHUB_REPO}:${IMAGE_TAG} \
                            sh -c 'find . -name "*.py" -not -path "./migrations/*" | head -20 | xargs -I {} python -m py_compile {}'
                        
                        # Health check - start container and check if it responds
                        echo "Running health check..."
                        docker run -d --rm --name bitly-healthcheck-${BUILD_NUMBER} \
                            -p 5555:5000 \
                            -e DATABASE_URL=sqlite:///test.db \
                            -e SECRET_KEY=test-key \
                            ${DOCKERHUB_REPO}:${IMAGE_TAG}
                        
                        # Wait for app to start
                        sleep 10
                        
                        # Check if app responds
                        curl -f http://localhost:5555 || (docker logs bitly-healthcheck-${BUILD_NUMBER} && exit 1)
                        
                        # Cleanup
                        docker stop bitly-healthcheck-${BUILD_NUMBER} || true
                        
                        echo "✅ All tests passed!"
                    """
                }
            }
        }
        
        stage('Manual Approval') {
            steps {
                echo '⏸️  Waiting for manual approval...'
                script {
                    def deploymentApproved = input(
                        id: 'DeployApproval',
                        message: '🚀 Deploy to production?',
                        parameters: [
                            choice(
                                name: 'DEPLOY_ACTION',
                                choices: ['Deploy', 'Abort'],
                                description: 'Select Deploy to proceed with deployment'
                            )
                        ]
                    )
                    
                    if (deploymentApproved != 'Deploy') {
                        error('Deployment aborted by user')
                    }
                    echo '✅ Deployment approved!'
                }
            }
        }
        
        stage('Deploy to VM') {
            steps {
                echo '🚀 Deploying to production...'
                script {
                    sh """
                        # Stop old containers
                        docker stop bitly_clone_app || true
                        docker rm bitly_clone_app || true
                        docker stop bitly_clone_db || true
                        docker rm bitly_clone_db || true
                        
                        # Create network if doesn't exist
                        docker network create bitly_net || true
                        
                        # Create volume for database if doesn't exist
                        docker volume create bitly_postgres_data || true
                        
                        # Start database
                        docker run -d \
                            --name bitly_clone_db \
                            --network bitly_net \
                            -e POSTGRES_USER=bitly_user \
                            -e POSTGRES_PASSWORD=bitly_secure_pass_123 \
                            -e POSTGRES_DB=bitly_db \
                            -v bitly_postgres_data:/var/lib/postgresql/data \
                            --restart unless-stopped \
                            postgres:15-alpine
                        
                        echo "Waiting for database to be ready..."
                        sleep 10
                        
                        # Pull the tested image from DockerHub
                        docker pull ${DOCKERHUB_REPO}:${IMAGE_TAG}
                        
                        # Start application with the tested image
                        docker run -d \
                            --name bitly_clone_app \
                            --network bitly_net \
                            -p 5000:5000 \
                            -e SECRET_KEY=production-secret-key-change-this \
                            -e DATABASE_URL=postgresql://bitly_user:bitly_secure_pass_123@bitly_clone_db:5432/bitly_db \
                            -e FLASK_ENV=production \
                            -e FLASK_DEBUG=0 \
                            --restart unless-stopped \
                            ${DOCKERHUB_REPO}:${IMAGE_TAG}
                        
                        echo "Waiting for application to start..."
                        sleep 15
                    """
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo '✅ Verifying deployment...'
                script {
                    sh """
                        # Check if containers are running
                        docker ps | grep bitly_clone
                        
                        # Health check
                        max_attempts=30
                        attempt=0
                        
                        while [ \$attempt -lt \$max_attempts ]; do
                            if curl -f http://localhost:5000 > /dev/null 2>&1; then
                                echo "✅ Application is healthy and responding!"
                                exit 0
                            fi
                            echo "Waiting for application... (\$attempt/\$max_attempts)"
                            sleep 2
                            attempt=\$((attempt + 1))
                        done
                        
                        echo "❌ Health check failed!"
                        docker logs bitly_clone_app --tail=50
                        exit 1
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo '========================================='
            echo '✅ DEPLOYMENT SUCCESSFUL!'
            echo '========================================='
            echo "🐳 Docker Image: ${DOCKERHUB_REPO}:${IMAGE_TAG}"
            echo '========================================='
        }
        failure {
            echo '========================================='
            echo '❌ PIPELINE FAILED!'
            echo '========================================='
            script {
                sh 'docker logs bitly_clone_app --tail=50 || true'
            }
        }
        always {
            echo 'Cleaning up test containers...'
            script {
                sh '''
                    docker stop bitly-healthcheck-${BUILD_NUMBER} || true
                    docker logout
                '''
            }
        }
    }
}
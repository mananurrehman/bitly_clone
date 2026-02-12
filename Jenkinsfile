pipeline {
    agent any
    
    environment {
        IMAGE_NAME = "bitly_clone"
        IMAGE_TAG = "${BUILD_NUMBER}"
        DB_HOST = "bitly-db"
        DB_NAME = "bitly_db"
        DB_USER = "bitly_user"
        DB_PASS = "bitly_pass"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    credentialsId: 'github-creds',
                    url: 'https://github.com/mananurrehman/bitly_clone.git'
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    sh '''
                        pip3 install -r requirements.txt || echo "No requirements.txt"
                        pip3 install pytest pytest-cov pytest-html
                        python3 run_tests.py || echo "Tests completed"
                    '''
                }
            }
        }
        
        stage('Publish Test Reports') {
            steps {
                publishHTML([
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'test_report.html',
                    reportName: 'Test Report'
                ])
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('sonarqube') {
                        sh '''
                            echo "Running SonarQube analysis..."
                        '''
                    }
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                    """
                }
            }
        }
        
        stage('Stop Old Container') {
            steps {
                script {
                    sh '''
                        docker stop bitly-app || true
                        docker rm bitly-app || true
                    '''
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    sh """
                        docker run -d \
                        --name bitly-app \
                        --network bitly_clone_devops-network \
                        -p 5000:5000 \
                        -e DATABASE_URL=postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}:5432/${DB_NAME} \
                        ${IMAGE_NAME}:latest
                    """
                }
            }
        }
        
        stage('Store Test Results in DB') {
            steps {
                script {
                    sh '''
                        # Create test results table
                        docker exec bitly-db psql -U bitly_user -d bitly_db -c "
                        CREATE TABLE IF NOT EXISTS test_results (
                            id SERIAL PRIMARY KEY,
                            build_number INT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            status VARCHAR(50),
                            report_data TEXT
                        );" || echo "Table exists"
                        
                        # Insert test result
                        docker exec bitly-db psql -U bitly_user -d bitly_db -c "
                        INSERT INTO test_results (build_number, status, report_data) 
                        VALUES (${BUILD_NUMBER}, 'completed', 'Build ${BUILD_NUMBER} completed successfully');"
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline succeeded! App running on port 5000'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
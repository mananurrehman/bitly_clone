pipeline {
    agent any

    environment {
        SONAR_HOME     = tool "Sonar"
        ORACLE_VM_IP   = '140.245.25.178'
        ORACLE_VM_USER = 'ubuntu'
        APP_DIR        = '/home/ubuntu/bitly-clone-testuser'
    }

    stages {

        stage("Clone Code from GitHub") {
            steps {
                git url: "https://github.com/mananurrehman/bitly_clone.git", branch: "main"
            }
        }

        stage("SonarQube Quality Analysis") {
            steps {
                withSonarQubeEnv("Sonar") {
                    sh "$SONAR_HOME/bin/sonar-scanner -Dsonar.projectName=bitly-clone-testuser -Dsonar.projectKey=bitly-clone-testuser"
                }
            }
        }

        stage("OWASP Dependency Check") {
            steps {
                dependencyCheck additionalArguments: '--scan ./', odcInstallation: 'dc'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }

        stage("Trivy File System Scan") {
            steps {
                sh "trivy fs --format table -o trivy-fs-report.html ."
            }
        }

        stage("Deploy to Oracle Cloud VM") {
            steps {
                sshagent(['oracle-vm-ssh-testuser']) {

                    // Step 1: Clone or Pull code
                    sh """
                        ssh -o StrictHostKeyChecking=no ${ORACLE_VM_USER}@${ORACLE_VM_IP} 'if [ -d "${APP_DIR}" ]; then cd ${APP_DIR} && git pull origin main; else git clone -b main https://github.com/mananurrehman/bitly_clone.git ${APP_DIR}; fi'
                    """

                    // Step 2: Create .env file
                    sh """
                        ssh -o StrictHostKeyChecking=no ${ORACLE_VM_USER}@${ORACLE_VM_IP} 'cat > ${APP_DIR}/.env << EOF
SECRET_KEY=your-super-secret-key-testuser-2024
POSTGRES_USER=bitly_testuser
POSTGRES_PASSWORD=bitly_password_testuser
POSTGRES_DB=bitly_db_testuser
DATABASE_URL=postgresql://bitly_testuser:bitly_password_testuser@bitly-db-testuser:5432/bitly_db_testuser
EOF'
                    """

                    // Step 3: Stop old containers
                    sh """
                        ssh -o StrictHostKeyChecking=no ${ORACLE_VM_USER}@${ORACLE_VM_IP} 'cd ${APP_DIR} && docker compose down || true'
                    """

                    // Step 4: Build and Start containers
                    sh """
                        ssh -o StrictHostKeyChecking=no ${ORACLE_VM_USER}@${ORACLE_VM_IP} 'cd ${APP_DIR} && docker compose up -d --build'
                    """
                }
            }
        }

        stage("Run Tests on Oracle VM") {
            steps {
                sshagent(['oracle-vm-ssh-testuser']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${ORACLE_VM_USER}@${ORACLE_VM_IP} '
                            sleep 15
                            docker exec bitly-app-testuser python run_tests.py || true
                        '
                    """

                    // Copy test reports from Oracle VM to Jenkins
                    sh """
                        scp -o StrictHostKeyChecking=no ${ORACLE_VM_USER}@${ORACLE_VM_IP}:${APP_DIR}/test_report.html . 2>/dev/null || echo "No test report found"
                        scp -o StrictHostKeyChecking=no ${ORACLE_VM_USER}@${ORACLE_VM_IP}:${APP_DIR}/test_summary.json . 2>/dev/null || echo "No test summary found"
                    """
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'test_report.html', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'test_summary.json', allowEmptyArchive: true
                }
            }
        }

        stage("Verify Deployment") {
            steps {
                sshagent(['oracle-vm-ssh-testuser']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${ORACLE_VM_USER}@${ORACLE_VM_IP} '
                            echo "=== Running Containers ==="
                            docker ps --format "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}" | grep testuser

                            echo ""
                            echo "=== Health Check ==="
                            curl -s -o /dev/null -w "App Status: %{http_code}\\n" http://localhost:5001 || echo "App: Not Ready"
                        '
                    """
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/dependency-check-report.*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'trivy-fs-report.html', allowEmptyArchive: true
        }
        success {
            echo "✅ Bitly Clone deployed successfully on http://140.245.25.178:5001 - testuser"
        }
        failure {
            echo "❌ Pipeline failed - testuser"
        }
    }
}

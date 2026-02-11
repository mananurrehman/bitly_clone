#!/bin/bash

echo "========================================="
echo "Jenkins CI/CD Setup Script"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed!${NC}"
    echo "Please install Docker first"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker &> /dev/null || ! docker compose version &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed!${NC}"
    exit 1
fi

# Check if docker-compose.jenkins.yml exists
if [ ! -f "docker-compose.jenkins.yml" ]; then
    echo -e "${RED}docker-compose.jenkins.yml not found!${NC}"
    exit 1
fi

# Start Jenkins
echo -e "${GREEN}Starting Jenkins container...${NC}"
docker compose -f docker-compose.jenkins.yml up -d

# Wait for Jenkins to start
echo ""
echo -e "${YELLOW}Waiting for Jenkins to start...${NC}"
sleep 20

# Get Jenkins password
echo ""
echo "========================================="
echo -e "${GREEN}Jenkins Started Successfully!${NC}"
echo "========================================="
echo ""
echo "🔑 Initial Admin Password:"
echo ""
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null || echo "Still initializing... wait 30 seconds and run: docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword"
echo ""
echo "========================================="
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Open Jenkins in browser"
echo "2. Enter the password above"
echo "3. Install suggested plugins"
echo "4. Create admin user"
echo "5. Install Docker CLI (see README_JENKINS.md)"
echo "6. Configure credentials"
echo "7. Create pipeline job"
echo ""
echo "Full guide: README_JENKINS.md"
echo ""
# Jenkins CI/CD Pipeline Setup

## Quick Setup on Any Machine

### Prerequisites
- Docker installed
- Docker Compose installed
- Git installed
- DockerHub account
- GitHub account

### Step 1: Start Jenkins
```bash
cd bitly_clone
docker compose -f docker-compose.jenkins.yml up -d
```

### Step 2: Get Jenkins Password
```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Step 3: Access Jenkins

Open browser: `http://YOUR_VM_IP:8080`

Use the password from Step 2.

### Step 4: Install Docker CLI in Jenkins
```bash
docker exec -u root -it jenkins bash

# Inside Jenkins container:
apt-get update
apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
apt-get install -y docker-ce-cli

# Test Docker access
docker ps

# Exit
exit
```

### Step 5: Configure Jenkins

1. Install suggested plugins
2. Create admin user
3. Add DockerHub credentials:
   - Manage Jenkins → Credentials → (global) → Add Credentials
   - Kind: Username with password
   - Username: mananurrehman
   - Password: Your DockerHub password/token
   - ID: `dockerhub-credentials` (MUST be exactly this)

4. Add GitHub credentials:
   - Same location
   - Kind: Username with password
   - Username: Your GitHub username
   - Password: GitHub Personal Access Token
   - ID: `github-credentials`

### Step 6: Create Pipeline Job

1. New Item → Name: `bitly-clone-pipeline` → Pipeline
2. Configure:
   - GitHub project: `https://github.com/mananurrehman/bitly_clone`
   - Build Triggers: ✓ Poll SCM: `H/2 * * * *`
   - Pipeline:
     - Definition: Pipeline script from SCM
     - SCM: Git
     - Repository: `https://github.com/mananurrehman/bitly_clone.git`
     - Credentials: github-credentials
     - Branch: `*/main`
     - Script Path: `Jenkinsfile`
3. Save

### Step 7: Run First Build

Click "Build Now"

## Pipeline Stages

1. **Checkout Code** - Pulls from GitHub
2. **Build Docker Image** - Creates image
3. **Push to DockerHub** - Saves to mananurrehman/bitly-clone:BUILD_NUMBER
4. **Run Tests** - Tests the image
5. **Manual Approval** - ⏸️ Waits for you to approve
6. **Deploy to VM** - Deploys on port 5000
7. **Verify Deployment** - Health check

## Useful Commands
```bash
# Start Jenkins
docker compose -f docker-compose.jenkins.yml up -d

# Stop Jenkins
docker compose -f docker-compose.jenkins.yml down

# View Jenkins logs
docker logs -f jenkins

# View deployed app logs
docker logs -f bitly_clone_app

# Check running containers
docker ps
```

## Firewall Configuration

Open these ports:
- 8080 (Jenkins)
- 5000 (Your app)

## Application Access

After successful deployment:
- Jenkins: `http://YOUR_VM_IP:8080`
- Application: `http://YOUR_VM_IP:5000`
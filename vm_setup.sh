#!/bin/bash

set -e  # exit on error

echo "🚀 Starting VM setup for Bitly Clone..."

# 1. Update system
echo "🔄 Updating system..."
sudo apt update -y && sudo apt upgrade -y

# 2. Install required packages
echo "📦 Installing prerequisite packages..."
sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    apt-transport-https

# 3. Remove old Docker versions if any
echo "🧹 Removing old Docker versions (if any)..."
sudo apt remove -y docker docker-engine docker.io containerd runc || true

# 4. Add Docker GPG key
echo "🔑 Adding Docker GPG key..."
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 5. Add Docker repository
echo "➕ Adding Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 6. Install Docker Engine & Compose
echo "🐳 Installing Docker and Docker Compose..."
sudo apt update -y
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 7. Enable & start Docker
echo "▶️ Enabling Docker service..."
sudo systemctl enable docker
sudo systemctl start docker

# 8. Add current user to docker group
echo "👤 Adding user to docker group..."
sudo usermod -aG docker $USER

# 9. Disable firewall (sandbox-friendly)
echo "🔥 Disabling UFW firewall..."
sudo ufw disable || true

# 10. Docker verification
echo "✅ Verifying Docker installation..."
docker --version
docker compose version

echo ""
echo "🎉 Setup complete!"
echo "⚠️ IMPORTANT: Logout & login again OR run:"
echo "    newgrp docker"
echo ""
echo "➡️ Then start your project with:"
echo "    docker compose up --build"
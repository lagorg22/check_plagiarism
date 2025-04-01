#!/bin/bash

set -e

echo "=== Code Plagiarism Detection System Setup ==="
echo "Setting up Docker containers..."

# Build and start all services using docker-compose
# docker-compose build
docker-compose up -d

echo "Waiting for services to start..."
sleep 15

# # Check if services are running
# echo "Checking service health..."

# check_service() {
#   local service=$1
#   local port=$2
#   echo -n "Checking $service (port $port): "
#   if curl -s http://localhost:$port/health > /dev/null; then
#     echo "✅ Ready"
#     return 0
#   else
#     echo "❌ Not ready"
#     return 1
#   fi
# }

# # Check each service
# check_service "Orchestrator" 8000
# # check_service "Indexer" 8001
# check_service "Embedding API" 8002
# check_service "Search API" 8003
# check_service "Code Processor" 8004
# check_service "LLM Service" 8005

echo ""
echo "======================Cloning the repositories========================="
echo ""

# Create a temp directory for repositories
mkdir -p temp_repos
cd temp_repos

# Define repositories to clone
REPOS=(
    "https://github.com/ej2xu/cs108.git"
    "https://github.com/abkds/cs106b-stanford.git"
    "https://github.com/lagorg22/bio.git"
    "https://github.com/lagorg22/e-commerce.git"
    "https://github.com/SoyDiego/projects-React.git"
)

# Clone each repository (using HTTPS instead of SSH for compatibility)
for repo in "${REPOS[@]}"; do
    git clone "$repo"
    echo ""
done
echo ""
echo "======================Cloning Done Successfully========================="

# Return to the parent directory
cd ..

# Copy the cloned repositories to the indexer container
echo ""
echo "Copying repositories to Docker container..."
for repo in "${REPOS[@]}"; do
    repo_name=$(basename "$repo" .git)
    if [ -d "temp_repos/$repo_name" ]; then
        echo "Copying $repo_name to container..."
        docker cp "temp_repos/$repo_name" "$(docker-compose ps -q indexer):/app/"
    fi
done

# Execute the original pipeline inside the indexer container
echo ""
echo "======================Gathering Codefiles========================="
echo ""
docker-compose exec indexer python extract_codefiles.py
echo ""
echo "======================Codefiles Gathered successfully========================="

echo ""
echo "======================Cleaning Codefiles========================="
echo ""
docker-compose exec indexer python process_codefiles.py
echo ""
echo "======================Codefiles Cleaned========================="

echo ""
echo "======================Generating Embeddings========================="
echo ""
docker-compose exec indexer python generate_embeddings.py
echo ""
echo "======================Embeddings Generated========================="

echo ""
echo "======================Removing Unnecessary Directories========================="
echo ""
docker-compose exec indexer bash -c "rm -rf /app/cs108/ /app/cs106b-stanford/ /app/bio/ /app/e-commerce/ /app/projects-React/"
echo "======================Unnecessary Directories removed========================="

# Clean up temporary repositories
echo ""
echo "Cleaning up temporary repositories..."
rm -rf temp_repos

echo ""
echo "Setup complete! Services are running with real-world code indexed."
echo "To use the system:"
echo "1. Add more code files to the shared volume if needed"
echo "2. Access the API at http://localhost:8000/check to check for plagiarism"
echo ""
echo "Example curl command to test plagiarism detection:"
echo "curl -X POST -H 'Content-Type: text/plain' --data-binary '@path/to/your/file.py' http://localhost:8000/check"
echo ""
echo "To shut down the system: docker-compose down" 
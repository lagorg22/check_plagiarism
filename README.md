# Code Plagiarism Detection System

A microservices-based system for detecting code plagiarism using embeddings and LLM analysis.

## Architecture Overview

The system consists of several microservices that work together to detect code plagiarism:

- **Orchestrator** (Port 8000): Coordinates the plagiarism detection process
- **Indexer** (Port 8001): Processes code repositories, extracts files, and generates embeddings
- **Embedding API** (Port 8002): Generates vector embeddings for code snippets
- **Search API** (Port 8003): Searches for similar code using FAISS
- **Code Processor** (Port 8004): Cleans and normalizes code
- **LLM Service** (Port 8005): Uses DeepSeek LLM to determine plagiarism
- **Evaluation** (Port 8888): evaluation script

## How It Works

1. **Indexing Process**:
   - The Indexer clones repositories and extracts code files
   - Code files are processed by the Code Processor to remove comments, blank lines, etc.
   - The Embedding API generates embeddings for each processed file
   - Embeddings are indexed using FAISS and stored in the shared volume

2. **Plagiarism Detection**:
   - User submits code to the Orchestrator
   - Orchestrator sends code to Search API
   - Search API processes the code and generates embeddings (with embedding_api)
   - Search API finds similar files using FAISS
   - Orchestrator sends user code and similar files to LLM Service
   - LLM Service reads file content and determines if code is plagiarized
   - Result is returned to the user

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Git

### Installation & Setup

1. Clone the repository:
   ```
   git clone https://github.com/lagorg22/check_plagiarism
   cd check_plagiarism
   ```

2. Run the setup script:
   ```
   #if you want to test with another repositories change them in setup.sh and process_codefiles
   chmod +x setup.sh
   ./setup.sh
   ```

3. comment the code suggested in docker-compose yaml:
   ```
   indexer is only needed for initial setup, after this it can be removed.
   ```

The setup script will:
- Build Docker containers for all services (embeddings build takes time because of huge dependencies)
- Clone repositories for indexing
- Process and index code files (takes time because of embeddings generation)
- Start all services

## Docker Configuration

The system uses Docker to containerize each service:

- Each service has its own Dockerfile and requirements.txt
- Services communicate through a Docker network
- A shared volume is used for storing code files and embeddings
- Health checks ensure services are running properly

## Directory Structure

```
check_plagiarism/
├── code_processor/       # Code cleaning service
├── embedding_api/        # Embedding generation service
├── evaluation/           # Evaluation tools and Jupyter notebook
├── indexer/              # Repository indexing service
├── llm_service/          # LLM-based plagiarism detection
├── orchestrator/         # API gateway and coordination service
├── search_api/           # FAISS-based similarity search 
├── shared/               # Shared files (mounted as a volume)
│   ├── codefiles/        # Original code files
│   ├── processed_codefiles/ # Cleaned code files
│   └── embeddings/       # Generated embeddings and FAISS index
├── docker-compose.yml    # Docker configuration
├── setup.sh              # Setup script
└── README.md             # This file
```

## API Endpoints

### Orchestrator

- `POST /check` - Check if code is plagiarized (accepts plain text code)
- `GET /health` - Health check

### LLM Service

- `POST /check_plagiarism` - Analyze code against similar files
- `GET /health` - Health check

### Search API

- `POST /search` - Find similar code files
- `GET /health` - Health check

### Code Processor

- `POST /process` - Clean and normalize code
- `POST /process_batch` - Process multiple code files
- `GET /health` - Health check

### Embedding API

- `POST /embed` - Generate embeddings for code
- `POST /embed_batch` - Generate embeddings for multiple code snippets
- `GET /health` - Health check

## Evaluation

The system includes an evaluation component for testing and measuring performance:

1. Add test files to `evaluation/original/` and `evaluation/plagiarized/` directories
2. Run the evaluation script: `python simple_evaluation.py`
3. Review results in the generated CSV and console output

## LLM Plagiarism Detection

The LLM service uses DeepSeek Coder to analyze code similarities. The prompt is designed to:
- Compare submitted code against reference files
- Look for similar code structures, variable names, and unique implementation approaches
- Consider common programming patterns and standard algorithms
- Make balanced judgments about whether code is original or plagiarized

## Shared Volume

The system uses a Docker volume to share data between services:
- `shared/codefiles/` - Original code files extracted from repositories
- `shared/processed_codefiles/` - Cleaned and normalized code
- `shared/embeddings/` - Generated embeddings and FAISS index

## Development

Each service has its own:
- Requirements file for Python dependencies
- Dockerfile for containerization

## Troubleshooting

- Check service logs: `docker-compose logs service_name`
- Verify all services are running: `docker-compose ps`
- Check service health endpoints: `curl http://localhost:PORT/health`
- Restart all services: `docker-compose restart`

## Performance Considerations

- The embedding model is resource-intensive, requiring significant memory
- Indexing large repositories can take time
- LLM inference has latency that affects response time
- FAISS search is optimized for speed but requires prebuilt indexes

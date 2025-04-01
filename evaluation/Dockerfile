FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && apt-get clean

# Install Jupyter and other evaluation dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create evaluation directories for test files
RUN mkdir -p /app/evaluation/plagiarized && \
    mkdir -p /app/evaluation/original && \
    chmod -R 777 /app/evaluation

# Copy notebook files
COPY *.ipynb /app/evaluation/
COPY *.py /app/evaluation/

# Expose Jupyter port
EXPOSE 8888

# Start Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"] 
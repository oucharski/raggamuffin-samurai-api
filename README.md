# RAGgamuffin Samurai API (RAG Study)

This project is a study on building a Retrieval-Augmented Generation (RAG) application using FastAPI, Ollama, and ChromaDB. It demonstrates how to index documents, generate responses using different models, and list available models—all through a simple API.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Endpoints](#endpoints)
  - [Indexing Endpoint](#indexing-endpoint)
  - [Generation Endpoint](#generation-endpoint)
  - [Models Endpoint](#models-endpoint)
- [Requirements](#requirements)
- [Usage](#usage)
- [Notes](#notes)

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**

   - On Windows:

     ```bash
     .venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source .venv/bin/activate
     ```

4. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The project includes a `config.py` file where you can set various configuration parameters. For example, you can specify the directory for documents:

```python
# config.py
DOCUMENTS_DIR = "@docs"
```

Place all the documents to be indexed (e.g., text files, markdown, PDFs) inside the folder defined by `DOCUMENTS_DIR`. After adding or updating documents, run the indexing endpoint to update the database.

## Endpoints

The API exposes three endpoints:

### Indexing Endpoint

- **Method:** POST  
- **URL:** `/api/index-db`  
- **Description:**  
  Initiates the process of indexing documents. The endpoint reads documents from the folder specified by `DOCUMENTS_DIR`, generates embeddings using the `mxbai-embed-large` model, and stores them in the ChromaDB collection.  
- **Usage:**  
  Add your documents to the folder and then call this endpoint to index them.

### Generation Endpoint

- **Method:** GET  
- **URL:** `/api/generate-response`  
- **Query Parameters:**  
  - `prompt`: The input prompt to generate a response for.  
  - `model`: The model to use for generation (selectable via a dropdown in Swagger; default is `llama3.2:3b`).
- **Description:**  
  Generates a response based on the provided prompt. It first generates an embedding for the prompt, queries the ChromaDB collection for the most relevant document, combines the retrieved document with the prompt, and then generates the final response using the selected model.

### Models Endpoint

- **Method:** GET  
- **URL:** `/api/list-models`  
- **Description:**  
  Lists available models by querying the Ollama service. This endpoint provides a mapping of available models (names, IDs, sizes, etc.) that you can use for response generation.

## Requirements

- **Ollama:** Must be installed and running.
- **Models:**  
  - `mxbai-embed-large` for embedding.
  - At least one generation model (e.g., `llama3.2:3b`) must be installed and running.
- **ChromaDB:** Used for storing and querying document embeddings.
- **Python Packages:**  
  - FastAPI
  - Uvicorn
  - Requests
  - PyPDF2
  - Other dependencies as listed in `requirements.txt`

## Usage

1. **Start the API:**

   ```bash
   uvicorn main:app --reload
   ```

2. **Access Swagger UI:**

   Open your browser and navigate to `http://localhost:8000/docs` to see and interact with the API endpoints.

3. **Index Documents:**

   Add your documents to the folder specified by `DOCUMENTS_DIR` (default is `@docs`), then call the `/api/index-db` endpoint (POST) to index the documents.

4. **Generate Response:**

   Use the `/api/generate-response` endpoint (GET) by specifying a prompt and selecting a model from the dropdown list to generate a response.

5. **List Models:**

   Check the `/api/list-models` endpoint (GET) to view the available models from the Ollama service.

## Notes

- This project is a study and demonstration of using FastAPI with Ollama and ChromaDB for RAG applications.
- The available models in Swagger are dynamically generated at application startup. If models change while the app is running, you may need to restart the server to update the list.
- Ensure that all required services (Ollama, the embed model, and a generation model) are installed and running before using the API.


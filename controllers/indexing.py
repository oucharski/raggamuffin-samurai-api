import os
import glob
from PyPDF2 import PdfReader
import controllers.ollama_interface as ollama_interface
from controllers.database import collection
from config import DOCUMENTS_DIR

def read_file_content(file_path: str) -> str:
    """
    Reads file content based on its extension.
    Supports:
      - .txt and .md: Reads plain text.
      - .pdf: Extracts text using PyPDF2.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".txt", ".md"]:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    elif ext == ".pdf":
        try:
            reader = PdfReader(file_path)
            content = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    content += page_text + "\n"
            return content.strip()
        except Exception as e:
            raise Exception(f"Failed to read PDF file {file_path}: {e}")
    else:
        raise Exception(f"Unsupported file extension: {ext}")

def index_documents():
    """
    Reads all .txt, .md, and .pdf files from the DOCUMENTS_DIR and indexes them.
    """
    # Check if the Ollama service is available.
    ollama_interface.check_service()

    # Get all files with supported extensions in DOCUMENTS_DIR.
    pattern = os.path.join(DOCUMENTS_DIR, "*")
    all_files = glob.glob(pattern)
    files = [f for f in all_files if os.path.splitext(f)[1].lower() in [".txt", ".md", ".pdf"]]
    
    if not files:
        raise Exception("No document files found in the 'documents' directory.")
    
    for file_path in files:
        content = read_file_content(file_path)
        # Generate the embedding for the document.
        response = ollama_interface.embed_text(model="mxbai-embed-large", text=content)
        embeddings = response["embeddings"]
        # Use the filename as a unique identifier.
        doc_id = os.path.basename(file_path)
        # Upsert the document and its embedding in the collection.
        collection.upsert(
            ids=[doc_id],
            embeddings=embeddings,
            documents=[content]
        )
    return {"message": f"Indexed {len(files)} documents successfully."}

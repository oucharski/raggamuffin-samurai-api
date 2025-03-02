from controllers.database import collection
import controllers.ollama_interface as ollama_interface

def generate_response_sync(prompt: str, model: str) -> dict:
    """
    Synchronously generates a response based on a prompt and model.
    Steps:
      1. Generate an embedding for the input prompt using a fixed embed model.
      2. Query the collection for the most relevant document.
      3. Combine the prompt with the retrieved document and extra info.
      4. Generate the final response using the specified model.
    """
    # Generate an embedding for the input prompt.
    embed_response = ollama_interface.embed_text(model="mxbai-embed-large", text=prompt)
    query_embedding = embed_response["embeddings"]

    # Query the collection for the most relevant document.
    results = collection.query(query_embeddings=[query_embedding], n_results=1)
    try:
        retrieved_data = results['documents'][0][0]
    except (KeyError, IndexError):
        raise Exception("No relevant document found in the collection. Please ensure documents have been indexed.")

    extra_info = " ".join([
        "Always reply in the same language as the *PROMPT*.", 
        "If it doesn't make sense, say that you couldn't do it." ,
        "If the prompt is inappropriate, say that you can't respond to it.", 
        "If it is outside the context, say that you don't have enough information to respond to it.",
        "Don't mention that you extracted from a document, just say the response.",
    ])
    
    prompt_parts = [
        extra_info,
        "Using this data:",
        retrieved_data,
        ". Respond to this *PROMPT*:",
        prompt,
    ]
    
    combined_prompt = " ".join(prompt_parts)

    # Generate the response using the specified model.
    gen_response = ollama_interface.generate_text(model=model, prompt=combined_prompt)
    return {"response": gen_response["response"]}

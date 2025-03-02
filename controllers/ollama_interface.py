import ollama
import subprocess
import json
import re

def flatten_embedding(embedding):
    """
    Flattens the embedding list if it's unnecessarily nested.
    For example, converts [[[0.1, 0.2, ...]]] to [0.1, 0.2, ...].
    """
    while isinstance(embedding, list) and len(embedding) == 1:
        embedding = embedding[0]
    return embedding

def check_service():
    """
    Checks if the Ollama service is up and running by sending a simple health check.
    Raises an exception if the service is not available.
    """
    try:
        response = ollama.embed(model="mxbai-embed-large", input="health check")
        if "embeddings" not in response:
            raise Exception("Ollama health check failed: unexpected response format.")
    except Exception as e:
        raise Exception("Ollama service is not running or not responding: " + str(e))

def embed_text(model: str, text: str):
    """
    Generates an embedding for the given text using the specified model.
    Flattens the returned embedding if necessary.
    """
    response = ollama.embed(model=model, input=text)
    embedding = response.get("embeddings")
    flattened = flatten_embedding(embedding)
    response["embeddings"] = flattened
    return response

def generate_text(model: str, prompt: str):
    """
    Generates a response using the given model and prompt.
    """
    return ollama.generate(model=model, prompt=prompt)

def check_model_availability(model: str):
    """
    Checks if the given model is available by making a dummy generation call.
    If the error message contains "model" and "not found", it appends a comma-separated list of available model names.
    """
    try:
        # Send a dummy prompt.
        response = ollama.generate(model=model, prompt="Test")
        if "response" not in response:
            raise Exception(f"Model {model} did not return a valid response.")
    except Exception as e:
        error_message = str(e)
        if "model" in error_message.lower() and "not found" in error_message.lower():
            try:
                from ollama_interface import list_available_models
                available_models = list_available_models()
                # Map available model names and join them with commas.
                names = [entry["NAME"] for entry in available_models if "NAME" in entry]
                available_models_str = ", ".join(names)
            except Exception as list_e:
                available_models_str = f"Error retrieving available models: {list_e}"
            raise Exception(f"{error_message}. Available models: {available_models_str}")
        else:
            raise Exception(error_message)


def list_available_models():
    """
    Runs the `ollama list` command and returns the available models.
    Parses the output and returns structured model info.
    """
    def parse_models(response):
        # The first line is the header, so we remove it
        header_line = response["models"][0]
        headers = re.split(r"\s{2,}", header_line.strip())
        
        parsed_models = []
        for line in response["models"][1:]:
            # Split by two or more spaces
            parts = re.split(r"\s{2,}", line.strip())
            # Create a dict mapping each header to its corresponding part
            model_info = dict(zip(headers, parts))
            parsed_models.append(model_info)
        return parsed_models

    try:
        # Run the command "ollama list"
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        output = result.stdout.strip()

        # Try parsing the output as JSON first.
        # If JSON parsing fails, assume it's plain text.
        try:
            parsed_json = json.loads(output)
            models = parse_models(parsed_json)
        except json.JSONDecodeError:
            # Split the output by newlines and build a fake dict.
            lines = output.splitlines()
            if not lines:
                raise Exception("No output from 'ollama list' command.")
            response = {"models": lines}
            models = parse_models(response)
        return models
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to list models: {e.stderr}")
# models_enum.py
from enum import Enum
from controllers.ollama_interface import list_available_models

# Get available models at startup.
try:
    available_models = list_available_models()
    # Extract model names. Adjust the key if necessary.
    model_names = [entry["NAME"] for entry in available_models if "NAME" in entry]
except Exception as e:
    # Fallback to a default list if something goes wrong.
    model_names = []

# Dynamically create an Enum with these models.
ModelEnum = Enum("ModelEnum", {name: name for name in model_names})

# Chatbot with function calling + short term memory

A simple chatbot with function calling and short term memory written using streamlit

## Run locally
`streamlit run main.py`

## Dependencies
1. `pip install -r requirements.txt`
2. Ollama server with llama3:8b-instruct-q8_0 model. When llama is run first time, execute shell inside the container and pull the model `ollama pull llama3:8b-instruct-q8_0`

### Ollama model server
```bash
services:  
  ollama:
    container_name: ollama
    image: ollama/ollama
    ports:
      - "11434:11434"
    deploy:
      resources:
        reservations:
          devices:
          - capabilities: ["gpu"]
    volumes:
      - ollama:/root/.ollama
    restart: unless-stopped

volumes:
    ollama:
```

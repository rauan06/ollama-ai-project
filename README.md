# Ollama AI project

Initialize the docker
```bash
docker build -t ollama-image .
```

Install the requirements
```bash
pip install -r requirements.txt
```

Install the light AI model
```bash
curl http://localhost:11434/api/pull -d '{
  "model": "qwen2.5:0.5b"
}'
```

Start the app 
```bash
streamlit run app.py
```

# Bella AI - Streamlit App

This is a simple Streamlit chat application (Bella AI) meant as a personal AI companion gift for Bella.
It uses OpenRouter-compatible LLM endpoints. Replace `OPENROUTER_API_KEY` with your key in Streamlit sidebar or set environment variable.

## Files
- `app.py` - main Streamlit app
- `assets/` - place your images here (`bella.jpg`, `groot.jpg`, `bella logo.png`)
- `memory/` - persistent memory JSON will be stored here
- `requirements.txt` - python dependencies

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy
- Streamlit Community Cloud: push repo, set secret `OPENROUTER_API_KEY` and deploy.
- Railway/Heroku: configure environment variable `OPENROUTER_API_KEY`, port, and start command:
```
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

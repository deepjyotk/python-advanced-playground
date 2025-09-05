.PHONY: frontend backend

# Run the backend FastAPI server
backend:
	source .venv/bin/activate && python backend_fastapi.py

# Run the frontend and open it in the default browser
frontend:
	python -m webbrowser -t "http://localhost:8080" && python -m http.server 8080
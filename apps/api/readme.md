# API for bash 

Build & run via Docker Compose (root):

$ cp .env.example .env
# edit .env if needed
$ docker compose up --build

# Health: http://localhost:8000/health
# Create case:
POST /v1/cases
{ "title": "...", "narrative":"...", "media":["http://..."] }

# lms-python

### Linux/Mac
```bash
cp .env.example .env
docker compose up -d
uv sync
uv run task -r data/rooms.json -s data/students.json
```

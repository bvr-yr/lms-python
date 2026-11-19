# lms-python

## Linux/Mac

### Setup

```bash
cp .env.example .env
docker compose up -d
uv sync
```

### Run

```bash
uv run task -r data/rooms.json -s data/students.json
```

### Tests
```bash
# export TEST_LIVE_DB=1 # connection test with container running
uv run pytest -v
```

# Demo 1: Standing up the Tracker Service

**Time Budget:** 3-4 mins

### 1) Clean up and inspect
```bash
docker stop finops-issue-tracker 2>/dev/null || true
docker rm finops-issue-tracker 2>/dev/null || true
find sections/08-issue-tracker-service/service -maxdepth 3 -type f | sort
```

### 2) Build the Docker image
```bash
docker build -t finops-issue-tracker:latest sections/08-issue-tracker-service/service
```

### 3) Run the tracker container (In a second terminal)
```bash
docker run --rm -p 8085:8000 -p 8086:8001 --name finops-issue-tracker finops-issue-tracker:latest
```

### 4) Open the board UI and FastAPI docs
- Board: `http://localhost:8085`
- Docs: `http://localhost:8085/docs`

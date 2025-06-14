# Dummy FastAPI App for Load Testing

## Features
- `/health`: Health check endpoint
- `/write`: POST endpoint to insert a message into PostgreSQL
- `/read`: GET endpoint to fetch all messages

---

**Directory structure:**
- dummy-app/
    - app.py
    - requirements.txt
    - Dockerfile
    - k8s-deployment.yaml
    - k8s-service.yaml
    - README.md

---

### app.py
```python
import os
import asyncpg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")
DB_NAME = os.getenv("DB_NAME", "postgres")

class Message(BaseModel):
    content: str

@app.on_event("startup")
async def startup():
    app.state.pool = await asyncpg.create_pool(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, database=DB_NAME
    )
    async with app.state.pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id serial PRIMARY KEY,
                content text NOT NULL,
                created_at timestamp NOT NULL DEFAULT now()
            )
        ''')

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/write")
async def write_message(msg: Message):
    try:
        async with app.state.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO messages (content, created_at) VALUES ($1, $2)",
                msg.content, datetime.utcnow()
            )
        return {"result": "written"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
async def read_messages():
    try:
        async with app.state.pool.acquire() as conn:
            rows = await conn.fetch("SELECT id, content, created_at FROM messages ORDER BY id DESC LIMIT 100")
        return [{"id": r["id"], "content": r["content"], "created_at": r["created_at"].isoformat()} for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

### requirements.txt
```
fastapi
uvicorn[standard]
asyncpg
```

---

### Dockerfile
```
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py ./
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

### k8s-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dummy-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: dummy-app
  template:
    metadata:
      labels:
        app: dummy-app
    spec:
      containers:
      - name: dummy-app
        image: <your-docker-repo>/dummy-app:latest
        ports:
        - containerPort: 8080
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: pgsql-credentials
              key: host
        - name: DB_PORT
          value: "5432"
        - name: DB_USER
          valueFrom:
            secretKeyRef:
              name: pgsql-credentials
              key: user
        - name: DB_PASS
          valueFrom:
            secretKeyRef:
              name: pgsql-credentials
              key: password
        - name: DB_NAME
          valueFrom:
            secretKeyRef:
              name: pgsql-credentials
              key: dbname
```

---

### k8s-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: dummy-app
spec:
  type: ClusterIP
  selector:
    app: dummy-app
  ports:
    - port: 80
      targetPort: 8080
```

---

### README.md
```
# Dummy FastAPI App

- `/health`: Health check
- `/write`: POST JSON `{ "content": "..." }` to write a message
- `/read`: GET to fetch last 100 messages

Configure DB connection via environment variables. See k8s manifests for example.
```

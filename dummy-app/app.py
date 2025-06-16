import os
import asyncpg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import hashlib
import secrets

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")
DB_NAME = os.getenv("DB_NAME", "dummydb")

class Message(BaseModel):
    content: str

@asynccontextmanager
async def lifespan(app: FastAPI):
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
    yield
    await app.state.pool.close()

app.router.lifespan_context = lifespan

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

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

@app.get("/compute")
async def compute_hash(iterations: int = 100000):
    "Perform a CPU-intensive hash computation to generate load and store the result in the database."
    data = secrets.token_bytes(256)
    result = data
    for _ in range(iterations):
        result = hashlib.sha256(result).digest()
    hash_hex = result.hex()
    # Store the hash result in the database
    try:
        async with app.state.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO messages (content, created_at) VALUES ($1, $2)",
                f"hash:{hash_hex}", datetime.utcnow()
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hash computed but DB insert failed: {str(e)}")
    return {"hash": hash_hex, "iterations": iterations}

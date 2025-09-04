import time
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
    
@app.get("/pgsql/latency")
async def pgsql_latency():
    result = {}
    # Connection latency
    conn_start = time.perf_counter()
    try:
        async with app.state.pool.acquire() as conn:
            conn_latency = (time.perf_counter() - conn_start) * 1000
            result["connection_latency_ms"] = conn_latency
            # Bulk write latency
            write_start = time.perf_counter()
            await conn.execute("CREATE TABLE IF NOT EXISTS latency_test (id SERIAL PRIMARY KEY, val TEXT)")
            await conn.execute("DELETE FROM latency_test")
            for i in range(1000):
                await conn.execute("INSERT INTO latency_test (val) VALUES ($1)", f"row-{i}")
            write_latency = (time.perf_counter() - write_start) * 1000
            result["bulk_write_latency_ms"] = write_latency
            # Bulk read latency
            read_start = time.perf_counter()
            rows = await conn.fetch("SELECT * FROM latency_test")
            read_latency = (time.perf_counter() - read_start) * 1000
            result["bulk_read_latency_ms"] = read_latency
            result["bulk_read_rowcount"] = len(rows)
            # Transaction commit latency
            txn_start = time.perf_counter()
            async with conn.transaction():
                await conn.execute("INSERT INTO latency_test (val) VALUES ('txn-test')")
            txn_latency = (time.perf_counter() - txn_start) * 1000
            result["transaction_commit_latency_ms"] = txn_latency
    except Exception as e:
        result["error"] = str(e)
    return result

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

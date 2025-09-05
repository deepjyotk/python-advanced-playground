# server.py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Simulate streaming logs
async def log_generator():
    for i in range(1, 6):
        await asyncio.sleep(1)  # simulate delay
        yield f"Log entry {i}\n"  # chunk sent immediately

# 1. Normal endpoint: waits for all data
@app.get("/final-logs")
async def final_logs():
    logs = []
    for i in range(1, 6):
        await asyncio.sleep(1)
        logs.append(f"Log entry {i}")
    return {"logs": logs}  # sent as one big JSON at the end

# 2. Streaming endpoint: sends chunks one by one
@app.get("/stream-logs")
async def stream_logs():
    return StreamingResponse(log_generator(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

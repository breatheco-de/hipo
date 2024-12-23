from fastapi import FastAPI, HTTPException
from src.services.redis_manager import redis_manager
import uvicorn

app = FastAPI()

@app.get("/storage/{key}")
async def get_key(key: str):
    try:
        # Retrieve the value from Redis using the key
        value = redis_manager.get(key)
        if value is None:
            raise HTTPException(status_code=404, detail="Key not found")
        return value
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)


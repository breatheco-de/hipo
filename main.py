from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
import tempfile
import shutil

from src.services.redis_manager import redis_manager
import uvicorn
import whisper

model = whisper.load_model("base")
app = FastAPI()

# Serve static files (index.html) at "/playground"
app.mount("/playground", StaticFiles(directory="static", html=True), name="playground")


@app.get("/storage/{key}")
async def get_key(key: str):
    try:
        # Retrieve the value from Redis using the key
        value = redis_manager.get(key)
        if value is None:
            raise HTTPException(status_code=404, detail="Key not found")
        return PlainTextResponse(content=value, media_type="text/plain")
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    # Save file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        shutil.copyfileobj(file.file, temp_audio)
        temp_audio_path = temp_audio.name

    # Transcribe the audio
    result = model.transcribe(temp_audio_path)

    print(result["text"], "result")

    return {"filename": file.filename, "transcription": result["text"]}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)

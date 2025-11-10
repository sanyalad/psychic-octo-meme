"""
FastAPI backend for Audio-to-Sheet Music Transcription
"""
import os
import uuid
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import aiofiles

from audio_processor import AudioProcessor

# Configuration
UPLOAD_DIR = Path("./uploads")
TEMP_DIR = Path("./temp")
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {".wav", ".mp3", ".ogg", ".flac", ".m4a"}

# Ensure directories exist
UPLOAD_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Initialize FastAPI app
app = FastAPI(
    title="Audio-to-Sheet Music API",
    description="API for transcribing audio files to sheet music notation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize audio processor
audio_processor = AudioProcessor()

# Storage for transcription results
transcriptions = {}


class TranscriptionResponse(BaseModel):
    """Response model for transcription"""
    transcription_id: str
    status: str
    message: str
    midi_file: Optional[str] = None
    musicxml_file: Optional[str] = None
    created_at: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    timestamp: str


def cleanup_old_files():
    """Remove files older than 24 hours"""
    now = datetime.now()
    for directory in [UPLOAD_DIR, TEMP_DIR]:
        for file_path in directory.glob("*"):
            if file_path.is_file():
                file_age = now - datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_age > timedelta(hours=24):
                    file_path.unlink()


def validate_audio_file(filename: str) -> bool:
    """Validate if file extension is allowed"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint"""
    return HealthResponse(
        status="ok",
        message="Audio-to-Sheet Music API is running",
        timestamp=datetime.now().isoformat()
    )


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="API is operational",
        timestamp=datetime.now().isoformat()
    )


@app.post("/api/upload", response_model=TranscriptionResponse)
async def upload_audio(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Upload an audio file for transcription
    
    Args:
        file: Audio file (WAV, MP3, OGG, FLAC, M4A)
        
    Returns:
        TranscriptionResponse with transcription_id
    """
    # Validate file extension
    if not validate_audio_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Generate unique ID
    transcription_id = str(uuid.uuid4())
    
    # Save uploaded file
    file_extension = Path(file.filename).suffix
    upload_path = UPLOAD_DIR / f"{transcription_id}{file_extension}"
    
    try:
        # Read and save file
        content = await file.read()
        
        # Check file size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        async with aiofiles.open(upload_path, 'wb') as f:
            await f.write(content)
        
        # Store transcription info
        transcriptions[transcription_id] = {
            "status": "uploaded",
            "filename": file.filename,
            "upload_path": str(upload_path),
            "created_at": datetime.now().isoformat()
        }
        
        # Schedule cleanup
        if background_tasks:
            background_tasks.add_task(cleanup_old_files)
        
        return TranscriptionResponse(
            transcription_id=transcription_id,
            status="uploaded",
            message="File uploaded successfully. Use /api/transcribe to process.",
            created_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        # Cleanup on error
        if upload_path.exists():
            upload_path.unlink()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.post("/api/transcribe/{transcription_id}", response_model=TranscriptionResponse)
async def transcribe_audio(transcription_id: str):
    """
    Transcribe uploaded audio file to MIDI and MusicXML
    
    Args:
        transcription_id: ID from upload endpoint
        
    Returns:
        TranscriptionResponse with file paths
    """
    # Check if transcription exists
    if transcription_id not in transcriptions:
        raise HTTPException(status_code=404, detail="Transcription not found")
    
    transcription = transcriptions[transcription_id]
    
    # Check if already processed
    if transcription["status"] == "completed":
        return TranscriptionResponse(
            transcription_id=transcription_id,
            status="completed",
            message="Already transcribed",
            midi_file=transcription.get("midi_file"),
            musicxml_file=transcription.get("musicxml_file"),
            created_at=transcription["created_at"]
        )
    
    try:
        # Update status
        transcription["status"] = "processing"
        
        # Process audio
        upload_path = Path(transcription["upload_path"])
        result = await audio_processor.transcribe(
            str(upload_path),
            transcription_id,
            str(TEMP_DIR)
        )
        
        # Update transcription info
        transcription.update({
            "status": "completed",
            "midi_file": result["midi_file"],
            "musicxml_file": result.get("musicxml_file"),
            "notes_detected": result.get("notes_detected", 0)
        })
        
        return TranscriptionResponse(
            transcription_id=transcription_id,
            status="completed",
            message="Transcription completed successfully",
            midi_file=result["midi_file"],
            musicxml_file=result.get("musicxml_file"),
            created_at=transcription["created_at"]
        )
        
    except Exception as e:
        transcription["status"] = "failed"
        transcription["error"] = str(e)
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@app.get("/api/download/{transcription_id}/{file_type}")
async def download_file(transcription_id: str, file_type: str):
    """
    Download transcribed file (MIDI or MusicXML)
    
    Args:
        transcription_id: ID from upload endpoint
        file_type: 'midi' or 'musicxml'
        
    Returns:
        File download
    """
    # Check if transcription exists
    if transcription_id not in transcriptions:
        raise HTTPException(status_code=404, detail="Transcription not found")
    
    transcription = transcriptions[transcription_id]
    
    # Check if completed
    if transcription["status"] != "completed":
        raise HTTPException(status_code=400, detail="Transcription not completed")
    
    # Get file path
    if file_type == "midi":
        file_path = transcription.get("midi_file")
    elif file_type == "musicxml":
        file_path = transcription.get("musicxml_file")
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Use 'midi' or 'musicxml'")
    
    if not file_path or not Path(file_path).exists():
        raise HTTPException(status_code=404, detail=f"{file_type.upper()} file not found")
    
    # Return file
    filename = Path(file_path).name
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )


@app.get("/api/status/{transcription_id}")
async def get_status(transcription_id: str):
    """
    Get transcription status
    
    Args:
        transcription_id: ID from upload endpoint
        
    Returns:
        Status information
    """
    if transcription_id not in transcriptions:
        raise HTTPException(status_code=404, detail="Transcription not found")
    
    return JSONResponse(content=transcriptions[transcription_id])


@app.delete("/api/transcription/{transcription_id}")
async def delete_transcription(transcription_id: str):
    """
    Delete transcription and associated files
    
    Args:
        transcription_id: ID from upload endpoint
        
    Returns:
        Success message
    """
    if transcription_id not in transcriptions:
        raise HTTPException(status_code=404, detail="Transcription not found")
    
    transcription = transcriptions[transcription_id]
    
    # Delete files
    for key in ["upload_path", "midi_file", "musicxml_file"]:
        if key in transcription:
            file_path = Path(transcription[key])
            if file_path.exists():
                file_path.unlink()
    
    # Remove from storage
    del transcriptions[transcription_id]
    
    return {"message": "Transcription deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

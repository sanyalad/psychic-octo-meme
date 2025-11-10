"""
Audio processing and transcription module using Basic Pitch
"""
import os
from pathlib import Path
from typing import Dict, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH


class AudioProcessor:
    """Handles audio transcription using Basic Pitch"""
    
    def __init__(self):
        """Initialize the audio processor"""
        self.model_path = ICASSP_2022_MODEL_PATH
        self.executor = ThreadPoolExecutor(max_workers=2)
    
    async def transcribe(
        self,
        audio_path: str,
        transcription_id: str,
        output_dir: str
    ) -> Dict[str, any]:
        """
        Transcribe audio file to MIDI and MusicXML
        
        Args:
            audio_path: Path to input audio file
            transcription_id: Unique ID for this transcription
            output_dir: Directory to save output files
            
        Returns:
            Dictionary with paths to generated files and metadata
        """
        # Run transcription in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor,
            self._transcribe_sync,
            audio_path,
            transcription_id,
            output_dir
        )
        return result
    
    def _transcribe_sync(
        self,
        audio_path: str,
        transcription_id: str,
        output_dir: str
    ) -> Dict[str, any]:
        """
        Synchronous transcription (runs in thread pool)
        
        Args:
            audio_path: Path to input audio file
            transcription_id: Unique ID for this transcription
            output_dir: Directory to save output files
            
        Returns:
            Dictionary with paths to generated files and metadata
        """
        try:
            # Prepare output paths
            output_dir_path = Path(output_dir)
            midi_path = output_dir_path / f"{transcription_id}.mid"
            
            # Run Basic Pitch prediction
            # predict() returns: model_output, midi_data, note_events
            model_output, midi_data, note_events = predict(
                audio_path,
                self.model_path
            )
            
            # Save MIDI file
            midi_data.write(str(midi_path))
            
            # Count detected notes
            notes_detected = len(note_events) if note_events is not None else 0
            
            # Prepare result
            result = {
                "midi_file": str(midi_path),
                "notes_detected": notes_detected,
                "status": "success"
            }
            
            # Try to generate MusicXML using music21 (optional)
            try:
                musicxml_path = self._convert_to_musicxml(
                    str(midi_path),
                    transcription_id,
                    output_dir
                )
                if musicxml_path:
                    result["musicxml_file"] = musicxml_path
            except Exception as e:
                # MusicXML generation is optional, don't fail if it doesn't work
                print(f"Warning: MusicXML generation failed: {e}")
            
            return result
            
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    def _convert_to_musicxml(
        self,
        midi_path: str,
        transcription_id: str,
        output_dir: str
    ) -> Optional[str]:
        """
        Convert MIDI to MusicXML using music21
        
        Args:
            midi_path: Path to MIDI file
            transcription_id: Unique ID for this transcription
            output_dir: Directory to save output file
            
        Returns:
            Path to MusicXML file or None if conversion fails
        """
        try:
            from music21 import converter, stream
            
            # Load MIDI file
            score = converter.parse(midi_path)
            
            # Prepare output path
            output_dir_path = Path(output_dir)
            musicxml_path = output_dir_path / f"{transcription_id}.musicxml"
            
            # Write MusicXML
            score.write('musicxml', fp=str(musicxml_path))
            
            return str(musicxml_path)
            
        except Exception as e:
            print(f"MusicXML conversion error: {e}")
            return None
    
    def get_audio_info(self, audio_path: str) -> Dict[str, any]:
        """
        Get information about audio file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary with audio metadata
        """
        try:
            import librosa
            
            # Load audio
            y, sr = librosa.load(audio_path, sr=None)
            
            # Calculate duration
            duration = librosa.get_duration(y=y, sr=sr)
            
            return {
                "duration": duration,
                "sample_rate": sr,
                "samples": len(y),
                "channels": 1 if y.ndim == 1 else y.shape[0]
            }
            
        except Exception as e:
            return {"error": str(e)}

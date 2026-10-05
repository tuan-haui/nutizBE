import ffmpeg
import os
import uuid
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class FfmpegService:
    def __init__(self):
        self.output_dir = "downloads"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def convert_audio(self, input_path: str, format: str, bitrate: str = "192k") -> str:
        filename = f"{uuid.uuid4()}.{format}"
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            (
                ffmpeg
                .input(input_path)
                .output(output_path, audio_bitrate=bitrate)
                .overwrite_output()
                .run(quiet=True)
            )
            return output_path
        except ffmpeg.Error as e:
            logger.error(f"FFmpeg error: {e.stderr}")
            raise Exception("FFmpeg conversion failed")

    def trim_audio(self, input_path: str, start: int, end: int) -> str:
        filename = f"trimmed_{uuid.uuid4()}.mp3"
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            (
                ffmpeg
                .input(input_path, ss=start, to=end)
                .output(output_path)
                .overwrite_output()
                .run(quiet=True)
            )
            return output_path
        except ffmpeg.Error as e:
            logger.error(f"FFmpeg error: {e.stderr}")
            raise Exception("FFmpeg trim failed")

ffmpeg_service = FfmpegService()

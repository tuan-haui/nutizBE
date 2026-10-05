import yt_dlp
import os
import uuid
import base64
from pathlib import Path
from typing import Dict, Any
from app.core.config import settings

class YtDlpService:
    def __init__(self):
        self.cookie_path = None
        if settings.YOUTUBE_COOKIES_BASE64:
            try:
                # Use a temp directory
                temp_dir = Path(os.environ.get("TEMP", "/tmp"))
                self.cookie_path = temp_dir / "youtube_cookies.txt"
                self.cookie_path.write_bytes(base64.b64decode(settings.YOUTUBE_COOKIES_BASE64))
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Failed to decode YOUTUBE_COOKIES_BASE64: {e}")

    def _get_base_opts(self) -> Dict[str, Any]:
        opts = {
            'quiet': True,
            'no_warnings': True,
        }
        if self.cookie_path and self.cookie_path.exists():
            opts['cookiefile'] = str(self.cookie_path)
        return opts

    def get_info(self, url: str) -> Dict[str, Any]:
        ydl_opts = self._get_base_opts()
        ydl_opts['extract_flat'] = False
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info

    def get_formats(self, url: str) -> Dict[str, Any]:
        return self.get_info(url)
        
    def extract_audio(self, url: str) -> Dict[str, Any]:
        ydl_opts = self._get_base_opts()
        ydl_opts['format'] = 'bestaudio/best'
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    def extract_video(self, url: str) -> Dict[str, Any]:
        ydl_opts = self._get_base_opts()
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
            
    def extract_best(self, url: str) -> Dict[str, Any]:
        ydl_opts = self._get_base_opts()
        ydl_opts['format'] = 'best'
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    def search(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        search_query = f"ytsearch{max_results}:{query}"
        ydl_opts = self._get_base_opts()
        ydl_opts['extract_flat'] = True
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(search_query, download=False)
            
    def download_audio(self, url: str, format: str = "mp3", quality: str = "192") -> str:
        filename = f"{uuid.uuid4()}"
        outmpl = os.path.join("downloads", f"{filename}.%(ext)s")
        
        ydl_opts = self._get_base_opts()
        ydl_opts.update({
            'format': 'bestaudio/best',
            'outtmpl': outmpl,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,
                'preferredquality': quality,
            }]
        })
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return os.path.join("downloads", f"{filename}.{format}")

    def download_video(self, url: str, format: str = "mp4", quality: str = "720p") -> str:
        filename = f"{uuid.uuid4()}"
        outmpl = os.path.join("downloads", f"{filename}.%(ext)s")
        
        # Simple quality mapping
        format_str = f'bestvideo[height<={quality.replace("p","")}]+bestaudio/best' if quality else 'best'
        
        ydl_opts = self._get_base_opts()
        ydl_opts.update({
            'format': format_str,
            'outtmpl': outmpl,
            'merge_output_format': format
        })
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return os.path.join("downloads", f"{filename}.{format}")

ytdlp_service = YtDlpService()

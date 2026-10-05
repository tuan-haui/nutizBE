import yt_dlp
from typing import Dict, Any

class YtDlpService:
    def get_info(self, url: str) -> Dict[str, Any]:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info

    def get_formats(self, url: str) -> Dict[str, Any]:
        return self.get_info(url)
        
    def extract_audio(self, url: str) -> Dict[str, Any]:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'bestaudio/best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    def extract_video(self, url: str) -> Dict[str, Any]:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
            
    def extract_best(self, url: str) -> Dict[str, Any]:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
            
    def download_audio(self, url: str, format: str = "mp3", quality: str = "192") -> str:
        import uuid
        import os
        filename = f"{uuid.uuid4()}"
        outmpl = os.path.join("downloads", f"{filename}.%(ext)s")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': outmpl,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,
                'preferredquality': quality,
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return os.path.join("downloads", f"{filename}.{format}")

    def download_video(self, url: str, format: str = "mp4", quality: str = "720p") -> str:
        import uuid
        import os
        filename = f"{uuid.uuid4()}"
        outmpl = os.path.join("downloads", f"{filename}.%(ext)s")
        
        # Simple quality mapping
        format_str = f'bestvideo[height<={quality.replace("p","")}]+bestaudio/best' if quality else 'best'
        
        ydl_opts = {
            'format': format_str,
            'outtmpl': outmpl,
            'merge_output_format': format,
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return os.path.join("downloads", f"{filename}.{format}")

ytdlp_service = YtDlpService()

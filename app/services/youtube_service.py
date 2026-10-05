from app.services.ytdlp_service import YtDlpService
from app.schemas.youtube import (
    VideoInfoResponse, VideoFormatsResponse, FormatInfo, 
    ExtractMediaResponse, MediaInfo, ChannelInfo
)
from app.core.exceptions import AppException
import logging

logger = logging.getLogger(__name__)

class YoutubeService:
    def __init__(self, ytdlp_service: YtDlpService):
        self.ytdlp = ytdlp_service

    def _handle_error(self, e: Exception, url: str):
        logger.error(f"yt-dlp error for {url}: {str(e)}")
        error_msg = str(e).lower()
        if "not found" in error_msg or "video isn't available" in error_msg:
            raise AppException(code="VIDEO_NOT_FOUND", message="The requested video is not found.", status_code=404)
        elif "unavailable" in error_msg:
            raise AppException(code="VIDEO_UNAVAILABLE", message="The requested video is unavailable.", status_code=400)
        elif "private" in error_msg:
            raise AppException(code="VIDEO_PRIVATE", message="The requested video is private.", status_code=403)
        elif "age" in error_msg and "restrict" in error_msg:
            raise AppException(code="VIDEO_AGE_RESTRICTED", message="The requested video is age restricted.", status_code=403)
        elif "unsupported url" in error_msg:
            raise AppException(code="UNSUPPORTED_URL", message="The URL is not supported.", status_code=400)
        else:
            raise AppException(code="EXTRACTION_FAILED", message="Failed to extract video information.", status_code=500)

    def get_info(self, url: str) -> VideoInfoResponse:
        try:
            info = self.ytdlp.get_info(url)
            channel = None
            if info.get('channel_id'):
                channel = ChannelInfo(id=info.get('channel_id'), name=info.get('channel'))
            
            return VideoInfoResponse(
                id=info.get('id', ''),
                title=info.get('title', ''),
                description=info.get('description'),
                duration=info.get('duration'),
                thumbnail=info.get('thumbnail'),
                channel=channel,
                view_count=info.get('view_count'),
                upload_date=info.get('upload_date'),
                webpage_url=info.get('webpage_url', url)
            )
        except Exception as e:
            self._handle_error(e, url)

    def get_formats(self, url: str) -> VideoFormatsResponse:
        try:
            info = self.ytdlp.get_formats(url)
            formats = []
            for f in info.get('formats', []):
                # Filter out some useless formats or just parse them
                vcodec = f.get('vcodec')
                acodec = f.get('acodec')
                has_video = vcodec != 'none'
                has_audio = acodec != 'none'
                
                formats.append(FormatInfo(
                    format_id=str(f.get('format_id', '')),
                    ext=f.get('ext', ''),
                    resolution=f.get('format_note') or f.get('resolution'),
                    fps=f.get('fps'),
                    filesize=f.get('filesize'),
                    abr=f.get('abr'),
                    has_video=has_video,
                    has_audio=has_audio
                ))
            
            return VideoFormatsResponse(
                video_id=info.get('id', ''),
                formats=formats
            )
        except Exception as e:
            self._handle_error(e, url)

    def extract_media(self, url: str, media_type: str) -> ExtractMediaResponse:
        try:
            if media_type == 'audio':
                info = self.ytdlp.extract_audio(url)
            elif media_type == 'video':
                info = self.ytdlp.extract_video(url)
            else:
                info = self.ytdlp.extract_best(url)
                
            return ExtractMediaResponse(
                video_id=info.get('id', ''),
                title=info.get('title', ''),
                duration=info.get('duration'),
                media=MediaInfo(
                    url=info.get('url', ''),
                    type=media_type,
                    format=info.get('ext', ''),
                    mime_type=None,
                    duration=info.get('duration')
                )
            )
        except Exception as e:
            self._handle_error(e, url)

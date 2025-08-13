"""
Video downloader module using yt-dlp for actual video downloading.
This provides real video downloading functionality.
"""

import os
import logging
import yt_dlp
from typing import Optional, Dict, Any, Tuple

logger = logging.getLogger(__name__)

class VideoDownloader:
    def __init__(self, download_folder: str = "temp_files"):
        self.download_folder = download_folder
        os.makedirs(download_folder, exist_ok=True)
        
        # Configure yt-dlp options
        self.ydl_opts = {
            'outtmpl': os.path.join(download_folder, '%(id)s_%(resolution)s.%(ext)s'),
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
    
    def get_video_info(self, url: str) -> Tuple[Optional[Dict], Optional[str]]:
        """Get video information using yt-dlp"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info, None
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return None, str(e)
    
    def download_video(self, url: str, resolution: str = "720p", format: str = "mp4") -> Tuple[Optional[str], Optional[str]]:
        """Download video with specified resolution"""
        try:
            # Configure format based on resolution
            if resolution:
                format_spec = f'best[height<={resolution[:-1]}][ext={format}]/best[ext={format}]'
            else:
                format_spec = f'best[ext={format}]'
            
            download_opts = self.ydl_opts.copy()
            download_opts['format'] = format_spec
            
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if info:
                    # Find the downloaded file
                    for filename in os.listdir(self.download_folder):
                        if info['id'] in filename and filename.endswith(f'.{format}'):
                            file_path = os.path.join(self.download_folder, filename)
                            return file_path, None
                
                return None, "No video file found after download"
                
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            return None, str(e)
    
    def download_audio(self, url: str, bitrate: str = "128k") -> Tuple[Optional[str], Optional[str]]:
        """Download audio with specified bitrate"""
        try:
            # Configure audio format
            format_spec = f'bestaudio[abr<={bitrate[:-1]}][ext=mp3]/bestaudio[ext=mp3]/best[ext=mp3]'
            
            download_opts = self.ydl_opts.copy()
            download_opts['format'] = format_spec
            download_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate[:-1],
            }]
            
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if info:
                    # Find the downloaded audio file
                    for filename in os.listdir(self.download_folder):
                        if info['id'] in filename and filename.endswith('.mp3'):
                            file_path = os.path.join(self.download_folder, filename)
                            return file_path, None
                
                return None, "No audio file found after download"
                
        except Exception as e:
            logger.error(f"Error downloading audio: {e}")
            return None, str(e)
    
    def get_available_formats(self, url: str) -> Tuple[Optional[Dict], Optional[str]]:
        """Get available video and audio formats"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info and 'formats' in info:
                    formats = info['formats']
                    
                    # Extract video formats
                    video_formats = []
                    for fmt in formats:
                        if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
                            video_formats.append({
                                'format_id': fmt.get('format_id'),
                                'resolution': fmt.get('resolution'),
                                'filesize': fmt.get('filesize'),
                                'ext': fmt.get('ext'),
                                'fps': fmt.get('fps'),
                                'vcodec': fmt.get('vcodec'),
                                'acodec': fmt.get('acodec'),
                            })
                    
                    # Extract audio formats
                    audio_formats = []
                    for fmt in formats:
                        if fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
                            audio_formats.append({
                                'format_id': fmt.get('format_id'),
                                'abr': fmt.get('abr'),
                                'filesize': fmt.get('filesize'),
                                'ext': fmt.get('ext'),
                                'acodec': fmt.get('acodec'),
                            })
                    
                    return {
                        'video_formats': video_formats,
                        'audio_formats': audio_formats,
                        'title': info.get('title'),
                        'duration': info.get('duration'),
                        'uploader': info.get('uploader'),
                    }, None
                
                return None, "No formats found"
                
        except Exception as e:
            logger.error(f"Error getting available formats: {e}")
            return None, str(e)

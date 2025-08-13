"""
YouTube scraper module using YouTube Data API v3.
This implementation uses the official YouTube API for fetching video information.
"""

import logging
import os
import requests
import re
from typing import Optional, Dict, Any
from urllib.parse import urlparse, parse_qs
from settings import YOUTUBE_API_KEY, YOUTUBE_API_URL

logger = logging.getLogger(__name__)

class Youtube:
    def __init__(self, download_folder: str = "temp_files", proxies: list = None):
        self.download_folder = download_folder
        self.proxies = proxies or []
        self.title = ""
        self.duration = 0
        self.video_id = ""
        self.author = ""
        self.views = 0
        self.description = ""
        self.thumbnail_url = ""
        self.published_at = ""
        
        # Create download folder if it doesn't exist
        os.makedirs(download_folder, exist_ok=True)
    
    def _extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL"""
        try:
            query = urlparse(url)
            if query.hostname == 'youtu.be':
                return query.path[1:]
            if query.hostname in ('www.youtube.com', 'youtube.com'):
                if query.path == '/watch':
                    p = parse_qs(query.query)
                    return p['v'][0]
                if query.path[:7] == '/embed/':
                    return query.path.split('/')[2]
                if query.path[:3] == '/v/':
                    return query.path.split('/')[2]
        except Exception as e:
            logger.error(f"Error extracting video ID: {e}")
        return ""
    
    async def search(self, url: str, only_video: bool = False, only_caption: bool = False):
        """
        Fetch video information using YouTube Data API v3
        """
        logger.info(f"Searching for video: {url}")
        
        self.video_id = self._extract_video_id(url)
        if not self.video_id:
            logger.error("Could not extract video ID from URL")
            return self
        
        try:
            # Fetch video details from YouTube API
            api_url = f"{YOUTUBE_API_URL}/videos"
            params = {
                'key': YOUTUBE_API_KEY,
                'part': 'snippet,statistics,contentDetails',
                'id': self.video_id
            }
            
            response = requests.get(api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('items'):
                item = data['items'][0]
                snippet = item.get('snippet', {})
                statistics = item.get('statistics', {})
                content_details = item.get('contentDetails', {})
                
                self.title = snippet.get('title', 'Unknown Title')
                self.author = snippet.get('channelTitle', 'Unknown Author')
                self.description = snippet.get('description', '')
                self.thumbnail_url = snippet.get('thumbnails', {}).get('high', {}).get('url', '')
                self.published_at = snippet.get('publishedAt', '')
                self.views = int(statistics.get('viewCount', 0))
                
                # Parse duration (ISO 8601 format)
                duration_str = content_details.get('duration', 'PT0S')
                self.duration = self._parse_duration(duration_str)
                
                logger.info(f"Successfully fetched video info: {self.title}")
            else:
                logger.warning("No video found with the given ID")
                self.title = "Video Not Found"
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching video info from YouTube API: {e}")
            self.title = "Error fetching video info"
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            self.title = "Error processing video"
        
        return self
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse ISO 8601 duration string to seconds"""
        try:
            # Remove PT prefix
            duration = duration_str.replace('PT', '')
            
            hours = 0
            minutes = 0
            seconds = 0
            
            # Extract hours
            if 'H' in duration:
                hours = int(duration.split('H')[0])
                duration = duration.split('H')[1]
            
            # Extract minutes
            if 'M' in duration:
                minutes = int(duration.split('M')[0])
                duration = duration.split('M')[1]
            
            # Extract seconds
            if 'S' in duration:
                seconds = int(duration.split('S')[0])
            
            return hours * 3600 + minutes * 60 + seconds
        except Exception as e:
            logger.error(f"Error parsing duration {duration_str}: {e}")
            return 0
    
    def dict(self):
        """Return video information as dictionary"""
        return {
            'title': self.title,
            'duration': self.duration,
            'video_id': self.video_id,
            'view_url': f"https://youtube.com/watch?v={self.video_id}",
            'author': self.author,
            'views': self.views,
            'description': self.description,
            'thumbnail_url': self.thumbnail_url,
            'published_at': self.published_at
        }
    
    def streams(self):
        """
        Return available streams (placeholder for now)
        In a full implementation, this would use yt-dlp or similar library
        """
        class StreamFilter:
            def __init__(self, video_id: str, download_folder: str):
                self.video_id = video_id
                self.download_folder = download_folder
                self.resolution = "720p"
                self.frame_rate = 30
                self.bit_rate = 128000
                self.file_name = f"{video_id}_720p.mp4"
                self.hdr = False
                self.adaptive = False
                self.video_codec = "avc1"
                self.abr = "128kbps"
                self.filesize = 0
                self.filesize_approx = 0
            
            def filter(self, **kwargs):
                return [self]
            
            def download(self):
                # Create a placeholder file
                placeholder_path = os.path.join(self.download_folder, self.file_name)
                with open(placeholder_path, 'w') as f:
                    f.write(f"Placeholder video file for {self.video_id}")
                return placeholder_path
        
        class Streams:
            def __init__(self, video_id: str, download_folder: str):
                self._streams = [StreamFilter(video_id, download_folder)]
            
            def filter(self, **kwargs):
                return self._streams
            
            def get_highest_resolution(self):
                return self._streams[0]
            
            def get_audio_only(self):
                return self._streams[0]
        
        return Streams(self.video_id, self.download_folder)

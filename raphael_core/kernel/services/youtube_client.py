import os
import logging
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.readonly']

class YouTubeClient:
    def __init__(self, credentials_dir: str = r"C:\RaphaelOS\credentials"):
        self.credentials_dir = Path(credentials_dir)
        self.client_secrets_file = self.credentials_dir / "youtube_client_secrets.json"
        self.token_file = self.credentials_dir / "youtube_token.json"
        self.youtube = self.authenticate()

    def authenticate(self):
        creds = None
        if self.token_file.exists():
            creds = Credentials.from_authorized_user_file(str(self.token_file), SCOPES)
            
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Refreshing YouTube credentials...")
                creds.refresh(Request())
            else:
                if not self.client_secrets_file.exists():
                    raise FileNotFoundError(f"Missing client secrets at {self.client_secrets_file}")
                logger.info("Starting new YouTube OAuth flow...")
                flow = InstalledAppFlow.from_client_secrets_file(str(self.client_secrets_file), SCOPES)
                # This will print a URL to click
                creds = flow.run_local_server(port=0)
                
            with open(str(self.token_file), 'w') as token:
                token.write(creds.to_json())
                
        return build('youtube', 'v3', credentials=creds)

    def search_video(self, request_id: str) -> str:
        """
        Searches the authenticated user's channel for a video with the request_id in its description.
        Returns the video_id if found, None otherwise.
        """
        logger.info(f"Searching YouTube channel for existing upload with request_id: {request_id}")
        
        # Get the user's uploaded videos playlist
        channels_response = self.youtube.channels().list(
            mine=True,
            part='contentDetails'
        ).execute()
        
        if not channels_response.get('items'):
            return None
            
        uploads_list_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # Check recent 50
        playlistitems_list_request = self.youtube.playlistItems().list(
            playlistId=uploads_list_id,
            part='snippet',
            maxResults=50
        )
        
        playlistitems_list_response = playlistitems_list_request.execute()
        for playlist_item in playlistitems_list_response.get('items', []):
            description = playlist_item['snippet']['description']
            if request_id in description:
                logger.info(f"Found existing video on YouTube: {playlist_item['snippet']['resourceId']['videoId']}")
                return playlist_item['snippet']['resourceId']['videoId']
                
        return None

    def upload_video(self, video_path: str, title: str, description: str, privacy_status: str = "private") -> str:
        """
        Uploads a video to YouTube. Returns the Video ID.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['FocusMarketing', 'AI'],
                'categoryId': '22'  # People & Blogs
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }
        
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        
        request = self.youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        logger.info(f"Starting YouTube upload for {video_path}...")
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                logger.info(f"Uploaded {int(status.progress() * 100)}%")
                
        video_id = response.get('id')
        logger.info(f"Upload complete! Video ID: {video_id}")
        return video_id

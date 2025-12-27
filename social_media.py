"""
Social media posting modules for different platforms
"""
import tweepy
import requests
from atproto import Client as BlueskyClient
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import json
import os
import logging
from typing import Optional, Dict, Any

class TwitterPoster:
    def __init__(self, api_key: str, api_secret: str, access_token: str, access_token_secret: str):
        """Initialize Twitter API client"""
        try:
            # Twitter API v2 client
            self.client = tweepy.Client(
                bearer_token=None,
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                wait_on_rate_limit=True
            )
            # Verify credentials
            self.client.get_me()
            self.enabled = True
            logging.info("Twitter client initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize Twitter client: {e}")
            self.enabled = False
    
    def post(self, message: str) -> bool:
        """Post a tweet"""
        if not self.enabled:
            return False
        
        try:
            response = self.client.create_tweet(text=message)
            if hasattr(response, 'data') and response.data:
                logging.info(f"Successfully posted to Twitter: {response.data['id']}")
            else:
                logging.info("Successfully posted to Twitter")
            return True
        except Exception as e:
            error_msg = str(e)
            if "oauth1 app permissions" in error_msg.lower():
                logging.error("Twitter posting failed: App permissions are read-only")
                logging.error("Solution: Go to Twitter Developer Portal > Your App > Edit Permissions > Change to 'Read and Write' > Regenerate tokens")
            else:
                logging.error(f"Failed to post to Twitter: {e}")
            # Log additional details for debugging
            if hasattr(e, 'response'):
                logging.error(f"Twitter API response: {e.response}")
            return False

class BlueskyPoster:
    def __init__(self, handle: str, password: str):
        """Initialize Bluesky client"""
        try:
            self.client = BlueskyClient()
            # Use the correct login method
            session = self.client.login(handle, password)
            # Verify login was successful
            if session:
                self.enabled = True
                logging.info(f"Bluesky client initialized successfully for {handle}")
            else:
                self.enabled = False
                logging.error("Bluesky login failed - no session returned")
        except Exception as e:
            logging.error(f"Failed to initialize Bluesky client: {e}")
            logging.debug(f"Bluesky error details: {str(e)}")
            self.enabled = False
    
    def post(self, message: str) -> bool:
        """Post to Bluesky"""
        if not self.enabled:
            return False
        
        try:
            # Use the correct method for posting to Bluesky with the latest atproto library
            from atproto import models
            
            # Create the post record
            post = self.client.send_post(text=message)
            
            # Extract useful information from the response
            if hasattr(post, 'uri'):
                logging.info(f"Successfully posted to Bluesky: {post.uri}")
            elif hasattr(post, 'cid'):
                logging.info(f"Successfully posted to Bluesky: {post.cid}")
            else:
                logging.info("Successfully posted to Bluesky")
            
            return True
        except Exception as e:
            logging.error(f"Failed to post to Bluesky: {e}")
            # Log the full exception for debugging
            logging.debug(f"Bluesky error details: {str(e)}")
            
            # Try alternative method if the first fails
            try:
                # Fallback to manual post creation
                from atproto.models.app.bsky.feed.post import Post
                from datetime import datetime, timezone
                
                post_record = Post(
                    text=message,
                    createdAt=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
                )
                
                result = self.client.com.atproto.repo.create_record({
                    'repo': self.client.me.did,
                    'collection': 'app.bsky.feed.post',
                    'record': post_record.model_dump()
                })
                
                logging.info(f"Successfully posted to Bluesky (fallback): {result.uri}")
                return True
            except Exception as e2:
                logging.error(f"Bluesky fallback method also failed: {e2}")
                return False

class FacebookPoster:
    def __init__(self, page_access_token: str, page_id: str):
        """Initialize Facebook client"""
        self.access_token = page_access_token
        self.page_id = page_id
        self.base_url = f"https://graph.facebook.com/v19.0"
        
        # Verify token
        try:
            response = requests.get(
                f"{self.base_url}/me",
                params={"access_token": self.access_token}
            )
            if response.status_code == 200:
                self.enabled = True
                logging.info("Facebook client initialized successfully")
            else:
                self.enabled = False
                # Don't log the full response which might contain token info
                logging.error(f"Facebook token validation failed: Status {response.status_code}")
        except Exception as e:
            logging.error(f"Failed to initialize Facebook client: {e}")
            self.enabled = False
    
    def post(self, message: str) -> bool:
        """Post to Facebook page"""
        if not self.enabled:
            return False
        
        try:
            response = requests.post(
                f"{self.base_url}/{self.page_id}/feed",
                data={
                    "message": message,
                    "access_token": self.access_token
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                logging.info(f"Successfully posted to Facebook: {result.get('id')}")
                return True
            else:
                error_response = response.json() if response.content else {}
                logging.error(f"Failed to post to Facebook: Status {response.status_code}")
                logging.error(f"Facebook error response: {error_response}")
                return False
        except Exception as e:
            logging.error(f"Failed to post to Facebook: {e}")
            return False

class YouTubePoster:
    def __init__(self, client_id: str, client_secret: str, channel_id: str):
        """Initialize YouTube client"""
        self.client_id = client_id
        self.client_secret = client_secret
        self.channel_id = channel_id
        self.credentials = None
        self.service = None
        
        # OAuth 2.0 scopes
        self.scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']
        
        try:
            self._authenticate()
            self.enabled = True
            logging.info("YouTube client initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize YouTube client: {e}")
            self.enabled = False
    
    def _authenticate(self):
        """Authenticate with YouTube API"""
        creds_file = 'youtube_credentials.json'
        token_file = 'youtube_token.json'
        
        # Load existing credentials
        if os.path.exists(token_file):
            self.credentials = Credentials.from_authorized_user_file(token_file, self.scopes)
        
        # If there are no valid credentials available, let the user log in
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                # Create credentials file if it doesn't exist
                if not os.path.exists(creds_file):
                    creds_data = {
                        "installed": {
                            "client_id": self.client_id,
                            "client_secret": self.client_secret,
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "redirect_uris": ["http://localhost:8080/callback"]
                        }
                    }
                    with open(creds_file, 'w') as f:
                        json.dump(creds_data, f)
                
                flow = InstalledAppFlow.from_client_secrets_file(creds_file, self.scopes)
                self.credentials = flow.run_local_server(port=8080)
            
            # Save the credentials for the next run
            with open(token_file, 'w') as token:
                token.write(self.credentials.to_json())
        
        self.service = build('youtube', 'v3', credentials=self.credentials)
    
    def post(self, message: str) -> bool:
        """Post a community post to YouTube"""
        if not self.enabled:
            return False
        
        try:
            # Note: YouTube Community Posts API is limited
            # This creates a comment on the channel's latest video instead
            # For full community posts, you'd need YouTube Studio API access
            
            # Get channel's latest video
            search_response = self.service.search().list(
                part='snippet',
                channelId=self.channel_id,
                order='date',
                type='video',
                maxResults=1
            ).execute()
            
            if search_response['items']:
                video_id = search_response['items'][0]['id']['videoId']
                
                # Add comment to latest video
                comment_response = self.service.commentThreads().insert(
                    part='snippet',
                    body={
                        'snippet': {
                            'videoId': video_id,
                            'topLevelComment': {
                                'snippet': {
                                    'textOriginal': message
                                }
                            }
                        }
                    }
                ).execute()
                
                logging.info(f"Successfully posted YouTube comment: {comment_response['id']}")
                return True
            else:
                logging.warning("No videos found to comment on")
                return False
                
        except Exception as e:
            logging.error(f"Failed to post to YouTube: {e}")
            return False

class InstagramPoster:
    def __init__(self, access_token: str, user_id: str):
        """Initialize Instagram client"""
        self.access_token = access_token
        self.user_id = user_id
        self.base_url = "https://graph.facebook.com/v19.0"
        
        # Verify token
        try:
            response = requests.get(
                f"{self.base_url}/{self.user_id}",
                params={"access_token": self.access_token}
            )
            if response.status_code == 200:
                self.enabled = True
                logging.info("Instagram client initialized successfully")
            else:
                self.enabled = False
                # Don't log the full response which might contain token info
                logging.error(f"Instagram token validation failed: Status {response.status_code}")
        except Exception as e:
            logging.error(f"Failed to initialize Instagram client: {e}")
            self.enabled = False
    
    def post(self, message: str) -> bool:
        """Post to Instagram (creates a media object)"""
        if not self.enabled:
            return False
        
        try:
            # Note: Instagram Graph API requires media (image/video) for posts
            # Text-only posts are not supported - this will create a story instead
            # For proper posts, you need to provide an image URL
            
            # Create a story with text (alternative for text-only content)
            story_response = requests.post(
                f"{self.base_url}/{self.user_id}/media",
                data={
                    "media_type": "STORIES",
                    "caption": message,
                    "access_token": self.access_token
                }
            )
            
            if story_response.status_code == 200:
                media_id = story_response.json()["id"]
                
                # Publish the story
                publish_response = requests.post(
                    f"{self.base_url}/{self.user_id}/media_publish",
                    data={
                        "creation_id": media_id,
                        "access_token": self.access_token
                    }
                )
                
                if publish_response.status_code == 200:
                    result = publish_response.json()
                    logging.info(f"Successfully posted to Instagram story: {result.get('id')}")
                    return True
                else:
                    logging.error(f"Failed to publish Instagram story: Status {publish_response.status_code}")
                    logging.error(f"Response: {publish_response.text}")
                    return False
            else:
                logging.error(f"Failed to create Instagram story: Status {story_response.status_code}")
                logging.error(f"Response: {story_response.text}")
                return False
                
        except Exception as e:
            logging.error(f"Failed to post to Instagram: {e}")
            return False

class SocialMediaManager:
    def __init__(self, config):
        """Initialize all social media clients"""
        self.platforms = {}
        
        # Initialize Twitter
        if all([config.TWITTER_API_KEY, config.TWITTER_API_SECRET, 
                config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET]):
            self.platforms['twitter'] = TwitterPoster(
                config.TWITTER_API_KEY,
                config.TWITTER_API_SECRET,
                config.TWITTER_ACCESS_TOKEN,
                config.TWITTER_ACCESS_TOKEN_SECRET
            )
        
        # Initialize Bluesky
        if all([config.BLUESKY_HANDLE, config.BLUESKY_PASSWORD]):
            self.platforms['bluesky'] = BlueskyPoster(
                config.BLUESKY_HANDLE,
                config.BLUESKY_PASSWORD
            )
        
        # Initialize Facebook
        if all([config.FACEBOOK_PAGE_ACCESS_TOKEN, config.FACEBOOK_PAGE_ID]):
            self.platforms['facebook'] = FacebookPoster(
                config.FACEBOOK_PAGE_ACCESS_TOKEN,
                config.FACEBOOK_PAGE_ID
            )
        
        # Initialize YouTube
        if all([config.YOUTUBE_CLIENT_ID, config.YOUTUBE_CLIENT_SECRET, config.YOUTUBE_CHANNEL_ID]):
            self.platforms['youtube'] = YouTubePoster(
                config.YOUTUBE_CLIENT_ID,
                config.YOUTUBE_CLIENT_SECRET,
                config.YOUTUBE_CHANNEL_ID
            )
        
        # Initialize Instagram
        if all([config.INSTAGRAM_ACCESS_TOKEN, config.INSTAGRAM_USER_ID]):
            self.platforms['instagram'] = InstagramPoster(
                config.INSTAGRAM_ACCESS_TOKEN,
                config.INSTAGRAM_USER_ID
            )
        
        enabled_platforms = [name for name, client in self.platforms.items() if client.enabled]
        logging.info(f"Initialized social media platforms: {enabled_platforms}")
    
    def post_to_all(self, messages: Dict[str, str]) -> Dict[str, bool]:
        """Post to all enabled platforms"""
        results = {}
        
        for platform_name, client in self.platforms.items():
            if client.enabled and platform_name in messages:
                results[platform_name] = client.post(messages[platform_name])
            else:
                results[platform_name] = False
        
        return results
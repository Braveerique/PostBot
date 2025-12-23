"""
Configuration settings for the PostBot
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twitter API Configuration
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

# Bluesky Configuration
BLUESKY_HANDLE = os.getenv('BLUESKY_HANDLE')  # e.g., yourhandle.bsky.social
BLUESKY_PASSWORD = os.getenv('BLUESKY_PASSWORD')  # App password

# Facebook Configuration
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')

# YouTube Configuration
YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')
YOUTUBE_CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')

# Instagram Configuration
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
INSTAGRAM_USER_ID = os.getenv('INSTAGRAM_USER_ID')

# Streaming Platform Configuration
TWITCH_USERNAME = os.getenv('TWITCH_USERNAME')
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')

YOUTUBE_STREAM_KEY = os.getenv('YOUTUBE_STREAM_KEY')
OBS_WEBSOCKET_PASSWORD = os.getenv('OBS_WEBSOCKET_PASSWORD', '')
OBS_WEBSOCKET_PORT = int(os.getenv('OBS_WEBSOCKET_PORT', '4455'))

# General Configuration
STREAM_TITLE = os.getenv('STREAM_TITLE', 'Live Stream')
STREAM_GAME = os.getenv('STREAM_GAME', 'Just Chatting')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '30'))  # seconds

# Hashtag Configuration
MAX_HASHTAGS = int(os.getenv('MAX_HASHTAGS', '8'))
CUSTOM_HASHTAGS = os.getenv('CUSTOM_HASHTAGS', 'MysticsDen,IndieDev,Discord,Fun,Community').split(',')
AUTO_HASHTAGS = os.getenv('AUTO_HASHTAGS', 'true').lower() == 'true'

# Message Templates
TWITTER_MESSAGE_TEMPLATE = os.getenv('TWITTER_MESSAGE_TEMPLATE', 
    '🔴 LIVE NOW! {title}\n\nPlaying: {game}\n\nCome hang out! 👇\n{stream_url}')

BLUESKY_MESSAGE_TEMPLATE = os.getenv('BLUESKY_MESSAGE_TEMPLATE',
    '🔴 Going live! {title}\n\nCurrently playing: {game}\n\nJoin the stream: {stream_url}')

FACEBOOK_MESSAGE_TEMPLATE = os.getenv('FACEBOOK_MESSAGE_TEMPLATE',
    '🎮 Live streaming now!\n\n{title}\n\nGame: {game}\n\nWatch here: {stream_url}')

YOUTUBE_MESSAGE_TEMPLATE = os.getenv('YOUTUBE_MESSAGE_TEMPLATE',
    '🔴 LIVE: {title}\n\nNow playing: {game}\n\nJoin us live: {stream_url}')

INSTAGRAM_MESSAGE_TEMPLATE = os.getenv('INSTAGRAM_MESSAGE_TEMPLATE',
    '🔴 Going live now!\n\n{title}\n\nGame: {game}\n\nWatch at: {stream_url}\n\n#LiveStream #Gaming #Twitch')

# Stream URLs
TWITCH_STREAM_URL = f"https://twitch.tv/{TWITCH_USERNAME}" if TWITCH_USERNAME else ""
YOUTUBE_STREAM_URL = f"https://youtube.com/channel/{YOUTUBE_CHANNEL_ID}/live" if YOUTUBE_CHANNEL_ID else ""

def validate_config():
    """Validate that required configuration is present"""
    missing_configs = []
    
    # Check for at least one social platform
    social_platforms = [
        (TWITTER_API_KEY and TWITTER_API_SECRET, "Twitter"),
        (BLUESKY_HANDLE and BLUESKY_PASSWORD, "Bluesky"),
        (FACEBOOK_PAGE_ACCESS_TOKEN and FACEBOOK_PAGE_ID, "Facebook"),
        (YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET, "YouTube"),
        (INSTAGRAM_ACCESS_TOKEN and INSTAGRAM_USER_ID, "Instagram")
    ]
    
    if not any(config for config, _ in social_platforms):
        missing_configs.append("At least one social media platform configuration")
    
    # Check for streaming platform
    streaming_platforms = [
        (TWITCH_USERNAME and TWITCH_CLIENT_ID and TWITCH_CLIENT_SECRET, "Twitch"),
        (OBS_WEBSOCKET_PASSWORD, "OBS WebSocket")
    ]
    
    if not any(config for config, _ in streaming_platforms):
        missing_configs.append("At least one streaming platform configuration")
    
    return missing_configs
"""
Message template system for generating platform-specific posts
"""
import re
from typing import Dict, Any, Optional
from datetime import datetime

class MessageTemplateManager:
    def __init__(self, config):
        """Initialize message templates from config"""
        self.templates = {
            'twitter': config.TWITTER_MESSAGE_TEMPLATE,
            'bluesky': config.BLUESKY_MESSAGE_TEMPLATE,
            'facebook': config.FACEBOOK_MESSAGE_TEMPLATE,
            'youtube': config.YOUTUBE_MESSAGE_TEMPLATE,
            'instagram': config.INSTAGRAM_MESSAGE_TEMPLATE
        }
        
        self.stream_urls = {
            'twitch': config.TWITCH_STREAM_URL,
            'youtube': config.YOUTUBE_STREAM_URL
        }
        
        # Default values
        self.defaults = {
            'title': config.STREAM_TITLE,
            'game': config.STREAM_GAME,
            'streamer': config.TWITCH_USERNAME or 'Streamer'
        }
    
    def _format_template(self, template: str, stream_info: Dict[str, Any], 
                        platform: str = 'twitch') -> str:
        """Format a template with stream information"""
        
        # Prepare variables for template substitution
        variables = {
            'title': stream_info.get('title', self.defaults['title']),
            'game': stream_info.get('game', self.defaults['game']),
            'streamer': self.defaults['streamer'],
            'stream_url': self.stream_urls.get(platform, self.stream_urls.get('twitch', '')),
            'viewer_count': stream_info.get('viewer_count', 0),
            'time': datetime.now().strftime('%I:%M %p'),
            'date': datetime.now().strftime('%B %d, %Y'),
            'detection_method': stream_info.get('detection_method', 'unknown')
        }
        
        # Add platform-specific variables
        if platform == 'twitch':
            variables['platform'] = '🟣 Twitch'
            variables['platform_emoji'] = '🟣'
        elif platform == 'youtube':
            variables['platform'] = '🔴 YouTube'
            variables['platform_emoji'] = '🔴'
        elif platform == 'instagram':
            variables['platform'] = '📷 Instagram'
            variables['platform_emoji'] = '📷'
        else:
            variables['platform'] = 'Live Stream'
            variables['platform_emoji'] = '🔴'
        
        # Handle special cases for different detection methods
        if stream_info.get('detection_method') == 'obs':
            variables['title'] = f"Live Stream - {stream_info.get('scene', 'Main Scene')}"
        elif stream_info.get('detection_method') == 'process':
            variables['title'] = 'Live Stream'
            variables['game'] = 'Streaming Software Active'
        
        # Format the template
        try:
            formatted_message = template.format(**variables)
            return formatted_message
        except KeyError as e:
            # If a variable is missing, return a safe default message
            return f"🔴 Going live now!\n\n{variables['title']}\n\nCome watch: {variables['stream_url']}"
    
    def generate_messages(self, stream_info: Dict[str, Any], 
                         platforms: list = None) -> Dict[str, str]:
        """Generate platform-specific messages"""
        
        if platforms is None:
            platforms = list(self.templates.keys())
        
        messages = {}
        
        for platform in platforms:
            if platform in self.templates:
                messages[platform] = self._format_template(
                    self.templates[platform], 
                    stream_info, 
                    platform
                )
        
        return messages
    
    def add_hashtags(self, message: str, hashtags: list, max_length: int = 280) -> str:
        """Add hashtags to a message while respecting character limits"""
        
        hashtag_string = ' '.join([f'#{tag}' for tag in hashtags])
        
        # Check if we have space for hashtags
        available_space = max_length - len(message) - 2  # -2 for spacing
        
        if len(hashtag_string) <= available_space:
            return f"{message}\n\n{hashtag_string}"
        else:
            # Try to fit as many hashtags as possible
            fitted_hashtags = []
            current_length = len(message) + 2
            
            for hashtag in hashtags:
                tag_with_hash = f'#{hashtag}'
                if current_length + len(tag_with_hash) + 1 <= max_length:  # +1 for space
                    fitted_hashtags.append(tag_with_hash)
                    current_length += len(tag_with_hash) + 1
                else:
                    break
            
            if fitted_hashtags:
                return f"{message}\n\n{' '.join(fitted_hashtags)}"
            else:
                return message
    
    def customize_for_platform(self, message: str, platform: str) -> str:
        """Apply platform-specific customizations"""
        
        if platform == 'twitter':
            # Twitter character limit handling
            if len(message) > 280:
                # Truncate and add ellipsis
                message = message[:277] + '...'
        
        elif platform == 'facebook':
            # Facebook allows longer posts, can be more descriptive
            pass
        
        elif platform == 'youtube':
            # YouTube community posts have different formatting
            pass
        
        elif platform == 'bluesky':
            # Bluesky has a character limit similar to Twitter
            if len(message) > 300:
                message = message[:297] + '...'
        
        elif platform == 'instagram':
            # Instagram has a 2200 character limit for captions
            if len(message) > 2200:
                message = message[:2197] + '...'
        
        return message

# Default hashtag sets for different games/categories
DEFAULT_HASHTAGS = {
    'just chatting': ['JustChatting', 'Twitch', 'LiveStream', 'Streaming'],
    'minecraft': ['Minecraft', 'Gaming', 'LiveStream', 'Twitch'],
    'fortnite': ['Fortnite', 'Gaming', 'BattleRoyale', 'LiveStream'],
    'among us': ['AmongUs', 'Gaming', 'Twitch', 'LiveStream'],
    'valorant': ['Valorant', 'Gaming', 'FPS', 'LiveStream'],
    'league of legends': ['LeagueOfLegends', 'LoL', 'Gaming', 'LiveStream'],
    'default': ['LiveStream', 'Twitch', 'Gaming', 'Live']
}

def get_hashtags_for_game(game_name: str) -> list:
    """Get appropriate hashtags for a game"""
    game_lower = game_name.lower()
    
    for game_key, hashtags in DEFAULT_HASHTAGS.items():
        if game_key in game_lower:
            return hashtags
    
    return DEFAULT_HASHTAGS['default']
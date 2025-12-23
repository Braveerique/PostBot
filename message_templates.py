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
        
        # Hashtag configuration
        self.max_hashtags = getattr(config, 'MAX_HASHTAGS', 8)
        self.custom_hashtags = getattr(config, 'CUSTOM_HASHTAGS', ['MysticsDen', 'IndieDev', 'Discord', 'Fun', 'Community'])
        self.auto_hashtags = getattr(config, 'AUTO_HASHTAGS', True)
    
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
                message = self._format_template(
                    self.templates[platform], 
                    stream_info, 
                    platform
                )
                
                # Add automatic hashtags if enabled and no hashtags present
                if self.auto_hashtags and not self._has_hashtags(message):
                    message = self._add_smart_hashtags(message, stream_info, platform)
                
                messages[platform] = message
        
        return messages
    
    def _has_hashtags(self, message: str) -> bool:
        """Check if message already contains hashtags"""
        return '#' in message
    
    def _add_smart_hashtags(self, message: str, stream_info: Dict[str, Any], platform: str) -> str:
        """Add smart hashtags based on game and platform"""
        game_name = stream_info.get('game', self.defaults['game'])
        
        # Get game-specific hashtags
        game_hashtags = get_hashtags_for_game(game_name)
        
        # Combine with custom hashtags
        all_hashtags = combine_hashtags(game_hashtags, self.custom_hashtags, self.max_hashtags)
        
        # Add hashtags with platform-specific limits
        if platform == 'twitter':
            return self.add_hashtags(message, all_hashtags, max_length=280)
        elif platform == 'bluesky':
            return self.add_hashtags(message, all_hashtags, max_length=300)
        elif platform == 'instagram':
            return self.add_hashtags(message, all_hashtags, max_length=2200)
        else:
            return self.add_hashtags(message, all_hashtags, max_length=1000)
    
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

# Enhanced hashtag sets for different games/categories
DEFAULT_HASHTAGS = {
    'just chatting': ['JustChatting', 'Twitch', 'LiveStream', 'Streaming', 'MysticsDen'],
    'minecraft': ['Minecraft', 'Gaming', 'LiveStream', 'Twitch', 'Survival', 'Building'],
    'fortnite': ['Fortnite', 'Gaming', 'BattleRoyale', 'LiveStream', 'Epic'],
    'among us': ['AmongUs', 'Gaming', 'Twitch', 'LiveStream', 'Multiplayer'],
    'valorant': ['Valorant', 'Gaming', 'FPS', 'LiveStream', 'Riot'],
    'league of legends': ['LeagueOfLegends', 'LoL', 'Gaming', 'LiveStream', 'MOBA'],
    'apex legends': ['ApexLegends', 'Gaming', 'BattleRoyale', 'FPS', 'LiveStream'],
    'call of duty': ['CallOfDuty', 'COD', 'Gaming', 'FPS', 'LiveStream'],
    'counter-strike': ['CounterStrike', 'CS2', 'Gaming', 'FPS', 'Competitive'],
    'world of warcraft': ['WorldOfWarcraft', 'WoW', 'Gaming', 'MMO', 'LiveStream'],
    'overwatch': ['Overwatch', 'Gaming', 'FPS', 'Blizzard', 'LiveStream'],
    'rocket league': ['RocketLeague', 'Gaming', 'Sports', 'Cars', 'LiveStream'],
    'fall guys': ['FallGuys', 'Gaming', 'BattleRoyale', 'Fun', 'LiveStream'],
    'grand theft auto': ['GTA', 'Gaming', 'OpenWorld', 'LiveStream', 'Rockstar'],
    'sea of thieves': ['SeaOfThieves', 'Gaming', 'Pirates', 'Adventure', 'LiveStream'],
    'destiny': ['Destiny', 'Gaming', 'FPS', 'MMO', 'Bungie'],
    'dead by daylight': ['DeadByDaylight', 'Gaming', 'Horror', 'Multiplayer', 'LiveStream'],
    'the sims': ['TheSims', 'Gaming', 'Simulation', 'Building', 'LiveStream'],
    'animal crossing': ['AnimalCrossing', 'Gaming', 'Nintendo', 'Chill', 'LiveStream'],
    'pokemon': ['Pokemon', 'Gaming', 'Nintendo', 'Adventure', 'LiveStream'],
    'zelda': ['Zelda', 'Gaming', 'Nintendo', 'Adventure', 'BOTW'],
    'elder scrolls': ['ElderScrolls', 'Gaming', 'RPG', 'Skyrim', 'LiveStream'],
    'dark souls': ['DarkSouls', 'Gaming', 'RPG', 'Challenge', 'LiveStream'],
    'elden ring': ['EldenRing', 'Gaming', 'RPG', 'FromSoftware', 'LiveStream'],
    'terraria': ['Terraria', 'Gaming', 'Sandbox', 'Building', 'Adventure'],
    'stardew valley': ['StardewValley', 'Gaming', 'Farming', 'Indie', 'Chill'],
    'hollow knight': ['HollowKnight', 'Gaming', 'Indie', 'Metroidvania', 'Adventure'],
    'indie': ['IndieGames', 'Gaming', 'Indie', 'LiveStream', 'IndieDev'],
    'retro': ['RetroGaming', 'Gaming', 'Nostalgic', 'Classic', 'LiveStream'],
    'horror': ['HorrorGaming', 'Gaming', 'Scary', 'LiveStream', 'Spooky'],
    'puzzle': ['PuzzleGames', 'Gaming', 'Brain', 'Challenge', 'LiveStream'],
    'strategy': ['Strategy', 'Gaming', 'Tactical', 'RTS', 'LiveStream'],
    'racing': ['Racing', 'Gaming', 'Cars', 'Speed', 'LiveStream'],
    'sports': ['SportsGaming', 'Gaming', 'Sports', 'Competition', 'LiveStream'],
    'art': ['Art', 'Digital', 'Creative', 'Drawing', 'LiveStream'],
    'music': ['Music', 'LiveMusic', 'Performance', 'Creative', 'LiveStream'],
    'coding': ['Coding', 'Programming', 'Development', 'Tech', 'LiveStream'],
    'development': ['GameDev', 'IndieDev', 'Development', 'Coding', 'LiveStream'],
    'default': ['LiveStream', 'Twitch', 'Gaming', 'Live', 'MysticsDen']
}

def get_hashtags_for_game(game_name: str) -> list:
    """Get appropriate hashtags for a game with improved matching"""
    game_lower = game_name.lower()
    
    # Direct matches first
    for game_key, hashtags in DEFAULT_HASHTAGS.items():
        if game_key == game_lower:
            return hashtags
    
    # Partial matches
    for game_key, hashtags in DEFAULT_HASHTAGS.items():
        if game_key in game_lower or any(word in game_lower for word in game_key.split()):
            return hashtags
    
    # Keyword-based detection
    if any(word in game_lower for word in ['horror', 'scary', 'fear', 'dead']):
        return DEFAULT_HASHTAGS['horror']
    elif any(word in game_lower for word in ['indie', 'independent']):
        return DEFAULT_HASHTAGS['indie']
    elif any(word in game_lower for word in ['retro', 'classic', 'old']):
        return DEFAULT_HASHTAGS['retro']
    elif any(word in game_lower for word in ['puzzle', 'brain', 'logic']):
        return DEFAULT_HASHTAGS['puzzle']
    elif any(word in game_lower for word in ['strategy', 'rts', 'tactical']):
        return DEFAULT_HASHTAGS['strategy']
    elif any(word in game_lower for word in ['racing', 'car', 'driving']):
        return DEFAULT_HASHTAGS['racing']
    elif any(word in game_lower for word in ['sport', 'football', 'basketball', 'soccer']):
        return DEFAULT_HASHTAGS['sports']
    elif any(word in game_lower for word in ['art', 'draw', 'paint', 'design']):
        return DEFAULT_HASHTAGS['art']
    elif any(word in game_lower for word in ['music', 'song', 'audio']):
        return DEFAULT_HASHTAGS['music']
    elif any(word in game_lower for word in ['code', 'programming', 'development']):
        return DEFAULT_HASHTAGS['coding']
    
    return DEFAULT_HASHTAGS['default']

def get_custom_hashtags() -> list:
    """Get your custom MysticsDen hashtags"""
    return ['MysticsDen', 'IndieDev', 'Discord', 'Fun', 'Community']

def combine_hashtags(game_hashtags: list, custom_hashtags: list, max_tags: int = 8) -> list:
    """Combine game hashtags with custom hashtags, avoiding duplicates"""
    combined = []
    seen = set()
    
    # Add game hashtags first
    for tag in game_hashtags:
        if tag.lower() not in seen and len(combined) < max_tags:
            combined.append(tag)
            seen.add(tag.lower())
    
    # Add custom hashtags
    for tag in custom_hashtags:
        if tag.lower() not in seen and len(combined) < max_tags:
            combined.append(tag)
            seen.add(tag.lower())
    
    return combined
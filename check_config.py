#!/usr/bin/env python3
"""
Configuration diagnostic script - Check which platforms are properly configured
"""
import os
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Load environment variables
load_dotenv()

# Initialize colorama
init(autoreset=True)

def print_colored(message: str, color=Fore.WHITE):
    """Print colored message to console"""
    print(f"{color}{message}{Style.RESET_ALL}")

def check_platform_config(platform_name: str, required_vars: dict) -> bool:
    """Check if a platform has all required variables set"""
    missing = []
    placeholder = []
    
    for var_name, env_key in required_vars.items():
        value = os.getenv(env_key)
        if not value:
            missing.append(var_name)
        elif 'your_' in value.lower() or '_here' in value.lower():
            placeholder.append(var_name)
    
    if missing:
        print_colored(f"  ❌ {platform_name}: Missing variables: {', '.join(missing)}", Fore.RED)
        return False
    elif placeholder:
        print_colored(f"  ⚠️  {platform_name}: Using placeholder values: {', '.join(placeholder)}", Fore.YELLOW)
        return False
    else:
        print_colored(f"  ✅ {platform_name}: Properly configured", Fore.GREEN)
        return True

def main():
    """Main diagnostic function"""
    print_colored("🔧 PostBot Configuration Diagnostic", Fore.CYAN)
    print_colored("="*50, Fore.CYAN)
    
    platforms = {
        "Twitter": {
            "API Key": "TWITTER_API_KEY",
            "API Secret": "TWITTER_API_SECRET", 
            "Access Token": "TWITTER_ACCESS_TOKEN",
            "Access Token Secret": "TWITTER_ACCESS_TOKEN_SECRET"
        },
        "Bluesky": {
            "Handle": "BLUESKY_HANDLE",
            "Password": "BLUESKY_PASSWORD"
        },
        "Facebook": {
            "Page Access Token": "FACEBOOK_PAGE_ACCESS_TOKEN",
            "Page ID": "FACEBOOK_PAGE_ID"
        },
        "YouTube": {
            "Client ID": "YOUTUBE_CLIENT_ID",
            "Client Secret": "YOUTUBE_CLIENT_SECRET",
            "Channel ID": "YOUTUBE_CHANNEL_ID"
        },
        "Instagram": {
            "Access Token": "INSTAGRAM_ACCESS_TOKEN",
            "User ID": "INSTAGRAM_USER_ID"
        }
    }
    
    stream_platforms = {
        "Twitch": {
            "Username": "TWITCH_USERNAME",
            "Client ID": "TWITCH_CLIENT_ID",
            "Client Secret": "TWITCH_CLIENT_SECRET"
        },
        "OBS WebSocket": {
            "Password": "OBS_WEBSOCKET_PASSWORD"
        }
    }
    
    print_colored("\\n📱 Social Media Platform Configuration:", Fore.YELLOW)
    social_configured = 0
    for platform, vars in platforms.items():
        if check_platform_config(platform, vars):
            social_configured += 1
    
    print_colored("\\n🎥 Stream Detection Configuration:", Fore.YELLOW) 
    stream_configured = 0
    for platform, vars in stream_platforms.items():
        if check_platform_config(platform, vars):
            stream_configured += 1
    
    print_colored("\\n📊 Configuration Summary:", Fore.CYAN)
    print_colored(f"  📱 Social Platforms: {social_configured}/{len(platforms)} configured", 
                 Fore.GREEN if social_configured > 0 else Fore.RED)
    print_colored(f"  🎥 Stream Detection: {stream_configured}/{len(stream_platforms)} configured",
                 Fore.GREEN if stream_configured > 0 else Fore.RED)
    
    if social_configured == 0:
        print_colored("\\n⚠️  No social media platforms configured!", Fore.RED)
        print_colored("   Copy .env.example to .env and add your API credentials", Fore.YELLOW)
    
    if stream_configured == 0:
        print_colored("\\n⚠️  No stream detection methods configured!", Fore.RED)
        print_colored("   Configure either Twitch API or OBS WebSocket", Fore.YELLOW)
    
    print_colored("\\n💡 Configuration Tips:", Fore.CYAN)
    print_colored("   • Copy .env.example to .env", Fore.WHITE)
    print_colored("   • Replace placeholder values with real API credentials", Fore.WHITE)
    print_colored("   • Test with: python test_social_posting.py", Fore.WHITE)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Test script to verify social media posting functionality
"""
import logging
import sys
import os
from datetime import datetime
from colorama import init, Fore, Style

# Import our modules
import config
from social_media import SocialMediaManager

# Initialize colorama for colored console output
init(autoreset=True)

def setup_logging():
    """Setup logging for testing"""
    logging.basicConfig(
        level=logging.DEBUG,  # More verbose for testing
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(f'logs/test_social_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        ]
    )
    # Reduce noise from external libraries
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

def print_colored(message: str, color=Fore.WHITE):
    """Print colored message to console"""
    print(f"{color}{message}{Style.RESET_ALL}")

def test_platform_connections():
    """Test connections to all configured platforms"""
    print_colored("🧪 Testing Social Media Platform Connections", Fore.CYAN)
    print_colored("="*50, Fore.CYAN)
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    try:
        social_manager = SocialMediaManager(config)
        
        print_colored(f"\n📊 Platform Status:", Fore.YELLOW)
        for platform, client in social_manager.platforms.items():
            status = "✅ Connected" if client.enabled else "❌ Failed to connect"
            color = Fore.GREEN if client.enabled else Fore.RED
            print_colored(f"  {platform.title()}: {status}", color)
        
        return social_manager
    
    except Exception as e:
        print_colored(f"❌ Failed to initialize social manager: {e}", Fore.RED)
        logging.error(f"Social manager initialization failed: {e}")
        return None

def test_posting(social_manager):
    """Test posting to all platforms"""
    if not social_manager:
        print_colored("❌ Cannot test posting - social manager not initialized", Fore.RED)
        return
    
    print_colored(f"\n📤 Testing Post Functionality", Fore.CYAN)
    print_colored("="*50, Fore.CYAN)
    
    # Test message
    test_message = f"🧪 Test post from PostBot - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    print_colored(f"\n📝 Test Message: {test_message}", Fore.YELLOW)
    
    # Create test messages for each platform
    messages = {}
    for platform in social_manager.platforms.keys():
        messages[platform] = test_message
    
    # Add platform-specific modifications if needed
    if 'twitter' in messages:
        messages['twitter'] += " #TestPost"
    if 'bluesky' in messages:
        messages['bluesky'] += " #PostBot"
    
    # Post to all platforms
    results = social_manager.post_to_all(messages)
    
    # Report results
    print_colored(f"\n📊 Posting Results:", Fore.YELLOW)
    successful_posts = []
    failed_posts = []
    
    for platform, success in results.items():
        if success:
            successful_posts.append(platform)
            print_colored(f"  ✅ {platform.title()}: Posted successfully", Fore.GREEN)
        else:
            failed_posts.append(platform)
            print_colored(f"  ❌ {platform.title()}: Failed to post", Fore.RED)
    
    print_colored(f"\n📈 Summary:", Fore.CYAN)
    print_colored(f"  ✅ Successful: {len(successful_posts)} platforms", Fore.GREEN)
    print_colored(f"  ❌ Failed: {len(failed_posts)} platforms", Fore.RED)
    
    if failed_posts:
        print_colored(f"\n💡 Check the log file for detailed error information:", Fore.YELLOW)
        print_colored(f"  logs/test_social_{datetime.now().strftime('%Y%m%d')}*.log", Fore.YELLOW)

def main():
    """Main test function"""
    setup_logging()
    
    print_colored("🚀 PostBot Social Media Test Suite", Fore.CYAN)
    print_colored("This will test connections and posting to all configured platforms", Fore.WHITE)
    print_colored("="*60, Fore.CYAN)
    
    # Test connections
    social_manager = test_platform_connections()
    
    if social_manager:
        # Ask user if they want to test posting
        print_colored(f"\n❓ Do you want to test posting? This will create actual posts! (y/N): ", Fore.YELLOW, end="")
        response = input().strip().lower()
        
        if response in ['y', 'yes']:
            test_posting(social_manager)
        else:
            print_colored("📋 Skipping posting test", Fore.YELLOW)
    
    print_colored(f"\n✅ Test complete!", Fore.GREEN)

if __name__ == "__main__":
    main()
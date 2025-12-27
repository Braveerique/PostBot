#!/usr/bin/env python3
"""
Test Bluesky posting specifically
"""
import logging
import sys
import os
from datetime import datetime
from colorama import init, Fore, Style

# Import our modules
import config
from social_media import BlueskyPoster

# Initialize colorama
init(autoreset=True)

def setup_logging():
    """Setup detailed logging for debugging"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(f'logs/bluesky_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        ]
    )
    # Reduce noise from external libraries
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

def print_colored(message: str, color=Fore.WHITE):
    """Print colored message to console"""
    print(f"{color}{message}{Style.RESET_ALL}")

def test_bluesky():
    """Test Bluesky posting specifically"""
    setup_logging()
    
    print_colored("🦋 Testing Bluesky Posting", Fore.CYAN)
    print_colored("="*30, Fore.CYAN)
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    try:
        print_colored("📡 Initializing Bluesky client...", Fore.YELLOW)
        bluesky = BlueskyPoster(config.BLUESKY_HANDLE, config.BLUESKY_PASSWORD)
        
        if not bluesky.enabled:
            print_colored("❌ Bluesky client failed to initialize", Fore.RED)
            return
        
        print_colored("✅ Bluesky client initialized successfully", Fore.GREEN)
        
        # Test message
        test_message = f"🧪 Test post from PostBot - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        print_colored(f"📝 Test message: {test_message}", Fore.YELLOW)
        
        print_colored("📤 Attempting to post...", Fore.CYAN)
        success = bluesky.post(test_message)
        
        if success:
            print_colored("✅ Successfully posted to Bluesky!", Fore.GREEN)
        else:
            print_colored("❌ Failed to post to Bluesky", Fore.RED)
            print_colored("📋 Check the log file for detailed error information", Fore.YELLOW)
        
    except Exception as e:
        print_colored(f"❌ Error during Bluesky test: {e}", Fore.RED)
        logging.error(f"Test error: {e}")

if __name__ == "__main__":
    test_bluesky()
#!/usr/bin/env python3
"""
Test Bluesky posting specifically
"""
import logging
import sys
import os
from datetime import datetime

# Import our modules
import config
from social_media import BlueskyPoster

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

def test_bluesky():
    """Test Bluesky posting specifically"""
    setup_logging()
    
    print("Testing Bluesky Posting")
    print("=" * 30)
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    try:
        print("Initializing Bluesky client...")
        bluesky = BlueskyPoster(config.BLUESKY_HANDLE, config.BLUESKY_PASSWORD)
        
        if not bluesky.enabled:
            print("ERROR: Bluesky client failed to initialize")
            return
        
        print("SUCCESS: Bluesky client initialized")
        
        # Test message
        test_message = f"Test post from PostBot - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        print(f"Test message: {test_message}")
        
        print("Attempting to post...")
        success = bluesky.post(test_message)
        
        if success:
            print("SUCCESS: Posted to Bluesky!")
        else:
            print("ERROR: Failed to post to Bluesky")
        
    except Exception as e:
        print(f"ERROR: {e}")
        logging.error(f"Test error: {e}")

if __name__ == "__main__":
    test_bluesky()
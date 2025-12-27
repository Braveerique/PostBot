#!/usr/bin/env python3
"""
Test all social media platforms
"""
import logging
import sys
import os
from datetime import datetime

# Import our modules
import config
from social_media import SocialMediaManager

def setup_logging():
    """Setup basic logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    # Reduce noise from external libraries
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

def test_all_platforms():
    """Test all configured social media platforms"""
    setup_logging()
    
    print("Testing All Social Media Platforms")
    print("=" * 40)
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    try:
        print("Initializing social media manager...")
        social_manager = SocialMediaManager(config)
        
        print(f"\\nPlatform Status:")
        configured_count = 0
        for platform, client in social_manager.platforms.items():
            status = "ENABLED" if client.enabled else "DISABLED/ERROR"
            print(f"  {platform.upper()}: {status}")
            if client.enabled:
                configured_count += 1
        
        print(f"\\nConfigured platforms: {configured_count}/{len(social_manager.platforms)}")
        
        if configured_count == 0:
            print("ERROR: No platforms are properly configured!")
            return
        
        # Test posting only to enabled platforms
        test_message = f"Test post from PostBot - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        print(f"\\nTest message: {test_message}")
        
        # Create messages for each platform
        messages = {}
        for platform_name, client in social_manager.platforms.items():
            if client.enabled:
                messages[platform_name] = test_message
        
        if not messages:
            print("No enabled platforms to test!")
            return
        
        print(f"\\nTesting posting to {len(messages)} enabled platform(s)...")
        results = social_manager.post_to_all(messages)
        
        print("\\nPosting Results:")
        successful = 0
        for platform, success in results.items():
            if platform in messages:  # Only show results for enabled platforms
                status = "SUCCESS" if success else "FAILED"
                print(f"  {platform.upper()}: {status}")
                if success:
                    successful += 1
        
        print(f"\\nSummary: {successful}/{len(messages)} posts successful")
        
    except Exception as e:
        print(f"ERROR: {e}")
        logging.error(f"Test error: {e}")

if __name__ == "__main__":
    test_all_platforms()
"""
Test script for PostBot - Use this to test individual components
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from social_media import SocialMediaManager
from stream_detection import StreamDetectionManager
from message_templates import MessageTemplateManager
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_configuration():
    """Test if configuration is valid"""
    print("🧪 Testing Configuration...")
    
    missing = config.validate_config()
    if missing:
        print("❌ Configuration issues found:")
        for item in missing:
            print(f"   - {item}")
        return False
    else:
        print("✅ Configuration is valid!")
        return True

def test_social_media():
    """Test social media connections"""
    print("\n🧪 Testing Social Media Connections...")
    
    try:
        social_manager = SocialMediaManager(config)
        
        enabled_platforms = [name for name, client in social_manager.platforms.items() if client.enabled]
        disabled_platforms = [name for name, client in social_manager.platforms.items() if not client.enabled]
        
        print(f"✅ Enabled platforms: {', '.join(enabled_platforms) if enabled_platforms else 'None'}")
        if disabled_platforms:
            print(f"❌ Disabled platforms: {', '.join(disabled_platforms)}")
        
        return len(enabled_platforms) > 0
    
    except Exception as e:
        print(f"❌ Error testing social media: {e}")
        return False

def test_stream_detection():
    """Test stream detection methods"""
    print("\n🧪 Testing Stream Detection...")
    
    try:
        stream_detector = StreamDetectionManager(config)
        
        enabled_detectors = [name for name, detector in stream_detector.detectors.items() if detector.enabled]
        disabled_detectors = [name for name, detector in stream_detector.detectors.items() if not detector.enabled]
        
        print(f"✅ Enabled detectors: {', '.join(enabled_detectors) if enabled_detectors else 'None'}")
        if disabled_detectors:
            print(f"❌ Disabled detectors: {', '.join(disabled_detectors)}")
        
        # Test detection
        is_streaming, stream_info = stream_detector.check_stream_status()
        print(f"🔍 Current stream status: {'🔴 STREAMING' if is_streaming else '⚫ NOT STREAMING'}")
        
        if is_streaming and stream_info:
            print(f"   Title: {stream_info.get('title', 'N/A')}")
            print(f"   Game: {stream_info.get('game', 'N/A')}")
            print(f"   Method: {stream_info.get('detection_method', 'N/A')}")
        
        return len(enabled_detectors) > 0
    
    except Exception as e:
        print(f"❌ Error testing stream detection: {e}")
        return False

def test_message_templates():
    """Test message template generation"""
    print("\n🧪 Testing Message Templates...")
    
    try:
        message_manager = MessageTemplateManager(config)
        
        # Test with sample stream info
        sample_stream_info = {
            'title': 'Test Stream',
            'game': 'Just Chatting',
            'detection_method': 'test'
        }
        
        messages = message_manager.generate_messages(sample_stream_info)
        
        print("✅ Generated sample messages:")
        for platform, message in messages.items():
            print(f"\n📱 {platform.title()}:")
            print(f"   {message[:100]}{'...' if len(message) > 100 else ''}")
        
        return len(messages) > 0
    
    except Exception as e:
        print(f"❌ Error testing message templates: {e}")
        return False

def test_post_simulation():
    """Simulate posting without actually posting"""
    print("\n🧪 Testing Post Simulation...")
    
    try:
        # This would be where you test actual posting
        # For safety, we'll just simulate it
        print("✅ Post simulation completed (no actual posts made)")
        print("   To test actual posting, use 'python postbot.py test' with stream active")
        return True
    
    except Exception as e:
        print(f"❌ Error in post simulation: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 PostBot Test Suite")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Social Media", test_social_media),
        ("Stream Detection", test_stream_detection),
        ("Message Templates", test_message_templates),
        ("Post Simulation", test_post_simulation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🧪 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! PostBot is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the configuration and setup.")
        return 1

if __name__ == "__main__":
    exit(main())
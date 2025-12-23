"""
Main PostBot application - Automatically posts to social media when streaming starts
"""
import logging
import time
import schedule
from datetime import datetime
from typing import Dict, Any, Optional
import sys
import os
from colorama import init, Fore, Back, Style

# Import our modules
import config
from social_media import SocialMediaManager
from stream_detection import StreamDetectionManager
from message_templates import MessageTemplateManager, get_hashtags_for_game

# Initialize colorama for colored console output
init(autoreset=True)

class PostBot:
    def __init__(self):
        """Initialize the PostBot"""
        self.setup_logging()
        
        # Validate configuration
        missing_configs = config.validate_config()
        if missing_configs:
            logging.error("Missing required configuration:")
            for missing in missing_configs:
                logging.error(f"  - {missing}")
            self.print_colored("❌ Configuration validation failed. Please check your .env file.", Fore.RED)
            sys.exit(1)
        
        # Initialize components
        try:
            self.social_manager = SocialMediaManager(config)
            self.stream_detector = StreamDetectionManager(config)
            self.message_manager = MessageTemplateManager(config)
            
            self.last_notification_time = None
            self.cooldown_period = 300  # 5 minutes cooldown between notifications
            
            self.print_colored("✅ PostBot initialized successfully!", Fore.GREEN)
            self.print_status()
            
        except Exception as e:
            logging.error(f"Failed to initialize PostBot: {e}")
            self.print_colored(f"❌ Failed to initialize PostBot: {e}", Fore.RED)
            sys.exit(1)
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Setup file logging
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(f'logs/postbot_{datetime.now().strftime("%Y%m%d")}.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        # Reduce noise from external libraries
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    def print_colored(self, message: str, color=Fore.WHITE):
        """Print colored message to console"""
        print(f"{color}{message}{Style.RESET_ALL}")
    
    def print_status(self):
        """Print current bot status"""
        self.print_colored("\n" + "="*60, Fore.CYAN)
        self.print_colored("🤖 PostBot Status", Fore.CYAN)
        self.print_colored("="*60, Fore.CYAN)
        
        # Social Media Platforms
        self.print_colored("\n📱 Social Media Platforms:", Fore.YELLOW)
        for platform, client in self.social_manager.platforms.items():
            status = "✅ Enabled" if client.enabled else "❌ Disabled"
            color = Fore.GREEN if client.enabled else Fore.RED
            self.print_colored(f"  {platform.title()}: {status}", color)
        
        # Stream Detection Methods
        self.print_colored("\n🎥 Stream Detection Methods:", Fore.YELLOW)
        for method, detector in self.stream_detector.detectors.items():
            status = "✅ Enabled" if detector.enabled else "❌ Disabled"
            color = Fore.GREEN if detector.enabled else Fore.RED
            self.print_colored(f"  {method.title()}: {status}", color)
        
        self.print_colored(f"\n⏱️  Check Interval: {config.CHECK_INTERVAL} seconds", Fore.CYAN)
        self.print_colored("="*60 + "\n", Fore.CYAN)
    
    def check_and_notify(self):
        """Check stream status and notify if streaming started"""
        try:
            state_changed, is_streaming, stream_info = self.stream_detector.has_stream_state_changed()
            
            if state_changed:
                if is_streaming:
                    self.print_colored("🔴 Stream detected! Starting notifications...", Fore.GREEN)
                    self.handle_stream_start(stream_info)
                else:
                    self.print_colored("⚫ Stream ended.", Fore.YELLOW)
                    self.handle_stream_end()
        
        except Exception as e:
            logging.error(f"Error during stream check: {e}")
            self.print_colored(f"❌ Error checking stream status: {e}", Fore.RED)
    
    def handle_stream_start(self, stream_info: Dict[str, Any]):
        """Handle when a stream starts"""
        
        # Check cooldown
        current_time = datetime.now()
        if (self.last_notification_time and 
            (current_time - self.last_notification_time).seconds < self.cooldown_period):
            logging.info("Skipping notification due to cooldown period")
            return
        
        # Log stream information (without sensitive data)
        safe_stream_info = {k: v for k, v in stream_info.items() if k not in ['access_token', 'password', 'secret', 'key']}
        logging.info(f"Stream started: {safe_stream_info}")
        
        # Generate messages for all platforms
        messages = self.message_manager.generate_messages(stream_info)
        
        # Add hashtags based on game
        game_name = stream_info.get('game', 'Just Chatting')
        hashtags = get_hashtags_for_game(game_name)
        
        # Customize messages for each platform with hashtags
        for platform in messages:
            if platform == 'twitter':
                messages[platform] = self.message_manager.add_hashtags(
                    messages[platform], hashtags, max_length=280)
            elif platform == 'bluesky':
                messages[platform] = self.message_manager.add_hashtags(
                    messages[platform], hashtags, max_length=300)
        
        # Post to all platforms
        self.print_colored("📤 Posting notifications...", Fore.CYAN)
        results = self.social_manager.post_to_all(messages)
        
        # Report results
        successful_posts = []
        failed_posts = []
        
        for platform, success in results.items():
            if success:
                successful_posts.append(platform)
                self.print_colored(f"✅ {platform.title()}: Posted successfully", Fore.GREEN)
            else:
                failed_posts.append(platform)
                self.print_colored(f"❌ {platform.title()}: Failed to post", Fore.RED)
        
        # Log summary
        if successful_posts:
            logging.info(f"Successfully posted to: {', '.join(successful_posts)}")
        if failed_posts:
            logging.warning(f"Failed to post to: {', '.join(failed_posts)}")
        
        # Update last notification time
        self.last_notification_time = current_time
        
        # Display summary
        self.print_colored(f"\n📊 Notification Summary:", Fore.CYAN)
        self.print_colored(f"  ✅ Successful: {len(successful_posts)}", Fore.GREEN)
        self.print_colored(f"  ❌ Failed: {len(failed_posts)}", Fore.RED)
        self.print_colored(f"  📝 Game: {game_name}", Fore.YELLOW)
        self.print_colored(f"  🎯 Detection: {stream_info.get('detection_method', 'unknown')}", Fore.YELLOW)
    
    def handle_stream_end(self):
        """Handle when a stream ends"""
        logging.info("Stream ended")
        # You could implement end-of-stream notifications here if desired
    
    def run_once(self):
        """Run a single check (useful for testing)"""
        self.print_colored("🔍 Running single stream check...", Fore.CYAN)
        self.check_and_notify()
    
    def run_continuous(self):
        """Run the bot continuously"""
        self.print_colored("🚀 Starting PostBot continuous monitoring...", Fore.GREEN)
        self.print_colored("Press Ctrl+C to stop", Fore.YELLOW)
        
        # Schedule the check
        schedule.every(config.CHECK_INTERVAL).seconds.do(self.check_and_notify)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.print_colored("\n👋 PostBot stopped by user", Fore.YELLOW)
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")
            self.print_colored(f"❌ Unexpected error: {e}", Fore.RED)

def main():
    """Main entry point"""
    print(f"{Fore.CYAN}🤖 PostBot - Social Media Stream Notifier{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print(f"{Fore.RED}❌ No .env file found!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📝 Please copy .env.example to .env and configure your credentials{Style.RESET_ALL}")
        return
    
    try:
        bot = PostBot()
        
        # Check command line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] == 'test':
                bot.run_once()
            elif sys.argv[1] == 'status':
                bot.print_status()
            else:
                print(f"{Fore.RED}Unknown command: {sys.argv[1]}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Available commands: test, status{Style.RESET_ALL}")
        else:
            bot.run_continuous()
    
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to start PostBot: {e}{Style.RESET_ALL}")
        logging.error(f"Failed to start PostBot: {e}")

if __name__ == "__main__":
    main()
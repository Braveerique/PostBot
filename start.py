#!/usr/bin/env python3
"""
PostBot Launcher - Production-ready start script for cloud deployment
"""
import os
import sys
import logging
import signal
import time
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple health check endpoint for Railway"""
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "healthy", "service": "PostBot"}')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress HTTP server logs
        pass

def start_health_server():
    """Start health check server in background"""
    try:
        port = int(os.environ.get('PORT', 8080))
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        logging.info(f"Health check server starting on port {port}")
        server.serve_forever()
    except Exception as e:
        logging.warning(f"Could not start health server: {e}")

def setup_production_logging():
    """Set up logging for production environment"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/postbot.log', mode='a')
        ]
    )
    
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)

def signal_handler(signum, frame):
    """Handle graceful shutdown"""
    logging.info(f"Received signal {signum}, shutting down gracefully...")
    sys.exit(0)

def main():
    """Production entry point"""
    print(f"🤖 PostBot starting up at {datetime.now()}")
    print("=" * 50)
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Set up production logging
    setup_production_logging()
    
    # Start health check server in background thread
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    # Import and run the main bot
    try:
        from postbot import main as run_postbot
        logging.info("Starting PostBot in production mode")
        run_postbot()
    except Exception as e:
        logging.error(f"Failed to start PostBot: {e}")
        raise

if __name__ == "__main__":
    main()
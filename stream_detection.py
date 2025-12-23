"""
Stream detection modules for various platforms and methods
"""
import requests
import json
import logging
import psutil
import time
from typing import Optional, Dict, Any, List
import websocket
import threading

class TwitchStreamDetector:
    def __init__(self, client_id: str, client_secret: str, username: str):
        """Initialize Twitch API client for stream detection"""
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.access_token = None
        self.enabled = False
        
        try:
            self._get_access_token()
            self.enabled = True
            logging.info("Twitch stream detector initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize Twitch detector: {e}")
    
    def _get_access_token(self):
        """Get OAuth token from Twitch"""
        url = "https://id.twitch.tv/oauth2/token"
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        
        response = requests.post(url, data=data)
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
        else:
            raise Exception(f"Failed to get Twitch access token: {response.text}")
    
    def is_streaming(self) -> tuple[bool, Optional[Dict[str, Any]]]:
        """Check if the user is currently streaming on Twitch"""
        if not self.enabled:
            return False, None
        
        try:
            # Get user ID first
            user_url = "https://api.twitch.tv/helix/users"
            headers = {
                'Client-ID': self.client_id,
                'Authorization': f'Bearer {self.access_token}'
            }
            params = {'login': self.username}
            
            user_response = requests.get(user_url, headers=headers, params=params)
            if user_response.status_code != 200:
                logging.error(f"Failed to get Twitch user info: Status {user_response.status_code}")
                return False, None
            
            user_data = user_response.json()['data']
            if not user_data:
                logging.error(f"Twitch user {self.username} not found")
                return False, None
            
            user_id = user_data[0]['id']
            
            # Check stream status
            stream_url = "https://api.twitch.tv/helix/streams"
            params = {'user_id': user_id}
            
            stream_response = requests.get(stream_url, headers=headers, params=params)
            if stream_response.status_code == 200:
                streams = stream_response.json()['data']
                if streams:
                    stream_info = streams[0]
                    return True, {
                        'title': stream_info.get('title', 'Live Stream'),
                        'game': stream_info.get('game_name', 'Unknown'),
                        'viewer_count': stream_info.get('viewer_count', 0),
                        'started_at': stream_info.get('started_at')
                    }
                else:
                    return False, None
            else:
                logging.error(f"Failed to check Twitch stream status: Status {stream_response.status_code}")
                return False, None
                
        except Exception as e:
            logging.error(f"Error checking Twitch stream status: {e}")
            return False, None

class OBSWebSocketDetector:
    def __init__(self, password: str = "", port: int = 4455):
        """Initialize OBS WebSocket detector"""
        self.password = password
        self.port = port
        self.ws = None
        self.connected = False
        self.streaming = False
        self.stream_info = {}
        self.enabled = False
        
        try:
            self._connect()
            self.enabled = True
            logging.info("OBS WebSocket detector initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize OBS WebSocket detector: {e}")
    
    def _connect(self):
        """Connect to OBS WebSocket"""
        try:
            import obsws_python as obs
            self.obs = obs.ReqClient(host='localhost', port=self.port, password=self.password)
            self.connected = True
        except ImportError:
            logging.warning("obsws_python not installed. Install with: pip install obsws-python")
            self.enabled = False
        except Exception as e:
            logging.error(f"Failed to connect to OBS WebSocket: {e}")
            self.enabled = False
    
    def is_streaming(self) -> tuple[bool, Optional[Dict[str, Any]]]:
        """Check if OBS is currently streaming"""
        if not self.enabled or not self.connected:
            return False, None
        
        try:
            # Get streaming status
            status = self.obs.get_stream_status()
            is_active = status.output_active
            
            if is_active:
                # Get scene and source info
                current_scene = self.obs.get_current_program_scene()
                scene_name = current_scene.scene_name
                
                return True, {
                    'title': f'Live Stream - {scene_name}',
                    'game': 'Live Stream',
                    'scene': scene_name,
                    'output_duration': status.output_duration if hasattr(status, 'output_duration') else 0
                }
            else:
                return False, None
                
        except Exception as e:
            logging.error(f"Error checking OBS stream status: {e}")
            return False, None

class ProcessDetector:
    def __init__(self, process_names: List[str] = None):
        """Initialize process-based stream detection"""
        if process_names is None:
            # Common streaming software processes
            self.process_names = [
                'obs64.exe', 'obs32.exe', 'obs.exe',  # OBS Studio
                'XSplit.Core.exe',  # XSplit
                'streamlabs obs.exe',  # Streamlabs OBS
                'nvidia_share.exe',  # NVIDIA GeForce Experience
                'ffmpeg.exe'  # FFmpeg (often used for streaming)
            ]
        else:
            self.process_names = process_names
        
        self.enabled = True
        logging.info(f"Process detector initialized for: {', '.join(self.process_names)}")
    
    def is_streaming(self) -> tuple[bool, Optional[Dict[str, Any]]]:
        """Check if any streaming processes are running"""
        if not self.enabled:
            return False, None
        
        try:
            running_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    proc_name = proc.info['name'].lower()
                    for stream_proc in self.process_names:
                        if stream_proc.lower() in proc_name:
                            running_processes.append({
                                'name': proc.info['name'],
                                'pid': proc.info['pid'],
                                'cmdline': ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if running_processes:
                return True, {
                    'title': 'Live Stream Detected',
                    'game': 'Streaming Software Active',
                    'processes': running_processes
                }
            else:
                return False, None
                
        except Exception as e:
            logging.error(f"Error checking streaming processes: {e}")
            return False, None

class StreamDetectionManager:
    def __init__(self, config):
        """Initialize all stream detection methods"""
        self.detectors = {}
        self.last_stream_state = False
        self.current_stream_info = None
        
        # Initialize Twitch detector
        if all([config.TWITCH_USERNAME, config.TWITCH_CLIENT_ID, config.TWITCH_CLIENT_SECRET]):
            self.detectors['twitch'] = TwitchStreamDetector(
                config.TWITCH_CLIENT_ID,
                config.TWITCH_CLIENT_SECRET,
                config.TWITCH_USERNAME
            )
        
        # Initialize OBS WebSocket detector
        if config.OBS_WEBSOCKET_PASSWORD or config.OBS_WEBSOCKET_PORT:
            self.detectors['obs'] = OBSWebSocketDetector(
                config.OBS_WEBSOCKET_PASSWORD,
                config.OBS_WEBSOCKET_PORT
            )
        
        # Initialize process detector (always available)
        self.detectors['process'] = ProcessDetector()
        
        enabled_detectors = [name for name, detector in self.detectors.items() if detector.enabled]
        logging.info(f"Initialized stream detectors: {enabled_detectors}")
    
    def check_stream_status(self) -> tuple[bool, Optional[Dict[str, Any]]]:
        """Check if streaming across all detection methods"""
        stream_detected = False
        best_stream_info = None
        
        # Priority order: Twitch > OBS > Process
        detector_priority = ['twitch', 'obs', 'process']
        
        for detector_name in detector_priority:
            if detector_name in self.detectors and self.detectors[detector_name].enabled:
                is_streaming, stream_info = self.detectors[detector_name].is_streaming()
                
                if is_streaming:
                    stream_detected = True
                    best_stream_info = stream_info
                    best_stream_info['detection_method'] = detector_name
                    break  # Use the highest priority detection
        
        return stream_detected, best_stream_info
    
    def has_stream_state_changed(self) -> tuple[bool, bool, Optional[Dict[str, Any]]]:
        """
        Check if stream state has changed since last check
        Returns: (state_changed, is_streaming, stream_info)
        """
        current_streaming, current_info = self.check_stream_status()
        
        # Check if state changed
        state_changed = current_streaming != self.last_stream_state
        
        # Update state
        self.last_stream_state = current_streaming
        self.current_stream_info = current_info
        
        return state_changed, current_streaming, current_info
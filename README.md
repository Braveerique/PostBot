# PostBot - Social Media Stream Notifier

🤖 **PostBot** automatically posts to Twitter, Bluesky, Facebook, and YouTube when you start streaming - completely free!

## Features

- ✅ **Multi-Platform Support**: Twitter, Bluesky, Facebook, YouTube, Instagram
- ✅ **Multiple Detection Methods**: Twitch API, OBS WebSocket, Process Detection
- ✅ **Free APIs**: Uses free tiers of all social media platforms
- ✅ **Customizable Messages**: Platform-specific message templates
- ✅ **Smart Cooldown**: Prevents spam notifications
- ✅ **Real-time Monitoring**: Continuous background monitoring
- ✅ **Rich Logging**: Detailed logs and colored console output

## Quick Start

### 1. Install Dependencies

```bash
# Clone or download this repository
cd PostBot

# Install Python packages (already done if using the provided environment)
pip install tweepy atproto requests google-api-python-client google-auth-oauthlib google-auth-httplib2 psutil schedule python-dotenv colorama
```

### 2. Set Up Configuration

```bash
# Copy the example environment file
copy .env.example .env

# Edit .env with your credentials (see setup guides below)
notepad .env
```

### 3. Run the Bot

```bash
# Test configuration
python postbot.py status

# Run a single test
python postbot.py test

# Start continuous monitoring
python postbot.py
```

## Platform Setup Guides

### 🐦 Twitter Setup (Free)

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Apply for a developer account (free)
3. Create a new project/app
4. Generate API keys and tokens
5. Add to your `.env` file:

```env
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
```

### 🦋 Bluesky Setup (Free)

1. Create a Bluesky account at [bsky.app](https://bsky.app)
2. Go to Settings > App Passwords
3. Create a new app password
4. Add to your `.env` file:

```env
BLUESKY_HANDLE=yourhandle.bsky.social
BLUESKY_PASSWORD=your_app_password
```

### 📘 Facebook Setup (Free)

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add "Pages" product
4. Generate a Page Access Token
5. Get your Page ID from your Facebook page
6. Add to your `.env` file:

```env
FACEBOOK_PAGE_ACCESS_TOKEN=your_page_token
FACEBOOK_PAGE_ID=your_page_id
```

### 📷 Instagram Setup (Free)

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add "Instagram Basic Display" product
4. Set up Instagram Basic Display API
5. Generate User Access Token
6. Get your Instagram User ID
7. Add to your `.env` file:

```env
INSTAGRAM_ACCESS_TOKEN=your_access_token
INSTAGRAM_USER_ID=your_user_id
```

### 🔴 YouTube Setup (Free)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials
5. Add to your `.env` file:

```env
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_client_secret
YOUTUBE_CHANNEL_ID=your_channel_id
```

## Stream Detection Setup

### Method 1: Twitch API (Recommended)

1. Go to [Twitch Developers](https://dev.twitch.tv/)
2. Create a new application
3. Add to your `.env` file:

```env
TWITCH_USERNAME=your_twitch_username
TWITCH_CLIENT_ID=your_client_id
TWITCH_CLIENT_SECRET=your_client_secret
```

### Method 2: OBS WebSocket

1. In OBS Studio, go to Tools > WebSocket Server Settings
2. Enable WebSocket server
3. Set a password (optional)
4. Add to your `.env` file:

```env
OBS_WEBSOCKET_PASSWORD=your_password
OBS_WEBSOCKET_PORT=4455
```

### Method 3: Process Detection (Automatic)

No setup required! PostBot automatically detects common streaming software:
- OBS Studio
- XSplit
- Streamlabs OBS
- NVIDIA GeForce Experience
- FFmpeg

## Usage Examples

### Run Continuously
```bash
python postbot.py
```

### Test Configuration
```bash
python postbot.py status
```

### Single Test Run
```bash
python postbot.py test
```

## Configuration Options

Edit your `.env` file to customize:

```env
# Stream Information
STREAM_TITLE=My Awesome Stream
STREAM_GAME=Just Chatting
CHECK_INTERVAL=30

# Custom Message Templates
TWITTER_MESSAGE_TEMPLATE=🔴 LIVE NOW! {title}\n\nPlaying: {game}\n\nCome hang out! 👇\n{stream_url}
```

### Available Template Variables

- `{title}` - Stream title
- `{game}` - Game/category name
- `{streamer}` - Your username
- `{stream_url}` - Your stream URL
- `{viewer_count}` - Current viewer count (Twitch only)
- `{time}` - Current time
- `{date}` - Current date
- `{platform}` - Platform name with emoji
- `{platform_emoji}` - Just the platform emoji

## Troubleshooting

### Common Issues

1. **"No .env file found"**
   - Copy `.env.example` to `.env` and configure it

2. **"Configuration validation failed"**
   - Ensure at least one social platform and one detection method is configured
   - Check your API credentials are correct

3. **"Failed to initialize [Platform] client"**
   - Double-check your API credentials
   - Ensure you have the correct permissions/scopes

4. **Stream not detected**
   - Try different detection methods
   - Check if your streaming software is supported
   - Verify your Twitch username is correct

### Debug Mode

Add detailed logging by editing `postbot.py` and changing:
```python
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

1. Check the logs in the `logs/` folder
2. Run `python postbot.py status` to see what's configured
3. Test individual components with `python postbot.py test`

## Security Notes

- Never commit your `.env` file to version control
- Use app-specific passwords where available (Bluesky)
- Regularly rotate your API keys
- Use minimum required permissions for each platform

## Legal & Rate Limits

- **Twitter**: 300 tweets per 15 minutes (free tier)
- **Bluesky**: No official rate limits currently
- **Facebook**: Varies by app review status
- **YouTube**: 10,000 quota units per day (free tier)
- **Instagram**: 200 requests per hour (Basic Display API)

Always respect platform terms of service and rate limits.

## Advanced Features

### Custom Hashtags

Edit `message_templates.py` to customize hashtags for different games:

```python
DEFAULT_HASHTAGS = {
    'your_game': ['YourGame', 'Gaming', 'LiveStream', 'Twitch'],
}
```

### Multiple Stream URLs

Configure both Twitch and YouTube streaming:

```env
TWITCH_USERNAME=your_twitch_username
YOUTUBE_CHANNEL_ID=your_youtube_channel_id
```

### Cooldown Period

Prevent spam by adjusting the cooldown in `postbot.py`:

```python
self.cooldown_period = 300  # 5 minutes
```

## License

This project is open source. Feel free to modify and distribute.

---

**Happy Streaming! 🎮🔴**
# PostBot Quick Setup Guide

## Step 1: Configure Your Environment

1. Copy the example configuration:
   ```
   copy .env.example .env
   ```

2. Edit `.env` with your credentials (at minimum, set up one social platform and one detection method)

## Step 2: Get API Credentials (Free)

### Choose Your Social Platforms:

**Twitter (Easiest):**
- Go to: https://developer.twitter.com/
- Create free developer account
- Create new app, get API keys
- Add to `.env`: API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

**Bluesky (Simplest):**
- Go to: https://bsky.app/settings/app-passwords
- Create app password
- Add to `.env`: BLUESKY_HANDLE, BLUESKY_PASSWORD

**Facebook:**
- Go to: https://developers.facebook.com/
- Create app, add Pages product
- Get Page Access Token and Page ID
- Add to `.env`: FACEBOOK_PAGE_ACCESS_TOKEN, FACEBOOK_PAGE_ID

**Instagram:**
- Go to: https://developers.facebook.com/
- Add Instagram Basic Display product
- Generate User Access Token and get User ID
- Add to `.env`: INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_USER_ID

**YouTube:**
- Go to: https://console.cloud.google.com/
- Enable YouTube Data API v3
- Create OAuth credentials
- Add to `.env`: YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_CHANNEL_ID

### Choose Your Stream Detection:

**Twitch API (Recommended):**
- Go to: https://dev.twitch.tv/
- Create app, get Client ID/Secret
- Add to `.env`: TWITCH_USERNAME, TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET

**OBS WebSocket:**
- In OBS: Tools > WebSocket Server Settings
- Enable server, set password
- Add to `.env`: OBS_WEBSOCKET_PASSWORD

**Process Detection (Automatic):**
- No setup needed! Detects OBS, XSplit, etc.

## Step 3: Test and Run

```bash
# Test configuration
python test_postbot.py

# Run once to test
python postbot.py test

# Start monitoring
python postbot.py
```

Or use the provided scripts:
- Windows: `start_postbot.bat`
- Linux/Mac: `./start_postbot.sh`

## Minimal Setup Examples

### Example 1: Bluesky + Process Detection (5 minutes)
```env
BLUESKY_HANDLE=yourhandle.bsky.social
BLUESKY_PASSWORD=your_app_password
STREAM_TITLE=Live Stream
```

### Example 2: Twitter + Twitch (10 minutes)
```env
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_TOKEN_SECRET=your_token_secret
TWITCH_USERNAME=your_username
TWITCH_CLIENT_ID=your_client_id
TWITCH_CLIENT_SECRET=your_secret
```

## Need Help?

1. Run `python postbot.py status` to see what's configured
2. Run `python test_postbot.py` for detailed testing
3. Check `logs/` folder for error details
4. Make sure `.env` file exists and has correct format

**You only need ONE social platform and ONE detection method to start!**
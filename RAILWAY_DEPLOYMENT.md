# PostBot Railway Deployment Guide

## Quick Start

### 1. Prepare for GitHub

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

### 2. Deploy to Railway

1. **Go to [Railway.app](https://railway.app)**
2. **Sign in with GitHub**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your PostBot repository**
6. **Railway will automatically detect the Python app**

### 3. Configure Environment Variables

In your Railway dashboard, go to the **Variables** tab and add these environment variables:

#### Required Twitter/X API:
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET` 
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
- `TWITTER_BEARER_TOKEN`

#### Required Bluesky:
- `BLUESKY_HANDLE` (e.g., yourhandle.bsky.social)
- `BLUESKY_PASSWORD` (App password from Bluesky settings)

#### Optional Social Media:
- `FACEBOOK_PAGE_ACCESS_TOKEN`
- `FACEBOOK_PAGE_ID`
- `INSTAGRAM_ACCESS_TOKEN`
- `INSTAGRAM_USER_ID`
- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_CHANNEL_ID`

#### Stream Detection:
- `TWITCH_USERNAME`
- `TWITCH_CLIENT_ID`
- `TWITCH_CLIENT_SECRET`
- `OBS_WEBSOCKET_PASSWORD`
- `OBS_WEBSOCKET_PORT` (default: 4455)

#### Configuration:
- `STREAM_TITLE` (default: "Live Stream")
- `STREAM_GAME` (default: "Just Chatting")
- `CHECK_INTERVAL` (default: 30 seconds)

#### Message Templates (Optional):
- `TWITTER_MESSAGE_TEMPLATE`
- `BLUESKY_MESSAGE_TEMPLATE`
- `FACEBOOK_MESSAGE_TEMPLATE`
- `YOUTUBE_MESSAGE_TEMPLATE`

### 4. Deploy

1. **Railway will automatically build and deploy**
2. **Check the deployment logs for any issues**
3. **Your bot will start running automatically**

### 5. Monitor

- Check Railway logs to see if the bot is working correctly
- The bot will run continuously and check for streams every 30 seconds (or your configured interval)

## Features

- ✅ **Automatic stream detection** (Twitch API or OBS WebSocket)
- ✅ **Multi-platform posting** (Twitter/X, Bluesky, Facebook, Instagram, YouTube)
- ✅ **Smart hashtag addition** based on game being played
- ✅ **Cooldown periods** to prevent spam
- ✅ **Customizable message templates**
- ✅ **Robust error handling and logging**

## Commands

The bot supports these command-line arguments:
- `python postbot.py` - Run continuously (default)
- `python postbot.py test` - Run a single check
- `python postbot.py status` - Show current configuration

## Troubleshooting

1. **Check Railway logs** if the bot isn't working
2. **Verify all required environment variables** are set
3. **Test your API credentials** locally first
4. **Check that your Twitch username is correct**
5. **Ensure OBS WebSocket is enabled** if using OBS detection

## Cost

Railway offers:
- **$5/month** for the Pro plan (recommended for continuous running)
- **Free tier** available but may have limitations for 24/7 operation

## Security

- Never commit API keys or passwords to Git
- Use Railway's environment variables for all secrets
- The `.gitignore` file excludes all sensitive files
- Credentials are only stored in Railway's secure environment

## Support

Check the logs in Railway dashboard if you encounter issues. The bot includes comprehensive error handling and logging to help diagnose problems.
# Quick Fix Guide for Twitter Permissions

## Problem
Twitter posting fails with: `403 Forbidden - oauth1 app permissions`

## Solution
Your Twitter app currently has **Read-only** permissions. You need **Read and Write** permissions to post.

### Step 1: Go to Twitter Developer Portal
1. Visit: https://developer.twitter.com/en/portal/dashboard
2. Sign in with your Twitter account
3. Click on your PostBot app

### Step 2: Change App Permissions
1. In your app dashboard, find **App permissions** section
2. Click **Edit** next to "Read"  
3. Change from **"Read"** to **"Read and Write"**
4. Save changes

### Step 3: Regenerate Access Tokens
**IMPORTANT**: After changing permissions, you MUST regenerate tokens!

1. Go to **Keys and Tokens** tab
2. Under **Access Token and Secret**:
   - Click **Regenerate** 
   - Copy the new tokens

### Step 4: Update .env file
Replace these values in your `.env` file:
```
TWITTER_ACCESS_TOKEN=your_new_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_new_access_token_secret_here
```

### Step 5: Test
Run: `python test_all_platforms.py`

## Notes
- API Key and API Secret don't change
- Only Access Token and Access Token Secret need to be updated
- This is a one-time setup - permissions persist after this fix
# Logs directory - stores PostBot execution logs

This directory contains log files from PostBot runs:

- `postbot_YYYYMMDD.log` - Daily log files with detailed execution information
- Logs include stream detection events, social media posts, and error messages
- Log files are automatically created when PostBot runs
- Old log files can be safely deleted to save space

## Log Levels

- **INFO**: Normal operation events (stream detected, posts successful)
- **WARNING**: Non-critical issues (disabled platforms, cooldown skips)
- **ERROR**: Problems that prevent functionality (API failures, config issues)

## Privacy Note

Log files may contain:
- Stream titles and game names
- Posting success/failure status
- API response messages (no credentials are logged)

Ensure log files are kept secure and not shared publicly.
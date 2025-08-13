# Heroku Deployment Guide for YouTube-dl-api

## Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Make sure your project is in a Git repository

## Deployment Steps

### 1. Login to Heroku
```bash
heroku login
```

### 2. Create a new Heroku app
```bash
heroku create your-app-name
```

### 3. Set up environment variables
```bash
# Basic configuration
heroku config:set DEBUG=False
heroku config:set MAX_SIZE=2147483648
heroku config:set MAX_SEARCH=25
heroku config:set MIN_SEARCH_AMOUNT=2
heroku config:set DEFUALT_AMOUNT=20
heroku config:set EXPIRATION=1800
heroku config:set CODECS=avc1,aac

# Authentication (optional - set to False for basic deployment)
heroku config:set AUTH=False

# If you want to use authentication, set these:
# heroku config:set AUTH=True
# heroku config:set ACCESS_TOKEN=your_access_token
# heroku config:set REFRESH_TOKEN=your_refresh_token
# heroku config:set EXPIRES=your_expires
# heroku config:set VISITOR_DATA=your_visitor_data
# heroku config:set PO_TOKEN=your_po_token
```

### 4. Deploy to Heroku
```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

### 5. Open your app
```bash
heroku open
```

## About API Keys

**Your API key "AIzaSyDcJYgflcDs4vmrx8rlEjNdnwJQPds_978":**

This is now configured as your YouTube Data API v3 key. The application will use this to:

1. **Fetch video metadata** from YouTube Data API v3
2. **Download videos** using yt-dlp (which doesn't require API keys)
3. **Get video information** like title, duration, views, etc.

For production use, you should:
1. **Get your own API key** from [Google Cloud Console](https://console.cloud.google.com/)
2. **Set up proper quotas** and billing
3. **Keep your API key secure**

## Current Implementation Status

✅ **Fully Functional**: The deployment now includes:

- **Real YouTube API integration** using YouTube Data API v3
- **Actual video downloading** using yt-dlp
- **Video metadata fetching** (title, duration, views, etc.)
- **Audio downloading** with specified bitrates
- **Video downloading** with specified resolutions

The API will now:
1. **Fetch real video information** from YouTube
2. **Download actual videos** and audio files
3. **Provide real metadata** for videos

## Testing the Deployment

Once deployed, you can test these endpoints:

- `GET /ping` - Health check
- `GET /` - API documentation
- `GET /search?q=test` - Search videos
- `GET /info?url=https://youtube.com/watch?v=dQw4w9WgXcQ` - Get video info
- `POST /download` - Download video (real)
- `POST /download_audio` - Download audio (real)

### Example API Usage:

```bash
# Get video information
curl "https://your-app.herokuapp.com/info?url=https://youtube.com/watch?v=dQw4w9WgXcQ"

# Download video
curl -X POST "https://your-app.herokuapp.com/download" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/watch?v=dQw4w9WgXcQ"}'

# Download audio
curl -X POST "https://your-app.herokuapp.com/download_audio" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/watch?v=dQw4w9WgXcQ"}'
```

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `MAX_SIZE` | Max download size (bytes) | `2147483648` (2GB) |
| `MAX_SEARCH` | Max search results | `25` |
| `MIN_SEARCH_AMOUNT` | Min search results | `2` |
| `DEFUALT_AMOUNT` | Default search results | `20` |
| `EXPIRATION` | File expiration (seconds) | `1800` (30 min) |
| `CODECS` | Supported codecs | `avc1,aac` |
| `AUTH` | Enable authentication | `False` |

## Troubleshooting

### Common Issues:

1. **Build fails**: Check that all dependencies are in `requirements.txt`
2. **App crashes**: Check logs with `heroku logs --tail`
3. **Missing modules**: Ensure all Python files are committed to Git

### View Logs:
```bash
heroku logs --tail
```

### Restart App:
```bash
heroku restart
```

## Next Steps for Full Functionality

1. **Implement real YouTube scraping** using libraries like:
   - `yt-dlp`
   - `pytube`
   - `youtube-dl`

2. **Add FFmpeg support** for video processing

3. **Implement proper error handling** and rate limiting

4. **Add authentication** if needed

## Support

For issues with the deployment, check:
- Heroku logs: `heroku logs --tail`
- Application status: `heroku ps`
- Environment variables: `heroku config`

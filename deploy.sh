#!/bin/bash

echo "🚀 YouTube-dl-api Heroku Deployment Script"
echo "=========================================="

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed. Please install it first:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please login to Heroku first:"
    heroku login
fi

# Get app name from user
echo ""
read -p "Enter your Heroku app name (or press Enter to create a new one): " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "Creating new Heroku app..."
    APP_NAME=$(heroku create --json | grep -o '"name":"[^"]*"' | cut -d'"' -f4)
    echo "✅ Created app: $APP_NAME"
else
    echo "Using existing app: $APP_NAME"
fi

# Set environment variables
echo ""
echo "🔧 Setting up environment variables..."

heroku config:set DEBUG=False --app $APP_NAME
heroku config:set MAX_SIZE=2147483648 --app $APP_NAME
heroku config:set MAX_SEARCH=25 --app $APP_NAME
heroku config:set MIN_SEARCH_AMOUNT=2 --app $APP_NAME
heroku config:set DEFUALT_AMOUNT=20 --app $APP_NAME
heroku config:set EXPIRATION=1800 --app $APP_NAME
heroku config:set CODECS=avc1,aac --app $APP_NAME
heroku config:set AUTH=False --app $APP_NAME
heroku config:set YOUTUBE_API_KEY=AIzaSyDcJYgflcDs4vmrx8rlEjNdnwJQPds_978 --app $APP_NAME
heroku config:set YOUTUBE_API_URL=https://www.googleapis.com/youtube/v3 --app $APP_NAME

echo "✅ Environment variables configured"

# Deploy to Heroku
echo ""
echo "📦 Deploying to Heroku..."

# Add all files to git
git add .

# Commit changes
git commit -m "Deploy to Heroku - $(date)"

# Push to Heroku
git push heroku main

# Check if deployment was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment successful!"
    echo ""
    echo "🌐 Your app is available at: https://$APP_NAME.herokuapp.com"
    echo ""
    echo "📋 Quick test commands:"
    echo "   curl https://$APP_NAME.herokuapp.com/ping"
    echo "   curl https://$APP_NAME.herokuapp.com/"
    echo ""
    echo "📊 View logs: heroku logs --tail --app $APP_NAME"
    echo "🔧 Open app: heroku open --app $APP_NAME"
else
    echo "❌ Deployment failed. Check the logs above for errors."
    exit 1
fi

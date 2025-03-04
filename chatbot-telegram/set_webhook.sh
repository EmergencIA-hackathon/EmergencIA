#!/bin/bash

BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
NGROK_URL="https://${NGROK_HOSTNAME}"

WEBHOOK_URL="${NGROK_URL}/webhook"

curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" -d "url=${WEBHOOK_URL}"

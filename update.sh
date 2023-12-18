#!/bin/bash

REPO_URL="https://github.com/Anonyyymous/DiscordBotTest.git"
LOCAL_DIR="/home/oreo/Desktop/DiscordBot/DiscordBotTest"

cd "$LOCAL_DIR"

git pull

python3 "$LOCAL_DIR/Main.py"
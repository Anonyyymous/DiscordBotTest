#!/bin/bash

REPO_URL="https://github.com/Anonyyymous/DiscordBotTest.git"
LOCAL_DIR="/home/oreo/Desktop/DiscordBot/DiscordBotTest"

cd "$LOCAL_DIR"

while :
do
    git add NamesCount.txt
    gid commit
    git push
    git pull
    python3 "$LOCAL_DIR/Main.py"
    sleep 1s
done
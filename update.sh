#!/bin/bash

echo "Update started"
git pull
docker-compose up --build -d
echo "Update finished"
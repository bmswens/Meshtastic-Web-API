#!/bin/bash
docker run \
    -p 5000:5000 \
    --privileged \
    -v ./data:/app/data \
    bmswens/meshtastic-web-api
#!/bin/bash

# Check if the container "redis-hypo" exists
if [ "$(docker ps -a -q -f name=redis-hypo)" ]; then
    echo "Container 'redis-hypo' already exists. No action taken."
else
    echo "Container 'redis-hypo' does not exist. Creating a new container on port 6380..."
    docker run -d --name redis-hypo -p 6380:6379 redis
    if [ $? -eq 0 ]; then
        echo "Container 'redis-hypo' created successfully and is running on port 6380."
    else
        echo "Failed to create the container 'redis-hypo'."
        exit 1
    fi
fi

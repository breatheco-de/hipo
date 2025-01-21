#!/bin/bash

# Default port
HOST_PORT=""

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --port) HOST_PORT="$2"; shift ;; # Set the port from the flag
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# If no port is provided, ask the user
if [ -z "$HOST_PORT" ]; then
    read -p "No port specified. Please enter a port for the container on the host: " HOST_PORT
fi

# Validate that the port is a number
if ! [[ "$HOST_PORT" =~ ^[0-9]+$ ]]; then
    echo "Error: Port must be a valid number."
    exit 1
fi

# Check if the container "redis-hypo" exists
if [ "$(docker ps -a -q -f name=redis-hypo)" ]; then
    echo "Container 'redis-hypo' already exists. No action taken."
else
    echo "Container 'redis-hypo' does not exist. Creating a new container on port $HOST_PORT..."
    docker run -d --name redis-hypo -p $HOST_PORT:6379 redis
    if [ $? -eq 0 ]; then
        echo "Container 'redis-hypo' created successfully and is running on port $HOST_PORT."
    else
        echo "Failed to create the container 'redis-hypo'."
        exit 1
    fi
fi

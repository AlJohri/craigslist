#!/bin/sh

if [ -d "envs/local" ]; then
    echo "sourcing envs/local directory..."
    for f in envs/local/*; do eval $(echo export $(basename $f)=$(cat $f)); done
elif [ -f ".env" ]; then
    echo "sourcing .env file..."
    export $(cat .env | grep -v "^#" | xargs)
fi
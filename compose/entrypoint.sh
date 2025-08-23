#!/bin/bash


echo "Starting FastAPI application.."

# exec printenv
if [ $DEBUG="true" ]; then 
    uvicorn config.app:app --host "${HOST:-0.0.0.0}" --port "${APP_PORT:-8080}" --reload;
    echo "Successfully started development server";
else    
    gunicorn -c config/gunicorn.conf.py config.app:app;
    echo "Successfully started production server";
fi
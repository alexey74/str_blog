#!/bin/sh

until cd /app/; do
	echo "Waiting for server volume..."
done

# run a beat
celery -A config flower --loglevel=info

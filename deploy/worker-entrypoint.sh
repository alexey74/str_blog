#!/bin/sh

until cd /app/; do
	echo "Waiting for server volume..."
done

# run a worker
exec celery -A config worker --loglevel=info -E

#!/bin/sh

until cd /app/; do
	echo "Waiting for server volume..."
done

# run a beat
exec celery -A config beat --loglevel=info \
	--scheduler django_celery_beat.schedulers:DatabaseScheduler \
	--max-interval 120 \
	-s /celerybeat-schedule/schedule

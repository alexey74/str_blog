# Generated by Django 4.2.10 on 2024-02-29 16:12
# type: ignore

from django.db import migrations


def forwards(apps, schema_editor):
    """
    A migration that adds a periodic task
    for full push to JSON Placeholder API.
    """
    if schema_editor.connection.alias != "default":
        return
    IntervalSchedule = apps.get_model("django_celery_beat", "IntervalSchedule")
    PeriodicTask = apps.get_model("django_celery_beat", "PeriodicTask")
    schedule, _created = IntervalSchedule.objects.get_or_create(
        every=10,
        period="minutes",
    )
    PeriodicTask.objects.get_or_create(
        interval=schedule,  # we created this above.
        name="Full push to JSON Placeholder API",  # simply describes this periodic task.
        task="blog.tasks.push_to_jsonplaceholder",  # name of task.
    )


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_synclog"),
        ("django_celery_beat", "0018_improve_crontab_helptext"),
    ]

    operations = [
        migrations.RunPython(forwards, reverse_code=migrations.RunPython.noop),
    ]
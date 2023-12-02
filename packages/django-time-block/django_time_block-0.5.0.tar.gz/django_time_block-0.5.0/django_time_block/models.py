"""
models
"""

from django.db import models

# Create your models here.


class TimeBlock(models.Model):
    """
    a time block contains a duration [start_datetime: end_datetime) (not include the end_datetime)
    """
    object_id = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["object_id", "start_datetime"]),
            models.Index(fields=["object_id", "end_datetime"]),
        ]


class RelationTimeBlock(models.Model):
    """
    a time block with should be used in a model
    e.g.
        class Worker(models.Model):
            work_durations = models.ManyToManyField(RelationTimeBlock)
    """
    start_datetime = models.DateTimeField(db_index=True)
    end_datetime = models.DateTimeField(db_index=True)
    update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        pass

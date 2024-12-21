from django.db import models

class Meeting(models.Model):
    meeting_id = models.CharField(max_length=100, unique=True)
    transcription_text = models.TextField()
    recording_url = models.URLField()
    s3_key = models.CharField(max_length=255)

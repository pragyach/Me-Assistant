from django.test import TestCase
from unittest.mock import patch, MagicMock
from .models import Meeting
from . import zoom_recording_to_text_and_upload, upload_to_s3, transcribe_audio, get_zoom_recordings

from django.test import TestCase
from unittest.mock import patch, MagicMock
from apps.models import Meeting  # Add the missing import statement
from . import zoom_recording_to_text_and_upload, upload_to_s3, transcribe_audio, get_zoom_recordings

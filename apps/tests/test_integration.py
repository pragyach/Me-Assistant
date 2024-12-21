# test_integration.py
from unittest.mock import patch
from unittest import TestCase
from apps.zoom import zoom_recording_to_text_and_upload
from apps.models import Meeting

class ZoomIntegrationTestCase(TestCase):

    @patch(".get_zoom_recordings")
    @patch(".transcribe_audio")
    @patch(".upload_to_s3")
    def test_zoom_recording_to_text_and_upload(self, mock_upload_to_s3, mock_transcribe_audio, mock_get_zoom_recordings):
        # Mock Zoom API Response
        mock_get_zoom_recordings.return_value = [
            {"download_url": "https://zoom.us/recording1.mp4", "id": "recording1"},
            {"download_url": "https://zoom.us/recording2.mp4", "id": "recording2"},
        ]

        # Mock Transcription
        mock_transcribe_audio.side_effect = ["Transcription 1", "Transcription 2"]

        # Mock S3 Upload
        mock_upload_to_s3.side_effect = [
            "https://s3.amazonaws.com/your-bucket/recordings/recording1.mp4",
            "https://s3.amazonaws.com/your-bucket/recordings/recording2.mp4",
        ]

        # Call the function
        access_token = "test-access-token"
        meeting_id = "test-meeting-id"
        results = zoom_recording_to_text_and_upload(meeting_id, access_token)

        # Verify results
        self.assertEqual(len(results), 2)

        self.assertEqual(results[0]["transcription"], "Transcription 1")
        self.assertEqual(results[1]["transcription"], "Transcription 2")

        self.assertEqual(
            results[0]["s3_url"], "https://s3.amazonaws.com/your-bucket/recordings/recording1.mp4"
        )
        self.assertEqual(
            results[1]["s3_url"], "https://s3.amazonaws.com/your-bucket/recordings/recording2.mp4"
        )

        # Verify RDS entries
        meeting_records = Meeting.objects.filter(meeting_id=meeting_id)
        self.assertEqual(meeting_records.count(), 1)
        self.assertEqual(meeting_records.first().transcription_text, "Transcription 1")
from unittest.mock import patch
from unittest import TestCase
from apps.zoom import get_zoom_recordings
from apps.zoom import zoom_recording_to_text_and_upload




class ZoomAPITestCase(TestCase):

    @patch(".get_zoom_recordings")
    def test_zoom_recordings_error_handling(self, mock_get_zoom_recordings):
        # Mock Error Response from Zoom API
        mock_get_zoom_recordings.return_value = {"error": "Invalid meeting ID"}

        access_token = "test-access-token"
        meeting_id = "invalid-meeting-id"
        results = zoom_recording_to_text_and_upload(meeting_id, access_token)

        self.assertIn("error", results)
        self.assertEqual(results["error"], "Invalid meeting ID")
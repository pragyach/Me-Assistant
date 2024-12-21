from unittest.mock import patch
from unittest import TestCase
from unittest.mock import MagicMock
from apps import upload_to_s3
from apps.utils import transcribe_audio

# test_aws_integration.py
class AWSIntegrationTestCase(TestCase):

    @patch(".requests.get")
    def test_upload_to_s3(self, mock_requests_get):
        # Mock requests.get for file download
        mock_response = MagicMock()
        mock_response.raw = b"test data"
        mock_requests_get.return_value = mock_response

        file_url = "https://zoom.us/recording.mp4"
        file_key = "recordings/test-recording.mp4"
        s3_url = upload_to_s3(file_url, file_key)

        self.assertEqual(
            s3_url, "https://s3.amazonaws.com/your-bucket/recordings/test-recording.mp4"
        )

    @patch(".boto3.client")
    def test_transcribe_audio(self, mock_boto3_client):
        # Mock AWS Transcribe Client
        mock_client = MagicMock()
        mock_boto3_client.return_value = mock_client

        mock_client.get_transcription_job.side_effect = [
            {"TranscriptionJob": {"TranscriptionJobStatus": "IN_PROGRESS"}},
            {
                "TranscriptionJob": {
                    "TranscriptionJobStatus": "COMPLETED",
                    "Transcript": {"TranscriptFileUri": "https://transcribe.amazonaws.com/test-transcript.json"},
                }
            },
        ]

        mock_response = MagicMock()
        mock_response.text = "Test transcription text"
        with patch(".requests.get", return_value=mock_response):
            transcription = transcribe_audio("https://zoom.us/recording.mp4", "test-job")
            self.assertEqual(transcription, "Test transcription text")
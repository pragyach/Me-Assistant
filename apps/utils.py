import requests
import boto3

def transcribe_audio(audio_url, job_name):
    """
    Transcribe audio using AWS Transcribe.

    Args:
        audio_url (str): URL of the audio file to transcribe.
        job_name (str): Unique job name for AWS Transcribe.

    Returns:
        str: Transcription text or an error message.
    """
    transcribe = boto3.client("transcribe")
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": audio_url},
        MediaFormat="mp4",
        LanguageCode="en-US",
    )
    while response["TranscriptionJob"]["TranscriptionJobStatus"] == "IN_PROGRESS":
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if response["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        transcript_url = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        transcript_response = requests.get(transcript_url)
        return transcript_response.text
    return "Transcription failed"

def upload_to_s3(file_url, file_key):
    """
    Upload file to AWS S3.

    Args:
        file_url (str): URL of the file to upload.
        file_key (str): Key for the file in the S3 bucket.

    Returns:
        str: S3 URL of the uploaded file.
    """
    s3 = boto3.client("s3")
    bucket = "your-s3-bucket-name"
    response = requests.get(file_url, stream=True)
    s3.upload_fileobj(response.raw, bucket, file_key)
    return f"https://{bucket}.s3.amazonaws.com/{file_key}"

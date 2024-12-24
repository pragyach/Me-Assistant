from celery import shared_task
from .utils import get_zoom_recordings, transcribe_audio, upload_to_s3
from .models import Meeting
from apps.utils import process_transcription_to_databricks
from apps.zoom import get_zoom_recordings
from apps.gmeet import get_gmeet_recordings
from apps.teams import get_teams_recordings
from apps.utils import transcribe_audio, upload_to_s3

DELTA_TABLE_PATH = "s3://your-bucket-name/meetings/"

@shared_task
def process_recordings(platform, meeting_id, access_token):
    # Fetch recordings based on the platform
    if platform == "Zoom":
        recordings = get_zoom_recordings(meeting_id, access_token)
    elif platform == "GMeet":
        recordings = get_gmeet_recordings(meeting_id, access_token)
    elif platform == "Teams":
        recordings = get_teams_recordings(meeting_id, access_token)
    else:
        raise ValueError("Unsupported platform")

    for recording in recordings:
        try:
            audio_url = recording["download_url"]
            job_name = f"{platform}-transcription-{recording['id']}"

            # Transcribe the audio
            transcription = transcribe_audio(audio_url, job_name)

            # Upload the file to S3
            s3_key = f"recordings/{platform}/{recording['id']}.mp4"
            s3_url = upload_to_s3(audio_url, s3_key)

            # Process and save transcription data to Databricks
            process_transcription_to_databricks(
                meeting_id, platform, transcription, s3_url, DELTA_TABLE_PATH
            )
        except Exception as e:
            print(f"Error processing recording {recording['id']}: {e}")


@shared_task
def process_zoom_recording(meeting_id, access_token):
    """
    Task to process a Zoom meeting recording:
    1. Fetch recordings from the Zoom API.
    2. Transcribe the recordings.
    3. Upload the recordings to AWS S3.
    4. Save the data in the database.

    Args:
        meeting_id (str): The ID of the Zoom meeting.
        access_token (str): The access token for Zoom API.

    Returns:
        dict: A summary of the processed recordings.
    """
    recordings = get_zoom_recordings(meeting_id, access_token)
    if "error" in recordings:
        return {"error": recordings["error"]}

    results = []
    for recording in recordings:
        try:
            # Transcribe the recording
            audio_url = recording["download_url"]
            job_name = f"zoom-transcription-{recording['id']}"
            transcription = transcribe_audio(audio_url, job_name)

            # Upload the recording to S3
            s3_key = f"recordings/{recording['id']}.mp4"
            s3_url = upload_to_s3(audio_url, s3_key)

            # Save to database
            meeting, _ = Meeting.objects.get_or_create(
                meeting_id=meeting_id,
                defaults={
                    "transcription_text": transcription,
                    "recording_url": s3_url,
                    "s3_key": s3_key,
                }
            )

            results.append({
                "recording_id": recording["id"],
                "transcription": transcription,
                "s3_url": s3_url,
            })
        except Exception as e:
            results.append({"recording_id": recording["id"], "error": str(e)})

    return {"meeting_id": meeting_id, "results": results}

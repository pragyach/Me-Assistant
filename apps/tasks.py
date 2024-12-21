from celery import shared_task
from .utils import get_zoom_recordings, transcribe_audio, upload_to_s3
from .models import Meeting

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

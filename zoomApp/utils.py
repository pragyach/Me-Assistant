import requests
import boto3
from .models import Meeting
from .utils import transcribe_audio, upload_to_s3

# Zoom Integration

def get_zoom_recordings(meeting_id, access_token):
    """
    Fetch recordings from Zoom API.

    Args:
        meeting_id (str): The Zoom meeting ID.
        access_token (str): The OAuth 2.0 access token for Zoom API.

    Returns:
        list: List of recording details or an error dictionary.
    """
    url = f"https://api.zoom.us/v2/meetings/{meeting_id}/recordings"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("recording_files", [])
    return {"error": response.json()}

def zoom_recording_to_text_and_upload(meeting_id, access_token):
    """
    Process Zoom recordings: fetch, transcribe, and upload to AWS S3.

    Args:
        meeting_id (str): The Zoom meeting ID.
        access_token (str): The OAuth 2.0 access token for Zoom API.

    Returns:
        dict: Details of the processed recordings.
    """
    recordings = get_zoom_recordings(meeting_id, access_token)
    if "error" in recordings:
        return recordings

    results = []
    for recording in recordings:
        try:
            # Fetch the audio URL and initiate transcription
            audio_url = recording["download_url"]
            job_name = f"zoom-transcription-{recording['id']}"
            transcription = transcribe_audio(audio_url, job_name)

            # Upload the recording to S3
            s3_key = f"recordings/zoom/{recording['id']}.mp4"
            s3_url = upload_to_s3(audio_url, s3_key)

            # Save the processed details to the database
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

# GMeet Integration

def get_gmeet_recordings(meeting_id, access_token):
    """
    Fetch recordings from Google Meet API.

    Args:
        meeting_id (str): The Google Meet meeting ID.
        access_token (str): The OAuth 2.0 access token for Google APIs.

    Returns:
        list: List of recording details or an error dictionary.
    """
    url = f"https://www.googleapis.com/calendar/v3/calendars/{meeting_id}/events"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("recordings", [])
    return {"error": response.json()}

def gmeet_recording_to_text_and_upload(meeting_id, access_token):
    """
    Process Google Meet recordings: fetch, transcribe, and upload to AWS S3.

    Args:
        meeting_id (str): The Google Meet meeting ID.
        access_token (str): The OAuth 2.0 access token for Google APIs.

    Returns:
        dict: Details of the processed recordings.
    """
    recordings = get_gmeet_recordings(meeting_id, access_token)
    if "error" in recordings:
        return recordings

    results = []
    for recording in recordings:
        try:
            # Fetch the audio URL and initiate transcription
            audio_url = recording["downloadUrl"]
            job_name = f"gmeet-transcription-{recording['id']}"
            transcription = transcribe_audio(audio_url, job_name)

            # Upload the recording to S3
            s3_key = f"recordings/gmeet/{recording['id']}.mp4"
            s3_url = upload_to_s3(audio_url, s3_key)

            # Save the processed details to the database
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

# Microsoft Teams Integration

def get_teams_recordings(meeting_id, access_token):
    """
    Fetch recordings from Microsoft Teams API.

    Args:
        meeting_id (str): The Microsoft Teams meeting ID.
        access_token (str): The OAuth 2.0 access token for Microsoft APIs.

    Returns:
        list: List of recording details or an error dictionary.
    """
    url = f"https://graph.microsoft.com/v1.0/me/onlineMeetings/{meeting_id}/recordings"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("recordings", [])
    return {"error": response.json()}

def teams_recording_to_text_and_upload(meeting_id, access_token):
    """
    Process Microsoft Teams recordings: fetch, transcribe, and upload to AWS S3.

    Args:
        meeting_id (str): The Microsoft Teams meeting ID.
        access_token (str): The OAuth 2.0 access token for Microsoft APIs.

    Returns:
        dict: Details of the processed recordings.
    """
    recordings = get_teams_recordings(meeting_id, access_token)
    if "error" in recordings:
        return recordings

    results = []
    for recording in recordings:
        try:
            # Fetch the audio URL and initiate transcription
            audio_url = recording["contentUrl"]
            job_name = f"teams-transcription-{recording['id']}"
            transcription = transcribe_audio(audio_url, job_name)

            # Upload the recording to S3
            s3_key = f"recordings/teams/{recording['id']}.mp4"
            s3_url = upload_to_s3(audio_url, s3_key)

            # Save the processed details to the database
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

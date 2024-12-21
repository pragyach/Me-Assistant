from .models import Meeting
from .utils import transcribe_audio, upload_to_s3
import requests

def get_zoom_recordings(meeting_id, access_token):
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
    recordings = get_zoom_recordings(meeting_id, access_token)
    if "error" in recordings:
        return recordings

    results = []
    for recording in recordings:
        try:
            audio_url = recording["download_url"]
            job_name = f"zoom-transcription-{recording['id']}"
            transcription = transcribe_audio(audio_url, job_name)

            s3_key = f"recordings/zoom/{recording['id']}.mp4"
            s3_url = upload_to_s3(audio_url, s3_key)

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

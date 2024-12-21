import requests
import boto3

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

def transcribe_audio(audio_url, job_name):
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
    s3 = boto3.client("s3")
    bucket = "your-s3-bucket-name"
    response = requests.get(file_url, stream=True)
    s3.upload_fileobj(response.raw, bucket, file_key)
    return f"https://{bucket}.s3.amazonaws.com/{file_key}"

def zoom_recording_to_text_and_upload(meeting_id, access_token):
    recordings = get_zoom_recordings(meeting_id, access_token)
    results = []
    for recording in recordings:
        audio_url = recording["download_url"]
        job_name = f"zoom-transcription-{recording['id']}"
        transcription = transcribe_audio(audio_url, job_name)
        s3_key = f"recordings/{recording['id']}.mp4"
        s3_url = upload_to_s3(audio_url, s3_key)
        results.append({"recording_id": recording["id"], "transcription": transcription, "s3_url": s3_url})
    return results

from django.shortcuts import render
from .utils import zoom_recording_to_text_and_upload

def list_meetings_and_notes(request):
    access_token = "your-zoom-access-token"
    meeting_ids = ["meeting_id_1", "meeting_id_2"]  # Example meeting IDs
    meeting_data = []

    for meeting_id in meeting_ids:
        results = zoom_recording_to_text_and_upload(meeting_id, access_token)
        meeting_data.append({"meeting_id": meeting_id, "results": results})

    return render(request, "meetings_and_notes.html", {"meeting_data": meeting_data})

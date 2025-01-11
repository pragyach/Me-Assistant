from django.shortcuts import render
from .zoom import zoom_recording_to_text_and_upload
from django.shortcuts import render
from databricks_utils import query_delta_table

def list_meetings_and_notes(request):
    access_token = "your-zoom-access-token"
    meeting_ids = ["meeting_id_1", "meeting_id_2"]  # Example meeting IDs
    meeting_data = []

    for meeting_id in meeting_ids:
        results = zoom_recording_to_text_and_upload(meeting_id, access_token)
        meeting_data.append({"meeting_id": meeting_id, "results": results})

    return render(request, "meetings_and_notes.html", {"meeting_data": meeting_data})


# Delta Lake table path
DELTA_TABLE_PATH = "s3://your-bucket-name/meetings/"

def analytics_dashboard(request):
    # Query Delta Lake for transcription data
    transcription_data = query_delta_table(DELTA_TABLE_PATH)
    
    # Prepare data for rendering (e.g., count by platform or sentiment)
    platform_data = transcription_data.groupBy("platform").count().collect()
    sentiment_data = transcription_data.groupBy("sentiment").count().collect()

    return render(request, "analytics_dashboard.html", {
        "platform_data": platform_data,
        "sentiment_data": sentiment_data,
    })


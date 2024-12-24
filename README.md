# Meeting Assistant Project

## Overview
Meeting Assistant is a Django-based application enhanced with Databricks integration for scalable transcription storage, Natural Language Processing (NLP) for transcription analysis, and an analytics dashboard for real-time insights. It supports Zoom, Google Meet, and Microsoft Teams for managing recordings.

## Features
- Fetch recordings from Zoom, Google Meet, and Microsoft Teams.
- Transcribe recordings using AWS Transcribe.
- Perform NLP tasks like sentiment analysis and topic extraction on transcription data.
- Store transcription metadata in PostgreSQL and Delta Lake for efficient querying.
- Visualize data trends in an analytics dashboard.

## Tech Stack
### Backend
- **Django**: Web framework for handling APIs, database operations, and view rendering.
- **Celery**: For asynchronous task processing.
- **Databricks**: For scalable transcription data storage and analytics.
- **Delta Lake**: Provides ACID-compliant, scalable data storage on S3.

### APIs
- **Zoom API**: Fetch meeting recordings programmatically.
- **Google Meet API**: Manage and process Google Meet recordings.
- **Microsoft Teams API**: Integrate Microsoft Teams for recording management.

### Cloud Services
- **AWS S3**: Scalable storage for audio files and transcription metadata.
- **AWS Transcribe**: Automatic transcription of audio recordings.

### NLP
- **Hugging Face Transformers**: Sentiment analysis for transcription data.
- **Spark NLP**: Tokenization and topic extraction.

### Frontend
- **HTML/CSS**: For rendering the analytics dashboard.

## Setup
### Prerequisites
1. Python 3.8+
2. Redis server (for Celery)
3. AWS credentials for S3 and Transcribe
4. Databricks account with Delta Lake configured
5. Zoom, Google Meet, and Microsoft Teams API credentials

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/meeting-assistant.git
   cd meeting-assistant
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory and add:
     ```env
     AWS_ACCESS_KEY_ID=your-aws-access-key
     AWS_SECRET_ACCESS_KEY=your-aws-secret-key
     S3_BUCKET_NAME=your-s3-bucket-name
     DATABRICKS_HOST=your-databricks-host
     DATABRICKS_TOKEN=your-databricks-token
     ZOOM_API_KEY=your-zoom-api-key
     GMEET_CLIENT_ID=your-google-client-id
     TEAMS_API_KEY=your-teams-api-key
     CELERY_BROKER_URL=redis://localhost:6379/0
     ```

5. Run database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Start the server:
   ```bash
   python manage.py runserver
   ```

7. Start the Celery worker:
   ```bash
   celery -A mili_project worker --loglevel=info
   ```

## Usage
1. Process recordings from a platform (Zoom, Google Meet, or Teams):
   - Trigger tasks via Celery to fetch and process recordings.
   - Transcriptions and metadata will be stored in Delta Lake and PostgreSQL.

2. View analytics:
   - Access the analytics dashboard at `/analytics/`.
   - Insights include platform usage trends and sentiment analysis.

## Example Workflow
### Processing Recordings
```python
from zoom_app.tasks import process_recordings

# Example for Zoom
platform = "Zoom"
meeting_id = "example_zoom_meeting"
access_token = "example_access_token"
process_recordings.delay(platform, meeting_id, access_token)
```

### Analytics Dashboard
```python
# Query analytics data
from databricks_utils import query_delta_table

data = query_delta_table("s3://your-bucket-name/meetings/")
data.show()
```

### High-Level Architecture
                    +-------------------------------+
                    |       Load Balancer           |
                    +-------------------------------+
                        |                |
            +-----------------+    +-----------------+
            |     Web Server  |    |  Web Server     |
            |   (Django/ASGI) |    |   (Django)      |
            +-----------------+    +-----------------+
                        |                |
                        +----------------+
                                |
         +---------------------------------------------+
         |                Message Broker               |
         |           (Redis for WebSockets)           |
         +---------------------------------------------+
                                |
              +---------------------+---------------------+
              |                     |                     |
  +--------------------+   +--------------------+   +--------------------+
  |   Task Queue (API)  |   |   File Storage    |   | Database (RDS)     |
  |   (Celery + Redis)  |   |   (AWS S3)        |   | Postgres/Delta)    |
  +--------------------+   +--------------------+   +--------------------+
              |                     |                     |
   +------------------+  +--------------------+  +-----------------------+
   | Transcription API |  | Recording Files   |  | Metadata & Insights   |
   | (AWS Transcribe)  |  | & Transcripts     |  | (User-facing queries) |
   +------------------+  +--------------------+  +-----------------------+


## Testing
Run the tests to validate the application:
```bash
python manage.py test
```

## Future Enhancements
- Support additional video conferencing platforms.
- Extend NLP processing to include summarization and entity extraction.
- Add role-based authentication for better user management.
- Real-time transcription monitoring with WebSockets.

## Key Features Implemented
- Scalable data storage with Databricks and Delta Lake.
- NLP tasks for sentiment analysis and topic extraction.
- Analytics dashboard for transcription insights.
- Asynchronous task processing with Celery.



Let me know if you need additional help or have further questions! 🚀

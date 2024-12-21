# Meeting Assistant Project

## Overview
Meeting Assistant is a Django-based application designed to help officials seamlessly manage Zoom meeting recordings and transcriptions. It integrates with Zoom API, AWS S3, and AWS Transcribe to fetch, process, and store recordings in an efficient and scalable manner.

## Features
- Fetch recordings from the Zoom API using OAuth tokens.
- Transcribe recordings using AWS Transcribe for automated note-taking.
- Upload recordings to AWS S3 for secure and scalable storage.
- Store and manage transcription data in a relational database using Django ORM.
- Display meeting details and their respective transcriptions on a user-friendly HTML interface.

## Tech Stack

### 1. **Django**
- **Why:**
  Django provides a high-level web framework with built-in features like ORM, admin interface, and routing. Its modular structure allowed us to develop a scalable application with minimal effort.
- **Useful Links:**
  - [Django Official Documentation](https://docs.djangoproject.com/)
  - [Django Tutorials](https://www.djangoproject.com/start/)

### 2. **Celery with Redis**
- **Why:**
  Celery handles asynchronous task execution, such as processing Zoom recordings and uploading files to S3 without blocking the main application thread. Redis serves as the message broker for task queues.
- **Useful Links:**
  - [Celery Documentation](https://docs.celeryproject.org/)
  - [Redis Official Site](https://redis.io/)

### 3. **Zoom API**
- **Why:**
  The Zoom API enables us to fetch meeting recordings programmatically, providing a seamless integration with existing Zoom accounts.
- **Useful Links:**
  - [Zoom API Documentation](https://marketplace.zoom.us/docs/api-reference/introduction)
  - [Creating a Zoom OAuth App](https://marketplace.zoom.us/docs/guides/build/oauth)

### 4. **AWS S3**
- **Why:**
  AWS S3 is used for storing meeting recordings securely. Its scalability and availability ensure the application can handle large files efficiently.
- **Useful Links:**
  - [AWS S3 Overview](https://aws.amazon.com/s3/)
  - [AWS CLI for S3](https://aws.amazon.com/cli/)

### 5. **AWS Transcribe**
- **Why:**
  AWS Transcribe automates the transcription of meeting recordings into text. It eliminates the need for manual note-taking and ensures high accuracy.
- **Useful Links:**
  - [AWS Transcribe Documentation](https://aws.amazon.com/transcribe/)
  - [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

### 6. **HTML and CSS**
- **Why:**
  Used to create a simple, user-friendly interface for displaying meeting details and transcriptions.
- **Useful Links:**
  - [HTML Tutorial](https://www.w3schools.com/html/)
  - [CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS)

### 7. **SQLite (Development)** / **PostgreSQL (Production)**
- **Why:**
  SQLite is lightweight and perfect for development environments, while PostgreSQL is a robust relational database suitable for production with large-scale data requirements.
- **Useful Links:**
  - [SQLite Documentation](https://www.sqlite.org/docs.html)
  - [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)

### 8. **Testing Frameworks**
- **Django TestCase:** Used for unit testing the application.
- **unittest.mock:** Mocking external services like Zoom API, AWS S3, and AWS Transcribe.
- **Useful Links:**
  - [Django Testing](https://docs.djangoproject.com/en/dev/topics/testing/overview/)
  - [Python Mock Documentation](https://docs.python.org/3/library/unittest.mock.html)

## Setup

### Prerequisites
1. Python 3.8+
2. Redis server (for Celery)
3. AWS credentials (for S3 and Transcribe)
4. Zoom OAuth App credentials

### Installation
1. Clone this repository:
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

4. Configure environment variables:
   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```env
     AWS_ACCESS_KEY_ID=your-aws-access-key
     AWS_SECRET_ACCESS_KEY=your-aws-secret-key
     S3_BUCKET_NAME=your-s3-bucket-name
     ZOOM_OAUTH_TOKEN=your-zoom-oauth-token
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
   celery -A meeting_assistant worker --loglevel=info
   ```

## Usage
1. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/meetings/
   ```
2. View a list of meetings with their transcriptions and recording links.

## Testing
Run the tests to validate the application:
```bash
python manage.py test
```

## Future Enhancements
- Add user authentication to manage individual Zoom accounts securely.
- Implement real-time updates for transcription progress using WebSockets.
- Support additional video conferencing platforms (e.g., Microsoft Teams, Google Meet).


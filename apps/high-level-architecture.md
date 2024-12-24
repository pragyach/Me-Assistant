```mermaid
graph TD
    A[Load Balancer] -->|Distributes traffic| B(Web Server 1: Django/ASGI)
    A -->|Distributes traffic| C(Web Server 2: Django/ASGI)
    
    subgraph Web Servers
        B --> D[Redis: Message Broker]
        C --> D
    end

    D -->|WebSocket Messaging| E[Real-Time Updates]

    subgraph Backend Services
        E --> F[Task Queue: Celery + Redis]
        F --> G[Transcription API: AWS Transcribe]
        F --> H[Database: PostgreSQL/RDS]
        E --> H
        H -->|Query Metadata| I[Analytics & Insights]
        F --> J[File Storage: AWS S3]
    end

    J -->|Store Recordings| H

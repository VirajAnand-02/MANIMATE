# AI Video Generation Pipeline - API Integration

This document explains the integrated API architecture between the Node.js middleware server and the Python FastAPI backend.

## Architecture Overview

```
Frontend (React/Web) 
    ↓ HTTP Requests
Node.js Server (Port 5001) - Middleware & Video Streaming
    ↓ HTTP Requests  
Python FastAPI Server (Port 8001) - Core AI Video Generation
    ↓ Generates Videos
File System (renders/, archives/)
```

## Server Responsibilities

### Node.js Server (`index.js`) - Port 5001
- **Middleware Layer**: Handles frontend communication
- **Database Management**: Firebase operations for user sessions
- **Video Streaming**: Serves generated videos with range support
- **Real-time Updates**: SSE connections for live script updates
- **API Forwarding**: Forwards requests to Python API

### Python FastAPI Server (`main.py`) - Port 8001
- **Core AI Logic**: LLM script generation and video creation
- **Background Processing**: Asynchronous video generation jobs
- **Token Management**: Script versioning and storage
- **Job Monitoring**: Progress tracking and status management

## API Flow Documentation

### 1. Script Generation Flow

#### Step 1: Initial Request
```javascript
POST /submit
Body: { text: "topic", uid: "user123", chatID: "chat456" }
```

**Process:**
1. Node.js receives frontend request
2. Node.js → Python API: `POST /api/generate_scripts`
3. Python generates 3 script variations with tokens
4. Node.js polls Python API for script completion
5. Node.js updates Firebase database
6. Node.js returns completed scripts to frontend

#### Step 2: Script Polling (Internal)
```javascript
// Node.js polls Python API
GET /api/script/{token}
```

### 2. Script Update Flow

#### Frontend Update Request
```javascript
POST /update_script/{token}
Body: { script: {updated_script_data}, chatID: "chat456" }
```

**Process:**
1. Node.js receives script updates
2. Node.js → Python API: `POST /api/script/{token}`
3. Python API validates and stores updated script
4. Node.js updates Firebase database
5. Node.js confirms update to frontend

### 3. Video Generation Flow

#### Script Confirmation & Generation Start
```javascript
POST /confirm_script/{token}
Body: { chatID: "chat456", config: {generation_options} }
```

**Process:**
1. Node.js receives generation request
2. Node.js → Python API: `POST /api/generate/{token}`
3. Python API starts background video generation job
4. Python returns job_id for progress tracking
5. Node.js returns job_id to frontend

#### Progress Monitoring
```javascript
GET /generation_status/{job_id}
```

**Process:**
1. Frontend/Node.js polls for progress
2. Node.js → Python API: `GET /api/job/{job_id}`
3. Python returns current job status and progress
4. Node.js forwards status to frontend

## Environment Configuration

### Node.js Server (.env)
```bash
PORT=5001
PYTHON_API_URL=http://localhost:8001
# Firebase config...
```

### Python Server (.env)
```bash
PYTHON_API_PORT=8001
GOOGLE_API_KEY=your_api_key
TTS_PROVIDER=gemini
TTS_VOICE_NAME=Kore
# Other AI service keys...
```

## API Endpoints Reference

### Node.js Endpoints (Port 5001)

#### Core Functionality
- `POST /submit` - Start script generation process
- `POST /update_script/{token}` - Update existing script
- `POST /confirm_script/{token}` - Start video generation
- `GET /generation_status/{job_id}` - Check generation progress

#### Video Management
- `GET /videos` - List available videos
- `GET /stream/{filename}` - Stream video with range support
- `GET /download/{filename}` - Download video file

#### Real-time Features
- `GET /events/{chatID}` - SSE connection for live updates

#### System
- `GET /health` - Health check
- `GET /generation_jobs` - List all generation jobs
- `DELETE /generation_job/{job_id}` - Delete generation job

### Python FastAPI Endpoints (Port 8001)

#### Script Management
- `POST /api/generate_scripts` - Generate script variations
- `GET /api/script/{token}` - Get script by token
- `POST /api/script/{token}` - Update script

#### Video Generation
- `POST /api/generate/{token}` - Start video generation
- `GET /api/job/{job_id}` - Get job status
- `GET /api/jobs` - List jobs
- `DELETE /api/job/{job_id}` - Delete job

#### System
- `GET /` - API information
- `POST /api/validate_config` - Validate system configuration

## Data Flow Examples

### Example 1: Complete Script Generation
```json
1. POST /submit
   Request: {"text": "quantum computing", "uid": "user123", "chatID": "chat456"}
   
2. Internal: POST /api/generate_scripts
   Request: {"topic": "quantum computing", "quality": "high", ...}
   Response: {"tokens": ["abc123", "def456", "ghi789"]}
   
3. Internal Polling: GET /api/script/abc123
   Response: {"title": "Quantum Computing", "scenes": [...]}
   
4. Final Response:
   {"success": true, "scripts": [...], "tokens": [...], "chatID": "chat456"}
```

### Example 2: Script Update
```json
1. POST /update_script/abc123
   Request: {"script": {"title": "Updated Title", ...}, "chatID": "chat456"}
   
2. Internal: POST /api/script/abc123
   Request: {"title": "Updated Title", ...}
   
3. Response: {"success": true, "script": {...}, "token": "abc123"}
```

### Example 3: Video Generation
```json
1. POST /confirm_script/abc123
   Request: {"chatID": "chat456", "config": {"quality": "high"}}
   
2. Internal: POST /api/generate/abc123
   Response: {"job_id": "job_xyz", "status": "pending"}
   
3. Progress Check: GET /generation_status/job_xyz
   Response: {"job_status": {"status": "running", "progress": 45.0}}
```

## Error Handling

### Node.js Error Responses
```json
{
  "success": false,
  "message": "Error description",
  "error": "Detailed error message"
}
```

### Python API Error Responses
```json
{
  "detail": "Error description"
}
```

## Starting the Servers

### Option 1: Using Scripts
```bash
# Linux/Mac
./start-servers.sh

# Windows
start-servers.bat
```

### Option 2: Manual Start
```bash
# Terminal 1: Start Python API
cd langChan_tst
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py api

# Terminal 2: Start Node.js server
cd status-code-2
npm start
```

## Development Notes

### Token Management
- Each script generation creates unique tokens
- Tokens are used for script retrieval and updates
- Tokens persist across server restarts (stored in Python API memory)

### Job Management
- Video generation jobs run asynchronously
- Jobs have unique IDs for tracking
- Progress is reported as percentage (0-100)
- Job status: "pending", "running", "completed", "failed"

### Database Sync
- Firebase stores user sessions and script states
- Node.js handles all database operations
- Python API focuses on computation and processing

### Video Storage
- Generated videos stored in `langChan_tst/renders/`
- Node.js serves videos from configured directory
- Supports video streaming with range requests

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   - Ensure ports 5001 and 8001 are available
   - Check environment variables are set correctly

2. **API Communication Errors**
   - Verify PYTHON_API_URL is set correctly in Node.js
   - Check both servers are running and accessible

3. **Script Generation Timeouts**
   - Check Google API key configuration
   - Verify Python API is processing requests

4. **Video Generation Failures**
   - Check Python API logs for detailed errors
   - Ensure all dependencies are installed

### Monitoring
- Node.js console shows request forwarding
- Python API provides detailed logging
- Use `/health` endpoints to check server status
- FastAPI docs available at `http://localhost:8001/docs`

## Security Considerations

- Add API key validation between Node.js and Python API
- Implement rate limiting for script generation
- Add user authentication and authorization
- Secure video file access with proper permissions
- Use HTTPS in production deployments

# AI Video Generation - Node.js Middleware Server

This Node.js server acts as a middleware layer between the frontend and the Python FastAPI backend for AI-powered video generation.

## Quick Start

### Prerequisites
- Node.js 16+ installed
- Python server running on port 8001
- Firebase project configured (if using database features)

### Installation
```bash
npm install
```

### Configuration
1. Copy `.env.example` to `.env`
2. Update environment variables:
```bash
PORT=5001
PYTHON_API_URL=http://localhost:8001
# Add Firebase config if needed
```

### Running the Server
```bash
# Start the server
npm start

# Run integration tests
npm test
```

### Starting Both Servers
```bash
# Linux/Mac
./start-servers.sh

# Windows
start-servers.bat
```

## API Endpoints

### Script Generation
- `POST /submit` - Generate script variations
- `POST /update_script/:token` - Update existing script
- `POST /confirm_script/:token` - Start video generation

### Video Management
- `GET /videos` - List available videos
- `GET /stream/:filename` - Stream video
- `GET /download/:filename` - Download video

### Generation Monitoring
- `GET /generation_status/:job_id` - Check progress
- `GET /generation_jobs` - List all jobs
- `DELETE /generation_job/:job_id` - Delete job

### Real-time Features
- `GET /events/:chatID` - SSE connection for live updates

## Architecture

```
Frontend → Node.js (Port 5001) → Python API (Port 8001)
         ↓
    Firebase DB
         ↓
    Video Files
```

## Integration Flow

1. **Script Generation**: Frontend → Node.js → Python API
2. **Script Updates**: Frontend → Node.js → Python API → Firebase
3. **Video Generation**: Frontend → Node.js → Python API (background job)
4. **Progress Monitoring**: Frontend → Node.js → Python API

## Testing

Run the integration test to verify everything is working:
```bash
npm test
```

This will test:
- Server connectivity
- Script generation flow
- Script updates
- Video generation initiation
- Job status monitoring

## Troubleshooting

### Server Not Starting
- Check if port 5001 is available
- Verify all dependencies are installed: `npm install`

### Python API Communication Issues
- Ensure Python server is running on port 8001
- Check `PYTHON_API_URL` in `.env` file
- Verify network connectivity between servers

### Video Streaming Issues
- Check video file permissions
- Verify `VIDEO_STORAGE_PATH` configuration
- Ensure video files exist in the specified directory

## Development

### Adding New Endpoints
1. Add route handler in `index.js`
2. Forward to Python API if needed
3. Update database if required
4. Add tests in `test-integration.js`

### Debugging
- Check console logs for request/response details
- Use `/health` endpoint to verify server status
- Monitor Python API logs for backend issues

## Production Deployment

### Security Considerations
- Add API key validation
- Implement rate limiting
- Use HTTPS
- Add authentication middleware
- Secure video file access

### Performance
- Configure proper caching headers
- Use a reverse proxy (nginx)
- Monitor resource usage
- Scale horizontally if needed

## Related Documentation
- [API Integration Guide](./API_INTEGRATION_GUIDE.md)
- Python FastAPI documentation
- Frontend integration guide

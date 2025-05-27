# Slide Generator API

AI-powered presentation generator using OpenAI and python-pptx. This application automatically creates PowerPoint presentations from topics using Large Language Models.

## 🏗️ Architecture

```
          ┌────────────────────────────┐
          │        Client (UI)        │
          └────────────┬──────────────┘
                       │ REST API
                       ▼
       ┌──────────────────────────────────────┐
       │         FastAPI App (API Layer)      │
       └──────┬───────────────┬───────────────┘
              │               │
              ▼               ▼
   ┌────────────────┐ ┌─────────────────────┐
   │  Redis Queue   │ │     Database (DB)   │◄───┐
   └────────┬───────┘ └─────────────────────┘    │
            │                                    │
            ▼                                    │
 ┌────────────────────────┐                     │
 │  Worker (Background)   │                     │
 │  [Presentation Builder]│                     │
 └────────┬───────────────┘                     │
          ▼                                     │
 ┌─────────────────────────────┐                │
 │ LLM Client (OpenAI etc.)    │                │
 └─────────────────────────────┘                │
          ▼                                     │
 ┌─────────────────────────────┐                │
 │ PPTX Generator (python-pptx)│──► Generates ──┘
 └─────────────────────────────┘
          ▼
    Slide (.pptx) File Store
```

## 🚀 Features

- **AI-Powered Content Generation**: Uses OpenAI GPT models to generate structured slide content
- **Async Processing**: Background job processing with Redis and RQ
- **RESTful API**: Clean API endpoints for creating, managing, and downloading presentations
- **Professional Styling**: Consistent, professional PowerPoint formatting
- **Flexible Configuration**: Customizable number of slides and presentation settings
- **File Management**: Automatic file storage and download capabilities
- **Job Status Tracking**: Real-time status updates for presentation generation

## 📁 Project Structure

```
app/
├── main.py                  # FastAPI entrypoint
├── database.py              # Database configuration
├── queue.py                 # Redis queue setup
├── api/
│   └── routes.py            # API routes
├── orchestrator/
│   └── presentation_orchestrator.py
├── services/
│   ├── llm_client.py        # OpenAI integration
│   └── pptx_creator.py      # PowerPoint generation
├── models/
│   └── presentation.py      # SQLAlchemy models
├── schemas/
│   └── presentation_schema.py # Pydantic schemas
├── workers/
│   └── tasks.py             # Background job functions
├── utils/
│   └── layout_picker.py     # Layout utilities
presentations/               # Generated files
output_samples/             # Sample outputs
worker.py                   # Worker process script
requirements.txt
README.md
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SlideGenerator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file with:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=sqlite:///./presentations.db
   REDIS_URL=redis://localhost:6379/0
   ```

4. **Start Redis server**
   ```bash
   redis-server
   ```

5. **Start the worker process**
   ```bash
   python worker.py
   ```

6. **Start the API server**
   ```bash
   python app/main.py
   ```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/presentations` | POST | Submit a new presentation (topic, config, content) |
| `/api/v1/presentations/{id}` | GET | Get presentation metadata |
| `/api/v1/presentations/{id}/download` | GET | Download .pptx file |
| `/api/v1/presentations/{id}/configure` | POST | Update number of slides, theme, etc. |
| `/api/v1/presentations/{id}/status` | GET | Get job status |
| `/api/v1/presentations` | GET | List all presentations |

## 🔧 Usage Examples

### Create a Presentation

```bash
curl -X POST "http://localhost:8000/api/v1/presentations" \
     -H "Content-Type: application/json" \
     -d '{
       "topic": "Climate Change",
       "num_slides": 8,
       "config": {"theme": "professional"}
     }'
```

### Check Status

```bash
curl "http://localhost:8000/api/v1/presentations/{presentation_id}/status"
```

### Download Presentation

```bash
curl "http://localhost:8000/api/v1/presentations/{presentation_id}/download" \
     --output presentation.pptx
```

## 🎨 Sample Outputs

The application generates professional presentations with:
- Title slides with topic and overview
- Content slides with structured bullet points
- Conclusion slides with key takeaways
- Consistent professional styling
- Speaker notes for each slide

Sample presentations are stored in `output_samples/`:
- `climate_change.pptx`
- `ai_future.pptx`
- `history_of_internet.pptx`

## 🔐 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for content generation
- `DATABASE_URL`: Database connection string (SQLite or PostgreSQL)
- `REDIS_URL`: Redis connection string for job queue
- `DEBUG`: Enable debug mode (True/False)

### Presentation Configuration

```json
{
  "num_slides": 10,
  "config": {
    "theme": "professional",
    "include_notes": true,
    "slide_size": "16:9"
  }
}
```

## 🚀 Deployment

### Docker Deployment

1. Build the image:
   ```bash
   docker build -t slide-generator .
   ```

2. Run with docker-compose:
   ```bash
   docker-compose up -d
   ```

### Production Considerations

- Use PostgreSQL for production database
- Set up Redis cluster for high availability
- Configure proper CORS origins
- Add authentication and rate limiting
- Use environment-specific configuration
- Set up monitoring and logging

## 🧪 Testing

Run tests with:
```bash
pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🔮 Future Enhancements

- [ ] Authentication and user management
- [ ] Template system for custom themes
- [ ] Image integration from web search
- [ ] Multiple output formats (PDF, HTML)
- [ ] Collaborative editing features
- [ ] Advanced styling options
- [ ] Integration with cloud storage (S3, Google Drive)
- [ ] Real-time preview generation
- [ ] Batch processing capabilities

## Quick Start

The easiest way to start the application is using the startup script:

```bash
./startup.sh
```

This script will:
1. Set up a virtual environment if it doesn't exist
2. Install dependencies
3. Create an `.env` file from template if needed
4. Run database migrations
5. Check if Redis is running
6. Start the worker process
7. Start the FastAPI server

Press Ctrl+C to stop all processes gracefully.

## Manual Setup

### Prerequisites

- Python 3.9+
- Redis server
- (Optional) OpenAI API key or HuggingFace API key

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment template and configure it:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

### Running the Application

1. Start Redis server
   ```bash
   # macOS
   brew services start redis
   
   # Linux
   sudo systemctl start redis
   ```

2. Start the worker process:
   ```bash
   export PYTHONPATH=$(pwd)  # On Windows: set PYTHONPATH=%cd%
   python start_worker.py
   ```

3. In a separate terminal, start the API server:
   ```bash
   export PYTHONPATH=$(pwd)  # On Windows: set PYTHONPATH=%cd%
   python app/main.py
   ```

4. Visit the API documentation at http://localhost:8000/docs

## API Usage

The API provides endpoints for creating, retrieving, updating, and styling presentations.

### Creating a Presentation

```bash
curl -X POST "http://localhost:8000/api/v1/presentations/" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Artificial Intelligence",
    "content": "AI is transforming how we work and live...",
    "num_slides": 5
  }'
```

### Styling a Presentation

```bash
curl -X POST "http://localhost:8000/api/v1/presentations/{presentation_id}/configure-style" \
  -H "Content-Type: application/json" \
  -d '{
    "theme": "corporate",
    "background_color": "#F5F5F5",
    "font": "Arial",
    "title_color": "#003366",
    "content_color": "#333333",
    "accent_color": "#FF6600"
  }'
```

## Style Configuration

The application supports various styling options as documented in [STYLING_OPTIONS.md](docs/STYLING_OPTIONS.md).

## Troubleshooting

If you encounter issues with worker processes on macOS, please refer to the documentation in [docs/MACOS_WORKER_ISSUES.md](docs/MACOS_WORKER_ISSUES.md).
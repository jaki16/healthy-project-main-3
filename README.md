# HealthTrack AI Pro

🏥 Aplikasi kesehatan pintar berbasis PyQt6 dengan AI Assistant dan Smartwatch Integration

## Features

- 🤖 AI Health Assistant
- ⌚ Real-time Smartwatch Sync
- 📊 Advanced Health Analytics
- 🍎 Food Recognition AI
- 📈 Interactive Charts & Visualizations
- 🌙 Dark/Light Theme
- 📱 Activity Auto-Detection

## Installation

```bash
# Clone repository
git clone <your-repo-url>
cd HealthTrack-AI-PyQt6

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys

# Initialize database
python scripts/init_db.py

# Run application
python src/main.py
```

## Development

```bash
# Run tests
pytest

# Format code
black src/

# Lint code
pylint src/
```

## License

MIT License

## Author

Your Name

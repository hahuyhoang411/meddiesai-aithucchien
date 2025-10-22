# Meddies AI - AI Thuc Chien

## Quick Setup

Run the setup script to install dependencies and create a virtual environment:

```bash
./setup.sh
```

This script will:

- Install `uv` package manager from Astral
- Create a Python 3.11 virtual environment (if not exists)
- Install all project dependencies
- Set up the development environment

## Repository Structure

```
meddiesai-aithucchien/
├── core/                           # Core application modules
│   ├── __init__.py
│   ├── ping.py                     # Health check utilities
│   └── settings.py                 # Application settings
├── notebooks/                      # Jupyter notebooks for development
│   ├── Animated_Story_Video_Generation_gemini.ipynb
│   └── Book_illustration.ipynb
├── pyproject.toml                  # Project configuration and dependencies
├── setup.sh                       # Automated setup script
├── uv.lock                        # Dependency lock file
└── README.md                      # This file
```

## Development

After running `setup.sh`, activate the virtual environment:

```bash
source .venv/bin/activate
```

## Testing API Endpoints

Use the ping script to test different API modes:

```bash
# Test text generation (gemini-2.5-flash)
python -m core.ping -m text
# Expected: "PONG!" response

# Test image generation (imagen-4)
python -m core.ping -m image
# Expected: Saves generated_image_1.png

# Test video generation (veo-3.0)
python -m core.ping -m video
# Expected: Saves outputs/generated_video.mp4

# Test text-to-speech (gemini-2.5-flash-preview-tts)
python -m core.ping -m text2speech
# Expected: Saves outputs/generated_speech.mp3
```

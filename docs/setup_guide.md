# Setup Guide

## Requirements

- Python 3
- pip
- OpenAI API key
- Internet connection

## Local Setup

1. Clone the repository.
2. Open the project directory.
3. Create a Python virtual environment.
4. Activate the environment.
5. Install requirements.
6. Configure the .env file.
7. Start the FastAPI server.

## Start Command

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 4000
```

## Access Documentation

Open:

http://127.0.0.1:4000/docs

## Run Tests

```bash
python -m pytest tests/ -v
```

## Troubleshooting

### API key error

Check that OPENAI_API_KEY is configured in .env.

### Module not found

Activate the virtual environment and install requirements.

### Website extraction error

Check whether the website is publicly accessible and
whether it permits automated requests.

### AI provider error

Check API connectivity, account credits, model availability,
and rate limits.

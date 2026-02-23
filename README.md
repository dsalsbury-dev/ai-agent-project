# ai-agent-project

A minimal Python CLI chatbot that sends a single prompt to Google Gemini and prints the response.

## Why does this exist?

I am learning about AI chat bots and using this as a learning opportunity to do some new things.

## Requirements

- Python 3.13 (see [.python-version](.python-version))
- Dependencies are managed in [pyproject.toml](pyproject.toml)

## Setup

1. Create and activate a virtual environment.
2. Install dependencies from [pyproject.toml](pyproject.toml):
   ```bash
   python -m pip install -e .
   ```
3. Create a `.env` file with:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

Run the chatbot from [main.py](main.py):

```bash
python main.py "Write a haiku about coding"
```

Enable verbose token output:

```bash
python main.py "Write a haiku about coding" --verbose
```

## Notes

- The entry point is [`main`](main.py) in [main.py](main.py).
- `.env` is ignored by Git via [.gitignore](.gitignore).

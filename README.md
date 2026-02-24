# ai-agent-project

A minimal Python CLI chatbot that sends a single prompt to Google Gemini and prints either:

- a requested function call, or
- a direct text response.

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

The CLI accepts one required positional argument:

```bash
python main.py "<your prompt>"
```

Optional flag:

```bash
--verbose
```

In [main.py](main.py), responses are handled in two ways:

1. If the LLM decides a function call is needed, it prints:
   ```text
   Calling function: <function_name>({<args>})
   ```
2. Otherwise, it prints a plain text response:
   ```text
   Response:
   <model text>
   ```

### Example prompts

Prompt that typically triggers a function call:

```bash
python main.py "list the contents of pkg directory"
```

Example output:

```text
Calling function: get_files_info({'directory': 'pkg'})
```

Prompt that typically returns direct text:

```bash
python main.py "Write a haiku about coding"
```

Example output:

```text
Response:
Code hums in still night,
Logic blooms in quiet loops,
Dawn debugs the sky.
```

## Notes

- The entry point is [`main`](main.py) in [main.py](main.py).
- `.env` is ignored by Git via [.gitignore](.gitignore).

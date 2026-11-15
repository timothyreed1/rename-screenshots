# rename-screenshots
Rename screenshots based on their visual content using the OpenAI API. Pass filenames on the command line to rename based on content.

## What it does
- The original version analyzes images with OpenAI Vision using your own key. 
- The new version analyzes images with Apple Intelligence.
- Generates a short description filename
- Optionally prepends the YYYYMMDD format create date to the filename
- Renames the file
- Avoids filename collisions

## Requirements
- macOS
- Python 3.9+
- OpenAI API key (version 1) 
- Apple Intelligence (version 2)

## Setup
```bash
pip3 install openai
export OPENAI_API_KEY="sk-..."
chmod +x rename-screenshots.py
```

## Use cases
Rename files
```bash
rename-screenshots.py ~/Downloads/Screenshot\ 2026-01-01\ at\ 10.10.10.png
```

Dry run (no changes)
```bash
rename-screenshots.py --dry-run ~/Downloads/Screenshot\ 2026-01-01\ at\ 10.10.10.png
```

Rename files with "YYYYMMDD - " date prefix
```bash
rename-screenshots.py --date Screenshot\ 2026-01-01\ at\ 10.10.10.png
Screenshot 2026-01-01 at 10.10.10.png -> 20260215 - flickr-rusted_chain-and-bollard-riverwalk.png
```

## Notes

* Preserves original file extensions
* Appends -2, -3, etc. to duplicate filenames
* The original version requires your own ChatGPT API key
* The latest version requires Apple Intelligence locally

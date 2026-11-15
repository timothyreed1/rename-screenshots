# rename-screenshots
Rename screenshots based on their visual content using OpenAI (version 1) or on-device Apple Intelligence (version 2). Pass filenames on the command line to rename based on content.

## What it does
- The original version analyzes images with OpenAI Vision using your own key. 
- The new version analyzes images with Apple Intelligence.
- Generates a short description filename
- Optionally prepends the YYYYMMDD format create date to the filename
- Renames the file
- Avoids filename collisions

## Requirements
- macOS
- Version 1 (OpenAI): Python 3.9+ and an OpenAI API key
- Version 2 (Apple Intelligence): macOS 26+, Apple Intelligence turned on, Xcode 26+ with its license accepted, and Python 3.10+

## Setup
Version 1 (OpenAI)
```bash
pip3 install openai
export OPENAI_API_KEY="sk-..."
chmod +x rename-screenshots.py
```

Version 2 (Apple Intelligence)
```bash
pip3 install apple-fm-sdk
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

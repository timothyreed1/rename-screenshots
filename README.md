# rename-screenshots
Rename screenshots based on their visual content using the OpenAI API. Pass filenames on the command line to rename based on content.

## What it does
- Analyzes each image with an OpenAI vision model
- Generates a short, descriptive, filename-safe title
- Renames the file
- Avoids filename collisions automatically

## Requirements
- macOS
- Python 3.9+
- OpenAI API key

## Setup
```bash
pip3 install openai pillow
export OPENAI_API_KEY="sk-..."

## Usage
Make the script executable
```bash
chmod +x rename_screenshots.py

Rename files
```bash
rename-screenshots.py ~/Downloads/Screenshot\ 2026-01-01\ at\ 10.10.10.png

Dry run (no changes)
```bash
rename-screenshots.py --dry-run ~/Downloads/Screenshot\ 2026-01-01\ at\ 10.10.10.png

## Notes
* Supports PNG, JPG, JPEG, WEBP
* Preserves original file extensions
* Appends -2, -3, etc. to duplicate filenames
* Requires your own ChatGPT API key

#!/usr/bin/env python3
"""
rename-screenshot.py
Rename screenshots based on their visual content using the OpenAI API. 
Pass filenames on the command line to rename based on content.

The script accepts one or more image paths as command-line arguments,
analyzes each image to generate a concise, descriptive filename, and
renames the file in place. Only files explicitly passed on the command
line are processed.

- Supports PNG, JPG, JPEG, WEBP
- Preserves original file extensions
- Appends -2, -3, etc. to duplicate filenames
- Requires your own ChatGPT API key

Usage:
  ./rename_screenshots.py [--dry-run] <file1> <file2> ...

Requirements:
- Python 3.9+
- OPENAI_API_KEY set in the environment
- openai and pillow Python packages

Note:
API usage incurs OpenAI costs.

"""

import os
import sys
import base64
import time
from openai import OpenAI

client = OpenAI()

def encode_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def sanitize(text: str, max_len: int = 80) -> str:
    text = text.strip().lower()
    # keep it filename-safe
    allowed = []
    for ch in text:
        if ch.isalnum() or ch in ("-", "_"):
            allowed.append(ch)
        elif ch.isspace():
            allowed.append("-")
        # drop everything else
    out = "".join(allowed)
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-_")[:max_len] or "untitled"

def unique_path(dirpath: str, base: str, ext: str) -> str:
    candidate = os.path.join(dirpath, f"{base}{ext}")
    if not os.path.exists(candidate):
        return candidate
    i = 2
    while True:
        candidate = os.path.join(dirpath, f"{base}-{i}{ext}")
        if not os.path.exists(candidate):
            return candidate
        i += 1

def guess_ext(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in (".png", ".jpg", ".jpeg", ".webp"):
        return ext
    return ".png"

def rename_one(path: str, dry_run: bool = False) -> None:
    if not os.path.exists(path):
        print(f"SKIP (not found): {path}", file=sys.stderr)
        return
    if os.path.isdir(path):
        print(f"SKIP (directory): {path}", file=sys.stderr)
        return

    ext = guess_ext(path)

    # Use correct mime type for data URL
    mime = "image/png"
    if ext == ".jpg" or ext == ".jpeg":
        mime = "image/jpeg"
    elif ext == ".webp":
        mime = "image/webp"

    image_b64 = encode_image(path)

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Create a concise 5–8 word filename for this screenshot. Include app/site name if visible. No punctuation."},
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{image_b64}"}},
                ],
            }
        ],
        max_tokens=40,
    )

    description = resp.choices[0].message.content.strip()
    base = sanitize(description)
    dirpath = os.path.dirname(os.path.abspath(path))
    new_path = unique_path(dirpath, base, ext)

    if dry_run:
        print(f"{path} -> {new_path}")
    else:
        os.rename(path, new_path)
        print(f"{path} -> {new_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: rename_screenshots.py [--dry-run] <file1> <file2> ...", file=sys.stderr)
        sys.exit(2)

    args = sys.argv[1:]
    if "--dry-run" in args or "--dryrun" in args:
        dry_run = True
        args = [a for a in args if a not in ("--dry-run", "--dryrun" )]

    for p in args:
        rename_one(p, dry_run=dry_run)
        time.sleep(0.2)  # small pause to reduce rate-limit risk

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
rename-screenshots.py
Rename screenshots based on their visual content using Apple Intelligence.
Pass filenames on the command line to rename based on content.

The script accepts one or more filenames on the command line, analyzes each image
with on-device Apple Intelligence to generate a short filename, and renames the file
in place. 

- Supports PNG, JPG, JPEG, WEBP
- Preserves original file extensions
- Appends -2, -3, etc. to duplicate filenames
- Runs entirely on-device

Usage:
  ./rename-screenshots.py [--dry-run] [--date] [--help] <file1> <file2> ...

Requirements:
- macOS 26+ with Apple Intelligence turned on
- Xcode 26+ installed with its license accepted
- Python 3.10+
- apple-fm-sdk Python package
"""

import os
import sys
import asyncio
from datetime import datetime
from pathlib import Path

import apple_fm_sdk as fm

PROMPT = (
    "Create a concise 5-6 word description of this image that would be good for a filename. "
    "Do not use punctuation in description."
)

HELP = """\
Usage: rename-screenshots.py [--dry-run] [--date] [--help] <file1> <file2> ...

Rename screenshots based on their visual content using Apple Intelligence.
Each file is renamed in place to a short descriptive name and original file 
extension. Duplicate names get -2, -3, etc. appended to the filename.

Arguments:
  <file> ...    One or more image files to rename (PNG, JPG, JPEG, WEBP).

Options:
  --dry-run     Show the new names without renaming anything. --dryrun works too.
  --date        Prefix the new name with the file's creation date in YYYYMMDD format.
  -h, --help    Show this help and exit.

Requires Apple Intelligence turned on and the apple-fm-sdk package.
"""

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

def get_creation_date(path: str) -> str:
    """Get file creation date in YYYYMMDD format"""
    stat = os.stat(path)
    # Use birth time if available (macOS), otherwise fall back to mtime
    timestamp = getattr(stat, "st_birthtime", stat.st_mtime)
    return datetime.fromtimestamp(timestamp).strftime("%Y%m%d")

async def describe(path: str) -> str:
    # Fresh session per image so earlier images don't influence later names
    session = fm.LanguageModelSession()
    image = fm.ImageAttachment(path=Path(path).resolve())
    response = await session.respond([PROMPT, image])
    return str(response).strip()

async def rename_one(path: str, dry_run: bool = False, use_date: bool = False) -> None:
    if not os.path.exists(path):
        print(f"SKIP (not found): {path}", file=sys.stderr)
        return
    if os.path.isdir(path):
        print(f"SKIP (directory): {path}", file=sys.stderr)
        return

    ext = guess_ext(path)

    try:
        description = await describe(path)
    except Exception as e:
        print(f"SKIP (model error: {e}): {path}", file=sys.stderr)
        return

    base = sanitize(description)

    # Prepend date if requested
    if use_date:
        base = f"{get_creation_date(path)} - {base}"

    dirpath = os.path.dirname(os.path.abspath(path))
    new_path = unique_path(dirpath, base, ext)

    if not dry_run:
        os.rename(path, new_path)
    print(f"{path} -> {new_path}")

async def run(paths: list[str], dry_run: bool, use_date: bool) -> None:
    for p in paths:
        await rename_one(p, dry_run=dry_run, use_date=use_date)

def main():
    args = sys.argv[1:]
    if "-h" in args or "--help" in args:
        print(HELP, end="")
        sys.exit(0)

    if not args:
        print("Usage: rename-screenshots.py [--dry-run] [--date] [--help] <file1> <file2> ...", file=sys.stderr)
        sys.exit(2)

    dry_run = False
    if "--dry-run" in args or "--dryrun" in args:
        dry_run = True
        args = [a for a in args if a not in ("--dry-run", "--dryrun")]

    use_date = False
    if "--date" in args:
        use_date = True
        args = [a for a in args if a != "--date"]

    available, reason = fm.SystemLanguageModel().is_available()
    if not available:
        print(f"Apple Intelligence model not available: {reason}", file=sys.stderr)
        sys.exit(1)

    asyncio.run(run(args, dry_run, use_date))

if __name__ == "__main__":
    main()

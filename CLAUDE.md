# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

mbox-extractor is a command-line tool that recursively scans directories for `.mbox` email archive files and extracts all attachments. It's a single-file Python application with minimal dependencies.

## Installation & Setup

Install the tool using uv:

```bash
uv tool install .
```

## Running the Tool

Extract attachments from all `.mbox` files in a directory:

```bash
mbox-extractor /path/to/search
```

Test during development by running the main.py module directly:

```bash
python main.py /path/to/test/directory
```

## Architecture

This is a single-file application (`main.py`) with a simple processing pipeline:

1. **File Discovery** (`find_mbox_files`): Recursively walks directory tree to find `.mbox` files
2. **Attachment Extraction** (`extract_attachments`): For each `.mbox` file:
   - Opens it as a mailbox using Python's `mailbox.mbox`
   - Iterates through all messages with a progress bar
   - Extracts attachments from each message
   - Saves attachments with sanitized, unique filenames
3. **Filename Handling**:
   - `sanitize_filename`: Removes illegal characters for safe filesystem names
   - Uniqueness is ensured by appending an 8-character MD5 hash of the file content

**Key Design Points:**
- Each `.mbox` file's attachments are saved to a folder with the same name as the `.mbox` file (without extension)
- Filenames are made unique using content-based hashing (MD5) to prevent overwriting duplicate filenames
- Progress display uses `tqdm` for visual feedback on large mailboxes

## Dependencies

- **tqdm**: Progress bar display
- Python standard library: `mailbox`, `email`, `hashlib`, `argparse`, `os`, `re`

## Project Configuration

- Built with `hatchling` as the build backend
- Entry point: `mbox-extractor` command → `main:main`
- Python 3.7+ required
- The `main.py` file is packaged in the wheel distribution

## Important Notes

- README.md must be kept up to date with any significant project changes
- The tool uses `email.policy.default` for modern email parsing
- The `get_unique_filepath` function at main.py:16 is deprecated (MD5-based uniqueness replaced it)

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

mbox-extractor is both a command-line tool and importable Python package that recursively scans directories for `.mbox` email archive files and extracts all attachments.

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

Test during development:

```bash
python -c "from mbox_extractor import extract_attachments; print('OK')"
```

## Architecture

The project is structured as a proper Python package:

```
mbox_extractor/
├── __init__.py      # Public API exports + CLI entry point (main())
└── core.py          # Core extraction logic
```

### Processing Pipeline

1. **File Discovery** (`find_mbox_files` in `core.py`): Recursively walks directory tree to find `.mbox` files
2. **Attachment Extraction** (`extract_attachments` in `core.py`): For each `.mbox` file:
   - Opens it as a mailbox using Python's `mailbox.mbox`
   - Iterates through all messages with a progress bar
   - Extracts attachments from each message
   - Saves attachments with sanitized, unique filenames
3. **Filename Handling**:
   - `sanitize_filename`: Removes illegal characters for safe filesystem names
   - Uniqueness is ensured by appending an 8-character MD5 hash of the file content

### Public API

The package exports these functions via `mbox_extractor/__init__.py`:
- `extract_attachments(mbox_file, output_dir, show_progress=True)` - Main extraction function
- `find_mbox_files(root_path)` - Generator yielding .mbox file paths
- `sanitize_filename(filename)` - Clean filenames for filesystem
- `main()` - CLI entry point

**Key Design Points:**
- Each `.mbox` file's attachments are saved to a folder with the same name as the `.mbox` file (without extension)
- Filenames are made unique using content-based hashing (MD5) to prevent overwriting duplicate filenames
- Progress display uses `tqdm` for visual feedback on large mailboxes
- `show_progress=False` can be used for headless/automated usage

## Dependencies

- **tqdm**: Progress bar display
- Python standard library: `mailbox`, `email`, `hashlib`, `argparse`, `os`, `re`

## Project Configuration

- Built with `hatchling` as the build backend
- Entry point: `mbox-extractor` command → `mbox_extractor:main`
- Python 3.12+ required
- Package auto-discovered from `mbox_extractor/` directory

## Important Notes

- README.md must be kept up to date with any significant project changes
- The tool uses `email.policy.default` for modern email parsing
- The `get_unique_filepath` function in `core.py` is deprecated (MD5-based uniqueness replaced it)

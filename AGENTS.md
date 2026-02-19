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
python -c "from mbox_extractor import extract_mbox; print('OK')"
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

The package exports a single function via `mbox_extractor/__init__.py`:

```python
def extract_mbox(mbox_path: str, output_dir: str | None = None, show_progress: bool = True) -> int:
    """
    Extract attachments from an mbox file.

    Args:
        mbox_path: Absolute path to the .mbox file
        output_dir: Optional output directory. If None, creates a directory
                    with the same name as the mbox file (without extension)
                    in the same location as the mbox file.
        show_progress: Whether to display progress bar (default: True)

    Returns:
        Number of attachments extracted
    """
```

**Usage Examples:**

```python
from mbox_extractor import extract_mbox

# Extract with default output directory (creates /path/to/file/ from /path/to/file.mbox)
count = extract_mbox("/path/to/file.mbox")

# Extract to custom output directory
count = extract_mbox("/path/to/file.mbox", output_dir="/custom/output")

# Headless/automated usage (no progress bar)
count = extract_mbox("/path/to/file.mbox", show_progress=False)
```

**Key Design Points:**
- By default, attachments are saved to a folder with the same name as the `.mbox` file (without extension)
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
- Internal functions in `core.py` (`extract_attachments`, `find_mbox_files`, `sanitize_filename`) are not part of the public API

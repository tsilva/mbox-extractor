<div align="center">
  <img src="logo.png" alt="mbox-extractor" width="512"/>

  # mbox-extractor

  [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
  [![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)

  **📬 Recursively extract all attachments from .mbox email archives with a single command**

</div>

## Features

- **Recursive scanning** - Finds all `.mbox` files in any directory tree
- **Safe filenames** - Sanitizes attachment names, removing illegal characters
- **No duplicates** - Uses content-based hashing to prevent overwrites
- **Progress display** - Visual progress bar for large mailboxes

## Quick Start

```bash
uv tool install mbox-extractor
```

```bash
mbox-extractor /path/to/emails
```

## Installation

### Using uv (recommended)

```bash
uv tool install mbox-extractor
```

### Using pip

```bash
pip install mbox-extractor
```

### From source

```bash
git clone https://github.com/tsilva/mbox-extractor.git
cd mbox-extractor
uv tool install .
pre-commit install
```

## Usage

Extract all attachments from `.mbox` files under a directory:

```bash
mbox-extractor /path/to/search
```

Attachments from each `.mbox` file are saved to a folder with the same name:

```
Found mbox: /emails/archive.mbox -> extracting to /emails/archive
Extracting archive.mbox: 100%|████████████████████| 500/500 [00:10<00:00, 48.5it/s]
Extracted 42 attachments to '/emails/archive'.
```

### How It Works

1. Recursively scans the given path for `.mbox` files
2. Opens each mailbox and iterates through all messages
3. Extracts attachments with sanitized, unique filenames
4. Saves them to a folder named after the source `.mbox` file

Filenames are made unique by appending an 8-character MD5 hash of the file content, preventing overwrites when multiple attachments share the same name.

## Programmatic Usage

You can also use mbox-extractor as a library in your Python code:

```python
from mbox_extractor import extract_attachments, find_mbox_files

# Find and process all .mbox files in a directory
for mbox_path in find_mbox_files("/path/to/emails"):
    extract_attachments(mbox_path, "/output/directory")

# Extract from a single .mbox file
extract_attachments("/path/to/archive.mbox", "/output/directory")

# Extract without progress bar (for scripts/automation)
count = extract_attachments("/path/to/archive.mbox", "/output", show_progress=False)
print(f"Extracted {count} attachments")
```

### Available Functions

| Function | Description |
|----------|-------------|
| `find_mbox_files(path)` | Recursively yields paths to all `.mbox` files |
| `extract_attachments(mbox_file, output_dir, show_progress=True)` | Extracts attachments, returns count |
| `sanitize_filename(filename)` | Removes illegal characters from filenames |

## Requirements

- Python 3.12+
- tqdm (installed automatically)

## License

[MIT](LICENSE)

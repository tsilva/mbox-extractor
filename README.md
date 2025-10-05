# 📦 mbox-extractor

<p align="center">
  <img src="logo.png" alt="Logo" width="400"/>
</p>

🔹 Effortlessly extract all attachments from .mbox files in any directory tree

## 📖 Overview

mbox-extractor is a command-line tool that recursively scans a directory for `.mbox` files and extracts all email attachments found within them. Each attachment is saved to a folder named after its source `.mbox` file, with filenames made unique using a short hash to prevent overwriting. This tool is ideal for archiving or analyzing email attachments in bulk.

Attachments are sanitized for safe filenames, and progress is displayed using a modern progress bar for large mailboxes.

## 🚀 Installation

```bash
uv tool install .
```

## 🛠️ Usage

Extract all attachments from `.mbox` files under a directory (recursively):

```bash
mbox-extractor /path/to/search
```

- Replace `/path/to/search` with the directory or file you want to scan.
- Attachments from each `.mbox` file will be saved in a folder named after the `.mbox` file (without the extension).
- Filenames are made unique by appending a short hash.

Example output:

```
Found mbox: /emails/archive.mbox -> extracting to /emails/archive
Extracting archive.mbox: 100%|████████████████████| 500/500 [00:10<00:00, 48.5it/s]
Extracted 42 attachments to '/emails/archive'.
```

## 📄 License

This project is licensed under the [MIT License](LICENSE).
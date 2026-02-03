"""mbox-extractor: Extract attachments from .mbox email archives.

This package provides both a CLI tool and a programmatic API for extracting
attachments from .mbox email archive files.

CLI Usage:
    mbox-extractor /path/to/search

Library Usage:
    from mbox_extractor import extract_attachments, find_mbox_files

    for mbox_path in find_mbox_files("/path/to/emails"):
        extract_attachments(mbox_path, "/output/dir")
"""

import argparse
import os

from .core import extract_attachments, find_mbox_files, get_unique_filepath, sanitize_filename

__all__ = [
    "extract_attachments",
    "find_mbox_files",
    "sanitize_filename",
    "get_unique_filepath",
    "main",
]


def main():
    """CLI entry point for mbox-extractor."""
    parser = argparse.ArgumentParser(
        description="Recursively extract attachments from all .mbox files under a given path."
    )
    parser.add_argument(
        "path",
        help="Root directory or file to search for .mbox files"
    )
    args = parser.parse_args()
    root_path = args.path

    for mbox_path in find_mbox_files(root_path):
        mbox_dir = os.path.splitext(mbox_path)[0]
        print(f"Found mbox: {mbox_path} -> extracting to {mbox_dir}")
        extract_attachments(mbox_path, mbox_dir)

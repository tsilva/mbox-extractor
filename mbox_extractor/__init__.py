"""mbox-extractor: Extract attachments from .mbox email archives.

This package provides both a CLI tool and a programmatic API for extracting
attachments from .mbox email archive files.

CLI Usage:
    mbox-extractor /path/to/search

Library Usage:
    from mbox_extractor import extract_mbox

    # Uses default output directory (same location as mbox file)
    count = extract_mbox("/path/to/file.mbox")

    # With custom output directory
    count = extract_mbox("/path/to/file.mbox", output_dir="/custom/output")
"""

import argparse
import os

from .core import extract_attachments, find_mbox_files

__all__ = ["extract_mbox"]


def extract_mbox(mbox_path: str, output_dir: str | None = None, show_progress: bool = True) -> int:
    """Extract attachments from an mbox file.

    Args:
        mbox_path: Absolute path to the .mbox file.
        output_dir: Optional output directory. If None, creates a directory
                    with the same name as the mbox file (without extension)
                    in the same location as the mbox file.
        show_progress: Whether to display progress bar (default: True).

    Returns:
        Number of attachments extracted.
    """
    if output_dir is None:
        output_dir = os.path.splitext(mbox_path)[0]
    return extract_attachments(mbox_path, output_dir, show_progress)


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

    for mbox_path in find_mbox_files(args.path):
        print(f"Found mbox: {mbox_path}")
        extract_mbox(mbox_path)

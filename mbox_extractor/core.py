"""Core extraction functions for mbox-extractor."""

import hashlib
import mailbox
import os
import re
from email import policy
from email.parser import BytesParser

from tqdm import tqdm


def sanitize_filename(filename):
    """Remove directories and illegal characters from a filename.

    Args:
        filename: The original filename to sanitize.

    Returns:
        A sanitized filename safe for filesystem use.
    """
    filename = re.sub(r'[\\/*?:"<>|]', "_", filename)
    filename = filename.replace("..", "")  # extra safety
    return os.path.basename(filename)


def get_unique_filepath(output_dir, filename):
    """Get a unique filepath (deprecated).

    This function is no longer needed with MD5-based disambiguation.
    Kept for backward compatibility.

    Args:
        output_dir: Directory where file will be saved.
        filename: The filename.

    Returns:
        Full path to the file.
    """
    return os.path.join(output_dir, filename)


def find_mbox_files(root_path):
    """Recursively yield paths to all .mbox files under root_path.

    Args:
        root_path: Directory to search for .mbox files.

    Yields:
        Paths to .mbox files found under root_path.
    """
    for dirpath, _, filenames in os.walk(root_path):
        for fname in filenames:
            if fname.lower().endswith('.mbox'):
                yield os.path.join(dirpath, fname)


def extract_attachments(mbox_file, output_dir, show_progress=True):
    """Extract all attachments from an mbox file.

    Args:
        mbox_file: Path to the .mbox file.
        output_dir: Directory to save extracted attachments.
        show_progress: Whether to show progress bar (default: True).

    Returns:
        Number of attachments extracted.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if show_progress:
        print(f"Starting extraction for: {mbox_file}")

    mbox = mailbox.mbox(mbox_file, factory=lambda f: BytesParser(policy=policy.default).parse(f))
    attachment_count = 0

    total_msgs = len(mbox)
    iterator = tqdm(mbox, total=total_msgs, desc=f"Extracting {os.path.basename(mbox_file)}") if show_progress else mbox

    for message in iterator:
        for part in message.iter_attachments():
            filename = part.get_filename()
            if filename:
                clean_name = sanitize_filename(filename)
                payload = part.get_payload(decode=True)
                # Append short MD5 digest to filename for uniqueness
                digest = hashlib.md5(payload).hexdigest()[:8]
                base, ext = os.path.splitext(clean_name)
                unique_name = f"{base}_{digest}{ext}"
                safe_path = os.path.join(output_dir, unique_name)

                with open(safe_path, 'wb') as f:
                    f.write(payload)
                attachment_count += 1

    if show_progress:
        print(f"Extracted {attachment_count} attachments to '{output_dir}'.")

    return attachment_count

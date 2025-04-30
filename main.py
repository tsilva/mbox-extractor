import mailbox
import os
import re
import hashlib
from email import policy
from email.parser import BytesParser
import argparse
from tqdm import tqdm

def sanitize_filename(filename):
    # Remove directories and illegal characters
    filename = re.sub(r'[\\/*?:"<>|]', "_", filename)
    filename = filename.replace("..", "")  # extra safety
    return os.path.basename(filename)

def get_unique_filepath(output_dir, filename):
    # This function is no longer needed with MD5-based disambiguation
    return os.path.join(output_dir, filename)

def find_mbox_files(root_path):
    """Recursively yield paths to all .mbox files under root_path."""
    for dirpath, _, filenames in os.walk(root_path):
        for fname in filenames:
            if fname.lower().endswith('.mbox'):
                yield os.path.join(dirpath, fname)

def extract_attachments(mbox_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Starting extraction for: {mbox_file}")
    mbox = mailbox.mbox(mbox_file, factory=lambda f: BytesParser(policy=policy.default).parse(f))
    attachment_count = 0

    # Get total number of messages for tqdm progress bar
    total_msgs = len(mbox)
    for idx, message in enumerate(tqdm(mbox, total=total_msgs, desc=f"Extracting {os.path.basename(mbox_file)}")):
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

                # Save file
                with open(safe_path, 'wb') as f:
                    f.write(payload)
                attachment_count += 1

    print(f"Extracted {attachment_count} attachments to '{output_dir}'.")

if __name__ == "__main__":
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

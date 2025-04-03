#!/usr/bin/env python3
"""
Main entry point for the music organizer.
"""

import argparse
import sys
from pathlib import Path

from music_organizer.config import setup_beets
from music_organizer.monitor import start_monitoring
from music_organizer.organizer import process_existing_albums


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Automatically organize music albums using beets."
    )
    
    parser.add_argument(
        "--unsorted-dir",
        type=str,
        default="~/Music/_unsorted",
        help="Directory to monitor for new albums (default: ~/Music/_unsorted)",
    )
    
    parser.add_argument(
        "--music-dir",
        type=str,
        default="~/Music",
        help="Base directory for organized music (default: ~/Music)",
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()
    
    # Ensure directories exist
    unsorted_dir = Path(args.unsorted_dir).expanduser()
    music_dir = Path(args.music_dir).expanduser()
    
    if not unsorted_dir.exists():
        print(f"Creating unsorted directory: {unsorted_dir}")
        unsorted_dir.mkdir(parents=True, exist_ok=True)
    
    if not music_dir.exists():
        print(f"Creating music directory: {music_dir}")
        music_dir.mkdir(parents=True, exist_ok=True)
    
    # Setup beets configuration and library
    lib = setup_beets()
    
    # Always process existing albums first
    print(f"Processing existing albums in {unsorted_dir}")
    processed_dirs = process_existing_albums(unsorted_dir, music_dir, lib)
    
    # Always start monitoring after processing existing albums
    print(f"Starting to monitor {unsorted_dir} for new albums")
    try:
        start_monitoring(unsorted_dir, music_dir, lib, processed_dirs)
    except KeyboardInterrupt:
        print("Monitoring stopped by user")
    except Exception as e:
        print(f"Error during monitoring: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
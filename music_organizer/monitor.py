"""
File system monitoring for the music organizer.
"""

import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from music_organizer.organizer import process_album


class AlbumHandler(FileSystemEventHandler):
    """Handler for file system events related to new albums."""
    
    def __init__(self, unsorted_dir, music_dir, lib, processed_dirs=None):
        """
        Initialize the album handler.
        
        Args:
            unsorted_dir: Directory to monitor for new albums.
            music_dir: Base directory for organized music.
            lib: Beets library.
            processed_dirs: Set of already processed directories.
        """
        self.unsorted_dir = Path(unsorted_dir)
        self.music_dir = Path(music_dir)
        self.lib = lib
        self.processed_dirs = processed_dirs or set()
    
    def on_created(self, event):
        """
        Handle directory creation events.
        
        Args:
            event: The file system event.
        """
        if event.is_directory:
            # Wait a bit to ensure all files are copied
            time.sleep(5)
            path = Path(event.src_path)
            if path not in self.processed_dirs:
                self.processed_dirs.add(path)
                process_album(path, self.music_dir, self.lib)
    
    def on_moved(self, event):
        """
        Handle directory move events.
        
        Args:
            event: The file system event.
        """
        dest_path = Path(event.dest_path)
        if dest_path.is_dir() and dest_path.parent == self.unsorted_dir:
            # Wait a bit to ensure all files are copied
            time.sleep(5)
            if dest_path not in self.processed_dirs:
                self.processed_dirs.add(dest_path)
                process_album(dest_path, self.music_dir, self.lib)


def start_monitoring(unsorted_dir, music_dir, lib, processed_dirs=None):
    """
    Start monitoring a directory for new albums.
    
    Args:
        unsorted_dir: Directory to monitor for new albums.
        music_dir: Base directory for organized music.
        lib: Beets library.
        processed_dirs: Set of already processed directories.
    """
    event_handler = AlbumHandler(unsorted_dir, music_dir, lib, processed_dirs)
    observer = Observer()
    observer.schedule(event_handler, str(unsorted_dir), recursive=False)
    
    print(f"Starting to monitor {unsorted_dir} for new albums")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
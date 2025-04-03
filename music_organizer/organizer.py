"""
Album organization functionality for the music organizer.
"""

import os
import shutil
from pathlib import Path

from beets.ui.commands import import_files

from music_organizer.utils import sanitize_filename


def get_album_artists(album):
    """
    Get a list of unique artists in an album.
    
    Args:
        album: Beets album object.
        
    Returns:
        list: List of unique artist names.
    """
    artists = set()
    
    # Add the album artist
    if album.albumartist and album.albumartist.lower() != "various artists":
        artists.add(album.albumartist)
    
    # Add individual track artists
    for item in album.items():
        if item.artist and item.artist.lower() != "various artists":
            artists.add(item.artist)
    
    return list(artists)


def format_artist_string(artists):
    """
    Format the artist string based on the number of artists.
    
    Args:
        artists: List of artist names.
        
    Returns:
        str: Formatted artist string.
    """
    if not artists:
        return "Unknown"
    
    if len(artists) >= 3:
        return "VA"
    
    return ", ".join(artists)


def organize_album(album, music_dir):
    """
    Organize an album based on its metadata.
    
    Args:
        album: Beets album object.
        music_dir: Base directory for organized music.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Extract metadata
        year = album.year
        album_name = album.album or "Unknown"
        label = album.label or "Unknown"
        
        # Get all unique artists in the album
        artists = get_album_artists(album)
        artist_string = format_artist_string(artists)
        
        # Log the artists found
        if len(artists) >= 3:
            print(f"Album has {len(artists)} artists, using 'VA' as artist name")
        else:
            print(f"Album has {len(artists)} artists: {', '.join(artists)}")
        
        # Sanitize filenames
        artist_string = sanitize_filename(artist_string)
        album_name = sanitize_filename(album_name)
        label = sanitize_filename(label)
        
        # Create the new folder name - include year only if it exists
        if year:
            new_folder_name = f"{year} {artist_string} - {album_name}"
        else:
            new_folder_name = f"{artist_string} - {album_name}"
        
        # Determine target directory - always use a label folder (even "Unknown")
        music_dir = Path(music_dir)
        target_dir = music_dir / label
        
        # Create label directory if it doesn't exist
        target_dir.mkdir(parents=True, exist_ok=True)
        print(f"Using label directory: {label}")
        
        # Get the path to the album
        album_path = Path(os.path.dirname(album.items()[0].path))
        target_path = target_dir / new_folder_name
        
        # Move the album to the target directory
        print(f"Moving album to: {target_path}")
        
        # Create target directory if it doesn't exist
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if target already exists
        if target_path.exists():
            print(f"Target directory already exists: {target_path}")
            # Append a number to make it unique
            i = 1
            while (target_path.parent / f"{new_folder_name} ({i})").exists():
                i += 1
            target_path = target_path.parent / f"{new_folder_name} ({i})"
            print(f"Using alternative path: {target_path}")
        
        # Move the album
        shutil.move(str(album_path), str(target_path))
        
        # Update the paths in the library
        for item in album.items():
            old_path = item.path
            rel_path = os.path.relpath(old_path, str(album_path))
            new_path = os.path.join(str(target_path), rel_path)
            item.path = new_path
            item.store()
        
        print(f"Album organized successfully: {new_folder_name}")
        return True
    except Exception as e:
        print(f"Error organizing album: {str(e)}")
        return False


def process_album(album_path, music_dir, lib):
    """
    Process a new album directory.
    
    Args:
        album_path: Path to the album directory.
        music_dir: Base directory for organized music.
        lib: Beets library.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    album_name = album_path.name
    
    # Import the album with beets
    try:
        # Import the album
        import_files(lib, [str(album_path)], quiet=True)
        print(f"Successfully imported {album_name} with beets")
        
        # Find the album in the library
        query = f"path:{album_path}"
        items = lib.items(query)
        
        if items:
            # Get the first item's album
            album = items[0].album
            if album:
                return organize_album(album, music_dir)
            else:
                print(f"Could not find album for {album_name}")
        else:
            # Try to find by album name
            query = f"album:{album_name}"
            items = lib.items(query)
            if items:
                album = items[0].album
                if album:
                    return organize_album(album, music_dir)
                else:
                    print(f"Could not find album for {album_name}")
            else:
                print(f"Could not find imported album in library")
    except Exception as e:
        print(f"Error importing {album_name}: {str(e)}")
    
    return False


def process_existing_albums(unsorted_dir, music_dir, lib):
    """
    Process existing albums in the unsorted directory.
    
    Args:
        unsorted_dir: Directory containing unsorted albums.
        music_dir: Base directory for organized music.
        lib: Beets library.
        
    Returns:
        set: Set of processed directory paths.
    """
    processed_dirs = set()
    
    # Check if there are any directories to process
    entries = list(os.scandir(unsorted_dir))
    dirs = [entry for entry in entries if entry.is_dir()]
    
    if not dirs:
        print(f"No existing albums found in {unsorted_dir}")
        return processed_dirs
    
    print(f"Found {len(dirs)} album(s) to process")
    
    for entry in dirs:
        path = Path(entry.path)
        processed_dirs.add(path)
        print(f"Processing album: {path.name}")
        success = process_album(path, music_dir, lib)
        if success:
            print(f"Successfully processed album: {path.name}")
        else:
            print(f"Failed to process album: {path.name}")
    
    print(f"Finished processing {len(dirs)} existing album(s)")
    return processed_dirs
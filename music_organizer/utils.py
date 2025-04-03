"""
Utility functions for the music organizer.
"""


def sanitize_filename(filename):
    """
    Sanitize a filename to be safe for all file systems.
    
    Args:
        filename: The filename to sanitize.
        
    Returns:
        str: The sanitized filename.
    """
    # Replace invalid characters
    for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
        filename = filename.replace(char, '')
    
    # Replace multiple spaces with a single space
    filename = ' '.join(filename.split())
    
    # Trim leading/trailing spaces
    filename = filename.strip()
    
    # Ensure we have a valid filename
    if not filename:
        filename = "unknown"
    
    return filename
import os
from pathlib import Path

from beets import config as beets_config
from beets.library import Library


def setup_beets():
    """
    Setup beets configuration and library.
    
    Returns:
        Library: Initialized beets library.
    """
    # Use the existing beets configuration
    config_path = os.path.expanduser("~/.config/beets/config.yaml")
    print(f"Using beets config: {config_path}")
    
    # Read beets configuration
    beets_config.read(config_path)
    
    # Initialize library
    library_path = beets_config["library"].as_filename()
    lib = Library(library_path)
    
    return lib
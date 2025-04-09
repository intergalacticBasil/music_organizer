import os
import shutil
from pathlib import Path
from beets import config as beets_config
import subprocess

def organize_music(unsorted_dir):
    """
    Organizes music from the _unsorted directory using beets.

    Args:
        unsorted_dir (str): Path to the folder containing newly downloaded albums.
    """
    unsorted_path = Path(unsorted_dir).expanduser()
    if not unsorted_path.exists():
        print(f"Error: Unsorted folder '{unsorted_path}' does not exist.")
        return

    print(f"Organizing music from: {unsorted_path}")

    # Run beets import command
    cmd = ["beet", "import", str(unsorted_path)]
    subprocess.run(cmd, check=True)

    print("Music organization complete!")

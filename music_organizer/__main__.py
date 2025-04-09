import argparse
from .organizer import organize_music

def main():
    parser = argparse.ArgumentParser(description="Organize music using beets.")
    parser.add_argument(
        "--unsorted-dir",
        default="~/Music/_unsorted",
        nargs="?",
        type=str,
        help="Path to the _unsorted music folder.",
    )
    
    args = parser.parse_args()
    organize_music(args.unsorted_dir)

if __name__ == "__main__":
    main()

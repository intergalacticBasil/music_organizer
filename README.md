# Music Organizer

A tool to automatically organize music albums using beets.

## Features

- Monitors a directory for new album folders
- Processes albums with beets to extract metadata
- Organizes albums with smart naming conventions:
  - For 1-2 artists: "Year Artist 1, Artist 2 - Album name" (year omitted if unknown)
  - For 3+ artists: "Year VA - Album name" (year omitted if unknown)
- Places albums in record label folders (uses "Unknown" if no label exists)

## Prerequisites

### Beets Configuration

This tool requires a beets configuration file at `~/.config/beets/config.yaml`. If you don't have one, create it with the following content:

```yaml
directory: ~/Music/
library: ~/Music/library.db
import:
  move: yes
  write: yes
  copy: no
  group_albums: yes
paths:
  default: $artist/$album%aunique{}/$track $title
  singleton: Non-Album/$artist/$title
  comp: Compilations/$album%aunique{}/$track $title
plugins: fetchart
fetchart:
  auto: yes
```

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install the package:
```pip install -e .```

## Usage

```music-organizer [options]```

When run, the tool will:

1. Process any existing albums in the unsorted directory
2. Start monitoring the directory for new albums

### Options

- `--unsorted-dir`: Directory to monitor for new albums (default: ~/Music/_unsorted)
- `--music-dir`: Base directory for organized music (default: ~/Music)

### Example

```bash
# Create the unsorted directory if it doesn't exist
mkdir -p ~/Music/_unsorted

# Run with default directories
music-organizer

# Or specify custom directories
music-organizer --unsorted-dir ~/Downloads/new_music --music-dir ~/MyMusic
```

## How It Works

1. The tool monitors the unsorted directory for new album folders
2. When a new folder is detected, it uses beets to import and tag the music
3. It then organizes the album with the following naming pattern:
  - For albums with 1-2 artists: "Year Artist 1, Artist 2 - Album name"
  - For albums with 3+ artists: "Year VA - Album name"
  - The year is omitted if it's unknown
4. Albums are placed in subdirectories based on their record label
  - If no label information is available, it uses "Unknown"

## Running as a Service

To run as a systemd service, create a file at `~/.config/systemd/user/music-organizer.service`:

```bash
[Unit]
Description=Music Library Organizer
After=network.target

[Service]
ExecStart=/path/to/venv/bin/music-organizer
Restart=on-failure
Environment=PATH=/usr/bin:/usr/local/bin

[Install]
WantedBy=default.target
```

Replace `/path/to/venv/bin/music-organizer` with the actual path to the executable. You can find this path by running:

```which music-organizer```

Enable and start the service:

```bash
systemctl --user enable music-organizer.service
systemctl --user start music-organizer.service
```

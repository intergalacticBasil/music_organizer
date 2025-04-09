# 🎵 Music Organizer

A tool to automatically organize music albums using **Beets**.


## Features

- Processes albums with **Beets** to extract accurate metadata
- Organizes albums into smart, clean folder structures using the following rule:
  ```
  $label/$year $albumartist - $album/$track $title
  ```
- Sorts albums into record label folders (uses `_` if no label exists)
- Embeds album artwork automatically
- Robust matching and tagging based on MusicBrainz metadata

## Prerequisites

### Beets Configuration

This tool requires a beets configuration file at `~/.config/beets/config.yaml`. If you don't have one, create it with the following content:

```yaml
directory: ~/Music
library: ~/Music/library.db

import:
  move: yes
  write: yes
  autotag: yes

paths:
  default: $label/$year $albumartist - $album/$track $title
  singleton: $label/$year $artist - $title/$track $title
  comp: $label/$year VA - $album/$track $title

plugins: embedart fetchart

fetchart:
  sources: filesystem coverart

embedart:
  auto: yes

match:
  strong_rec_thresh: 0.04
  medium_rec_thresh: 0.25
```

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install the requirements:
```bash
pip install -r requirements.txt
```
4. Install the package:
```pip install -e .```

## 🛠️ Usage

```bash
music-organizer [options]
```

### Options

| Option            | Description                                          | Default                  |
|-------------------|------------------------------------------------------|---------------------------|
| `--unsorted-dir`  | Directory to monitor for new albums                  | `~/Music/_unsorted`        |
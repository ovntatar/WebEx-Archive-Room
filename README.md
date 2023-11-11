# WebEx Room Message Archiver

This Python script archives messages from a specified Cisco WebEx room and downloads any associated files.

## Features
- Fetches and archives messages from a specified WebEx room.
- Downloads all associated files (e.g., images) from the messages.
- Generates a timestamped text file for the archived messages.
- Ensures safe and valid filenames for downloaded files.

## Prerequisites
- Python 3
- `requests` library
- Access to WebEx API and a valid API token

## Setup
1. Install Python 3 and `pip` if not already installed.
2. Install the `requests` library using `pip`:

3. Set your WebEx API token as an environment variable `W_TOKEN`.

## Usage
To run the script, navigate to the script's directory and run:

Replace `run.py` with the name of your script file if different.

The script will archive messages from the specified room in `archive_messages_in_room("Room-Name")`. Replace `"Room-Name"` with the name of your target WebEx room.

## License
[MIT](https://choosealicense.com/licenses/mit/)

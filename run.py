import requests
from datetime import datetime
import os
import re

BASE_URL = "https://api.ciscospark.com/v1"
TOKEN = os.environ['W_TOKEN']

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def valid_filename(filename):
    """Ensure the filename is valid by removing special characters."""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_file(url, filename):
    """Download a file from a given URL and save it locally."""
    filename = valid_filename(filename)
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        print(f"Error downloading the file: {response.json()}")

def archive_messages_in_room(room_name):
    """Archive messages from a specified room and download associated files."""
    # Get room ID based on the room name
    rooms_url = f"{BASE_URL}/rooms"
    response = requests.get(rooms_url, headers=headers)
    
    if response.status_code != 200:
        print("Error fetching rooms:", response.json())
        return

    room_id = None
    rooms = response.json().get("items", [])
    for room in rooms:
        if room['title'] == room_name:
            room_id = room['id']
            break

    if not room_id:
        print(f"Room named '{room_name}' not found.")
        return

    # Fetch messages in the room
    messages_url = f"{BASE_URL}/messages?roomId={room_id}&max=1000"
    messages_response = requests.get(messages_url, headers=headers)

    if messages_response.status_code != 200:
        print("Error fetching messages:", messages_response.json())
        return

    messages = messages_response.json().get("items", [])

    # Get current date and time for the filename
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d-%H%M%S')
    text_filename = f"archive_{room_name}-{formatted_time}.txt"

    # Archive messages in a text file and save images locally
    with open(text_filename, "w") as archive_file:
        for message in messages:
            sender_name = message.get('personEmail', 'Unknown')
            timestamp = message.get('created', 'Unknown timestamp')
            text = message.get('text', '[Non-text message]')
            file_urls = message.get('files', [])

            archive_file.write(f"{sender_name} ({timestamp}): {text}\n")

            for file_url in file_urls:
                file_extension = file_url.split('.')[-1]
                safe_timestamp = valid_filename(timestamp)
                image_filename = f"{room_name}_{safe_timestamp}.{file_extension}"
                download_file(file_url, image_filename)

    print(f"Messages from room '{room_name}' have been archived in '{text_filename}'.")

if __name__ == "__main__":
    archive_messages_in_room("Network-base")



import requests
from decouple import config

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")

# Eleven Labs
# Convert Text to Speech
def convert_text_to_speech(message):
    
    print("000")
    print(message)
    print("123")

    # Define Data (Body)
    body = {
        "text": message,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }


    # Define voice
    voice_alex = "Hiyp1TNgfRxLxx9wQzPz"

    # Constructing Headers and Endpoint
    headers = {"xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json", "accept": "audio/mpeg"}
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_alex}"

    # Send request
    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        return
    
    # Handle Response
    if response.status_code == 200:
        return response.content
    else:
        return
    
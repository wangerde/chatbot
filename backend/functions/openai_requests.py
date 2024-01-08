import openai
from openai import OpenAI
from decouple import config

client = OpenAI(api_key=config("OPEN_AI_KEY"), organization=config("OPEN_AI_ORG"))
from decouple import config

# Import custom functions
from functions.database import get_recent_messages

# Retrieve Enviornment Variables
# TODO: The 'openai.organization' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(organization=config("OPEN_AI_ORG"))'
# openai.organization = config("OPEN_AI_ORG")


# Open AI - Whisper
# Convert audio to text


def convert_audio_to_text(audio_file):
    try:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        message_text = transcript.text
        return message_text
    except Exception as e:
        print(e)
        return


# Open AI - Chatgpt
# Get Response to our Message
def get_chat_response(message_input):
    
    messages = get_recent_messages()
    user_message = {"role": "user", "content": message_input}
    messages.append(user_message)
    print(messages)

    try:
        response = client.chat.completions.create(model="gpt-4-1106-preview",
        messages=messages)
        message_text = response.choices[0].message.content
        print(message_text)
        return message_text
    except Exception as e:
        print(e)
        return
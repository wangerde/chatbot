# uvicorn main:app
# uvicorn main:app --reload

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

# Custom Function Imports
from functions.database import store_messages, reset_messages
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech


#Initiate App
app = FastAPI()


#CORS - Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5200",
    "http://localhost:5300",
    "http://localhost:5400",
    "http://localhost:3000"
]


#CORS - Origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Check Health
@app.get("/health")
async def check_health():
    return {"message": "healthy"}


# Reset Messages
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "conversation reset!"}


# Get audio
@app.post("/post-audio-get/")
async def post_audio(file: UploadFile = File(...)):

    # Get saved Audio
    # audio_input = open("luna-voice-test.mp3", "rb")

    # Save file from Front end
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    # Decode Audio
    message_decoded = convert_audio_to_text(audio_input)

    # Guard: Ensure message decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode audio")
    
    # Get ChatGPT Response
    chat_response = get_chat_response(message_decoded)

    # Guard: Ensure message is back
    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to chat response")

    # Store messages
    store_messages(message_decoded, chat_response)

    # Convert chat response to audio
    audio_output = convert_text_to_speech(chat_response)

    # Guard: Ensure eleven labs response
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get Eleven Labs audio response")
    
    # Create a generator that yilds chunks of data
    def iterfile():
        yield audio_output

    # Return audio File
    return StreamingResponse(iterfile(), media_type="application/octet-stream")




# Post bot response
# Note: Not playing in browser using post request



    # print("Hello World")
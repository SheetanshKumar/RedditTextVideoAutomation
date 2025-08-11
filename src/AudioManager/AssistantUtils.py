from gtts import gTTS
from . import AssistantConfig as ac
import os

def assistant_speaks(output, file):
    directory = os.path.dirname(file)
    if directory and directory not in ("/", os.path.expanduser("~")) and not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
        except PermissionError as e:
            print(f"Warning: Could not create directory {directory}: {e}")
            print(f"Attempting to save audio file directly: {file}")
            # If we can't create the directory, try saving to current directory
            file = os.path.basename(file)
        except Exception as e:
            print(f"Unexpected error creating directory {directory}: {e}")
            raise
    
    toSpeak = gTTS(text=output, lang='en-US', slow=False)
    toSpeak.save(file)
    print("assistant speaks: ", output)
    ac.LENGTH_SPOKEN = ac.LENGTH_SPOKEN + len(output)


# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "My First Project.json"
# from google.cloud import texttospeech
#
# def assistant_speaks(text, filename):
#     client = texttospeech.TextToSpeechClient()
#     synthesis_input = texttospeech.types.SynthesisInput(text=text)
#
#     voice = texttospeech.types.VoiceSelectionParams(
#         language_code='en-IN',
#         name=ConstantsText.google_wavenet_name,
#         ssml_gender=ConstantsText.google_wavenet_gender)
#
#     audio_config = texttospeech.types.AudioConfig(
#         audio_encoding=texttospeech.enums.AudioEncoding.MP3)
#
#     response = client.synthesize_speech(synthesis_input, voice, audio_config)
#
#     with open(filename, 'wb') as out:
#         out.write(response.audio_content)
#     print(text)
#     ac.length_spoken = ac.length_spoken + len(output)

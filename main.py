import os
import speech_recognition as sr
from google.cloud import translate_v2, texttospeech
from google.oauth2 import service_account
import sys


def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak in English...")

        # Adjust for ambient noise only once
        recognizer.adjust_for_ambient_noise(source)

        try:
            while True:
                # Continuously listen to the user
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)

                try:
                    # Perform the speech-to-text conversion
                    user_input_text = recognizer.recognize_google_cloud(audio, credentials_json='./api-keys/advance-stratum-409704-50ff1f2aa864.json')
                    print("User Input (English):", user_input_text)

                    # Translate the user input to Hindi
                    translated_text = translate_text(user_input_text)
                    print("Translated Text:", translated_text)

                    # Convert translated text to speech in Hindi
                    text_to_speech(translated_text)

                    print("Speech file 'output.wav' generated.")
                except sr.UnknownValueError:
                    print("Google Cloud Speech-to-Text could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Cloud Speech-to-Text service; {e}")
        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
        finally:
            print("Cleaning up resources.")
            sys.exit()


def translate_text(text, target_language='hi'):
    credentials = service_account.Credentials.from_service_account_file('./api-keys/advance-stratum-409704-8f6e8f9201b9.json')
    translate_client = translate_v2.Client(credentials=credentials)

    try:
        # Translate the text
        result = translate_client.translate(text, target_language=target_language)

        # Get the translated text
        translated_text = result['translatedText']
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return None


def text_to_speech(text, language_code='hi-IN', voice_name='hi-IN-Wavenet-B', output_folder='output_folder'):
    credentials = service_account.Credentials.from_service_account_file('./api-keys/advance-stratum-409704-5126d296bfa8.json')
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save the audio file inside the folder
    output_path = os.path.join(output_folder, f'output_{len(os.listdir(output_folder)) + 1}.wav')
    with open(output_path, 'wb') as out:
        out.write(response.audio_content)

    print(f"Speech file '{output_path}' generated.")


if __name__ == "__main__":
    speech_to_text()

from google.cloud import texttospeech

def google_TtS(msg):
    """Synthesizes speech from the input string of text or ssml.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/
    """

    # Instantiates a client
    client = texttospeech.TextToSpeechClient ()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput (text=msg)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams (
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig (
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech (synthesis_input, voice, audio_config)

    file_name = 'output.mp3'
    # The response's audio_content is binary.
    with open (file_name, 'wb') as out:
        # Write the response to the output file.
        out.write (response.audio_content)
        print ('Audio content written to file "output.mp3"')

    return file_name
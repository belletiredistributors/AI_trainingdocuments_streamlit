import speech_recognition as sr

# Create a recognizer object
r = sr.Recognizer()

# Function to perform voice-to-text conversion
def convert_speech_to_text():
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        # print("Speak something...")
        audio = r.listen(source)
    try:
        # Use Google Speech Recognition to convert speech to text
        text = r.recognize_google(audio)
        # print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand audio.")
    except sr.RequestError as e:
        print("Error occurred; {0}".format(e))
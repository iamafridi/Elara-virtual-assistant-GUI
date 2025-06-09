import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import wikipedia
import pyjokes

# Initialize speech recognizer and text-to-speech engine
listener = sr.Recognizer()
elara = pyttsx3.init()

# Set voice to female if available
voices = elara.getProperty('voices')
if len(voices) > 1:
    elara.setProperty('voice', voices[1].id)

# Speak out text
def talk(text):
    print("Elara:", text)
    elara.say(text)
    elara.runAndWait()

# Listen and return user's command
def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print("\n[Listening...]")
            listener.adjust_for_ambient_noise(source, duration=0.5)  # helps ignore background noise
            voice = listener.listen(source, timeout=5, phrase_time_limit=7)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'elara' in command:
                command = command.replace('elara', '').strip()
    except sr.WaitTimeoutError:
        print("[No speech detected]")
    except sr.UnknownValueError:
        print("[Could not understand audio]")
    except sr.RequestError:
        print("[Could not connect to Google Speech Recognition]")
    except Exception as e:
        print("[Error]:", e)
    return command

# Process and respond to the command
def run_elara():
    command = take_command()
    if not command:
        return  # skip if no command

    print("You said:", command)

    if 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"Current time is {time}")
    elif 'play' in command:
        song = command.replace('play', '').strip()
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)
    elif 'tell me about' in command:
        topic = command.replace('tell me about', '').strip()
        try:
            info = wikipedia.summary(topic, sentences=1)
            talk(info)
        except:
            talk("Sorry, I couldn't find information on that.")
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'date' in command:
        talk('Sorry vaiya, I am in another relation.')
    else:
        talk("I didn't get that, but let me search it for you.")
        pywhatkit.search(command)

# Run continuously
if __name__ == "__main__":
    talk("Hello! I am your voice assistant ELARA. Say 'Elara' followed by a command.")
    while True:
        run_elara()


# import speech_recognition as sr
# import pyttsx3
# import datetime
# import pywhatkit
# import wikipedia
# import pyjokes

# # Initialize speech recognizer and text-to-speech engine
# listener = sr.Recognizer()
# alexa = pyttsx3.init()

# # Set voice to female if available
# voices = alexa.getProperty('voices')
# if len(voices) > 1:
#     alexa.setProperty('voice', voices[1].id)

# # Speak out text
# def talk(text):
#     print("Alexa:", text)
#     alexa.say(text)
#     alexa.runAndWait()

# # Listen and return user's command
# def take_command():
#     command = ""
#     try:
#         with sr.Microphone() as source:
#             print("\n[Listening...]")
#             listener.adjust_for_ambient_noise(source, duration=0.5)  # helps ignore background noise
#             voice = listener.listen(source, timeout=5, phrase_time_limit=7)
#             command = listener.recognize_google(voice)
#             command = command.lower()
#             if 'alexa' in command:
#                 command = command.replace('alexa', '').strip()
#     except sr.WaitTimeoutError:
#         print("[No speech detected]")
#     except sr.UnknownValueError:
#         print("[Could not understand audio]")
#     except sr.RequestError:
#         print("[Could not connect to Google Speech Recognition]")
#     except Exception as e:
#         print("[Error]:", e)
#     return command

# # Process and respond to the command
# def run_alexa():
#     command = take_command()
#     if not command:
#         return  # skip if no command

#     print("You said:", command)

#     if 'time' in command:
#         time = datetime.datetime.now().strftime('%I:%M %p')
#         talk(f"Current time is {time}")
#     elif 'play' in command:
#         song = command.replace('play', '').strip()
#         talk(f"Playing {song}")
#         pywhatkit.playonyt(song)
#     elif 'tell me about' in command:
#         topic = command.replace('tell me about', '').strip()
#         try:
#             info = wikipedia.summary(topic, sentences=1)
#             talk(info)
#         except:
#             talk("Sorry, I couldn't find information on that.")
#     elif 'joke' in command:
#         talk(pyjokes.get_joke())
#     elif 'date' in command:
#         talk('Sorry vaiya, I am in another relation.')
#     else:
#         talk("I didn't get that, but let me search it for you.")
#         pywhatkit.search(command)

# # Run continuously
# if __name__ == "__main__":
#     talk("Hello! I am your voice assistant. Say 'Alexa' followed by a command.")
#     while True:
#         run_alexa()

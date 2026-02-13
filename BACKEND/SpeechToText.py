import speech_recognition as sr
import os
import mtranslate as mt
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage")

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["what", "where", "when", "who", "why", "whose", "which", "how", "whom", "can you", "what's", "how's", "can you"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

def SpeechRecognition():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 0.6
            audio = r.listen(source, timeout=5, phrase_time_limit=8)

        print("Recognizing...")
        query = r.recognize_google(audio, language=InputLanguage)
        print(f"User said: {query}")

        if InputLanguage and (InputLanguage.lower() == "en" or "en" in InputLanguage.lower()):
            return QueryModifier(query)
        else:
            return QueryModifier(UniversalTranslator(query))

    except sr.WaitTimeoutError:
        # No speech detected within timeout
        return ""

    except sr.UnknownValueError:
        # Speech was unintelligible
        return ""

    except sr.RequestError:
        # Google API/network issue
        return ""

    except ConnectionResetError:
        # Connection dropped by Google
        return ""

    except Exception as e:
        # Catch-all to prevent thread crash
        print("SpeechRecognition error:", e)
        return ""

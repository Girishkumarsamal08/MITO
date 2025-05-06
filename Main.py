from FRONTEND.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus
)
from BACKEND.Model import FirstLayerDMM
from BACKEND.RealtimeSearchEngine import RealtimeSearchEngine
from BACKEND.Automation import Automation
from BACKEND.SpeechToText import SpeechRecognition
from BACKEND.TextToSpeech import TextToSpeech
from BACKEND.Chatbot import ChatBot
from BACKEND.FileAccess import list_all_files
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os
from PyQt5.QtWidgets import QApplication
from WAKEWORD.wake_word import detect_wake_word
from threading import Thread

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")

DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
{Assistantname} : Hello {Username}, I am doing well. How are you? And How may I help you?'''

process_list = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

MEMORY_FILE = "Data/relationship_memory.json"

def start_assistant():
    print("Waking up Darling...")
    # call your GUI or assistant trigger here


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"preferences": {}, "history": [], "nickname": "Darling", "mood": "happy"}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)

def ShowDefaultChatIfNoChats():
    with open(r'Data/ChatLog.json', "r", encoding='utf-8') as file:
        if len(file.read()) < 5:
            with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as f:
                f.write("")
            with open(TempDirectoryPath('Response.data'), 'w', encoding='utf-8') as f:
                f.write(DefaultMessage)

def ReadChatLogJson():
    with open(r'Data/ChatLog.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"{Username} : {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"{Assistantname} : {entry['content']}\n"

    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    with open(TempDirectoryPath('Database.data'), "r", encoding='utf-8') as file:
        data = file.read()
    if data:
        with open(TempDirectoryPath('Response.data'), "w", encoding='utf-8') as file:
            file.write(data)

def handle_file_access():
    permission = input("Darling: Can I access all your files, love? (yes/no): ")
    if permission.strip().lower() == "yes":
        try:
            files = list_all_files("/Users")  # You can use '/' for full access
            print(f"Found {len(files)} files.")
            # You can perform file-related operations here
        except Exception as e:
            print(f"Error while accessing files: {e}")   
    else:
        print("Okay, I won't access anything for now.")

def InitialExecution(): 
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()
    handle_file_access()



def MainExecution():
    QueryFinal = None
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""
    Answer = ""
    SetAssistantStatus("Listening...")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username} : {Query}")
    SetAssistantStatus("Thinking...")
    Decision = FirstLayerDMM(Query)
    memory = load_memory()

    print(f"\nDecision : {Decision}\n")

    G = any(i.startswith("general") for i in Decision)
    R = any(i.startswith("realtime") for i in Decision)

    Mearged_query = " and ".join(
        " ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")
    )

    for queries in Decision:
        if "generate " in queries:
            ImageGenerationQuery = queries
            ImageExecution = True

    for queries in Decision:
        if not TaskExecution:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(Decision))
                TaskExecution = True

    if ImageExecution:
        with open(r"FRONTEND/Files/ImageGeneration.data", "w") as file:
            file.write(f"{ImageGenerationQuery},True")
        try:
            p1 = subprocess.Popen(['python3', r'BACKEND/ImageGeneration.py'],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  stdin=subprocess.PIPE, shell=False)
            process_list.append(p1)
        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")

    if G and R or R:
        SetAssistantStatus("Searching...")
        Answer = RealtimeSearchEngine(QueryModifier(Mearged_query))
        ShowTextToScreen(f"{Assistantname} : {Answer}")
        SetAssistantStatus("Answering...")
        TextToSpeech(Answer)
        return True
    else:
        for Queries in Decision:
            if "general" in Queries:
                SetAssistantStatus("Thinking...")
                QueryFinal = Queries.replace("general: ", "")
                Answer=ChatBot(QueryModifier(QueryFinal))
                SetAssistantStatus("Answering...")
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                Thread(target=TextToSpeech, args=(Answer, memory.get("mood", "neutral"))).start()
                return True
            elif "realtime" in Queries:
                SetAssistantStatus("Searching...")
                QueryFinal = Queries.replace("realtime ", "")
                Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                SetAssistantStatus("Answering...")
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                Thread(target=TextToSpeech, args=(Answer, memory.get("mood", "neutral"))).start()
                return True
            elif "exit" in Queries:
                Answer = "Okay, Bye!"
                SetAssistantStatus("Answering...")
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                Thread(target=TextToSpeech, args=(Answer, memory.get("mood", "neutral"))).start()
                os._exit(1)

                # Save user query to memory history
                memory["history"].append({
                "user": Username,
                "query": Query,
                "response": Answer,
})

                # Example: Update mood or preferences based on keywords
                if "i love you" in Query.lower():
                    memory["mood"] = "loved"
                elif "you are annoying" in Query.lower():
                    memory["mood"] = "sad"
                elif "you make me angry" in Query.lower():
                    memory["mood"] = "angry"
                elif "thank you" in Query.lower():
                    memory["mood"] = "happy"

                if "call me" in Query.lower():
                   try:
                       nickname = Query.lower().split("call me")[-1].strip().split()[0]
                       if nickname:
                         memory["nickname"] = nickname.capitalize()
                         Answer = f"Alright! I'll call you {nickname.capitalize()} from now on."
                   except:
                        Answer = "Sorry, I couldn't understand the nickname you want me to use."
                
                save_memory(memory)


def FirstThread():
    while True:
        if GetMicrophoneStatus() == "True":
            MainExecution()
        else:
            if GetAssistantStatus() != "Available...":
                SetAssistantStatus("Available...")
            sleep(0.1)

def SecondThread():
    import sys
    app = QApplication(sys.argv)
    window = GraphicalUserInterface()
    window.show()
    sys.exit(app.exec_())

# Correct main entry point
if __name__ == "__main__":
    print("[HEY DARLING] Starting wake word listener in background...")
    InitialExecution()
    threading.Thread(target=FirstThread, daemon=True).start()
    SecondThread()

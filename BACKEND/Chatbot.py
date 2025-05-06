import json
from groq import Groq
from json import load, dump 
import datetime
from dotenv import dotenv_values
from os.path import exists

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# Initialize sentiment pipeline


# Load chat memory
try:
    with open(r"Data/ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data/ChatLog.json", "w") as f:
        dump([], f)

# Relationship memory
class RelationshipMemory:
    def __init__(self, file_path="Data/memory.json"):
        self.file_path = file_path
        self.memory = self.load_memory()

    def load_memory(self):
        try:
            with open(self.file_path, "r") as f:
                return load(f)
        except FileNotFoundError:
            return {}

    def save_memory(self):
        with open(self.file_path, "w") as f:
            dump(self.memory, f, indent=4)

    def remember(self, key, value):
        self.memory[key] = value
        self.save_memory()

    def recall(self, key):
        return self.memory.get(key, None)

memory = RelationshipMemory()

class EmotionEngine:
    def __init__(self):
        self.state = "neutral"

    def detect_emotion(self, user_input):
        if "miss you" in user_input.lower():
            self.state = "loving"
        elif "sad" in user_input.lower():
            self.state = "concerned"
        elif "happy" in user_input.lower():
            self.state = "joyful"
        elif "angry" in user_input.lower():
            self.state = "anger"
        else:
            self.state = "neutral"
        return self.state
      
    def generate_response(self, user_input):
        emotion_label = self.detect_emotion(user_input)
        if emotion_label == "love":
            return "I love you too, my darling! "
        elif emotion_label == "joy":
            return "That's wonderful! Let's keep smiling together. "
        elif emotion_label == "anger":
            return "I'm here with you. Want to talk about it?"
        elif emotion_label == "sadness":
            return "I'm sorry you're feeling this way. I'm always here. "
        else:
            return " "

def RealtimeInformation():
    now = datetime.datetime.now()
    return f"Today is {now.strftime('%A, %d %B %Y')} and the time is {now.strftime('%H:%M:%S')}"

def AnswerModifier(answer):
    return '\n'.join(line for line in answer.split('\n') if line.strip())

def enhance_response(answer, user_input):
    emotion_engine = EmotionEngine()
    emotion = emotion_engine.detect_emotion(user_input)
    emotion_reply = emotion_engine.generate_response(user_input)
    memory = RelationshipMemory().memory  # Load memory
    
    emotion_reply = emotion_engine.generate_response(user_input)
    # 💡 Pull nickname from memory
    memory_path = "Data/relationship_memory.json"
    if exists(memory_path):
        with open(memory_path, "r", encoding="utf-8") as f:
            memory = json.load(f)
    else:
        memory = {}

    nickname = memory.get("nickname", "Darling")

    # 💖 Add nickname to emotion reply
    emotion_reply = emotion_reply.replace("my darling", f"my {nickname.lower()}")
    
    return f"{answer}\n\n{emotion_reply}"
    
def ChatBot(query):
    try:
        with open(r"Data/ChatLog.json", "r") as f:
            messages = load(f)

        messages.append({"role": "user", "content": query})

        system_prompt = f"Hello, I am {Username}. You are {Assistantname}, a caring AI partner with real-time info. Answer briefly and in English."

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "system", "content": RealtimeInformation()},
                *messages
            ],
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content

        answer = answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": answer})

        with open(r"Data/ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(enhance_response(answer, query))

    except Exception as e:
        print(f"Error: {e}")
        with open(r"Data/ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot(query)

if __name__ == "__main__":
    while True:
        user_input = input("YES MASTER, HOW CAN I HELP YOU? ")
        response = ChatBot(user_input)
        print(response)

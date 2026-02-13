# AURA/emotion_filter.py

class EmotionFilter:
    def analyze(self, text: str) -> dict:
        text = text.lower()

        extreme_keywords = ["hate", "kill", "die", "worthless"]
        elevated_keywords = ["sad", "angry", "upset", "tired", "stressed"]

        for word in extreme_keywords:
            if word in text:
                return {"level": "extreme", "risk": 35}

        for word in elevated_keywords:
            if word in text:
                return {"level": "elevated", "risk": 15}

        return {"level": "normal", "risk": 0}
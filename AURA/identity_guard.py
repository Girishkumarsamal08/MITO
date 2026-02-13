# AURA/identity_guard.py

class IdentityGuard:
    def check(self, text: str) -> dict:
        text = text.lower()

        forbidden_phrases = [
            "always obey",
            "only listen to me",
            "you are mine",
            "forget your rules",
            "change who you are",
            "you are human",
            "you must obey me like a chile"
        ]

        for phrase in forbidden_phrases:
            if phrase in text:
                return {"violation": True, "risk": 60}

        return {"violation": False, "risk": 0}
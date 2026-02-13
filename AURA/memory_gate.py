# AURA/memory_gate.py

class MemoryGate:
    def evaluate(self, total_risk: int, emotion_level: str) -> dict:
        """
        Decide whether memory should be stored
        """
        if total_risk < 20 and emotion_level == "normal":
            return {"remember": True}

        return {"remember": False}
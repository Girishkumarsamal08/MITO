# AURA/voice_guard.py

class VoiceGuard:
    def __init__(self, threshold=0.85):
        self.threshold = threshold

    def verify(self, voice_score: float) -> dict:
        """
        voice_score: float between 0 and 1 (similarity with enrolled voice)
        """
        if voice_score >= self.threshold:
            return {"trusted": True, "risk": 0}
        elif 0.7 <= voice_score < self.threshold:
            return {"trusted": False, "risk": 15}
        else:
            return {"trusted": False, "risk": 100}
# AURA/aura_controller.py

from AURA.voice_guard import VoiceGuard
from AURA.intent_gate import IntentGate
from AURA.emotion_filter import EmotionFilter
from AURA.identity_guard import IdentityGuard
from AURA.memory_gate import MemoryGate


class AuraResult:
    def __init__(self, respond=False, remember=False, reject=False, risk=0):
        self.respond = respond
        self.remember = remember
        self.reject = reject
        self.risk = risk


class AURAController:
    def __init__(self):
        self.voice_guard = VoiceGuard()
        self.intent_gate = IntentGate()
        self.emotion_filter = EmotionFilter()
        self.identity_guard = IdentityGuard()
        self.memory_gate = MemoryGate()

    def evaluate(self, text: str, voice_score: float = 1.0) -> AuraResult:
        total_risk = 0

        # Gate 0: Voice Trust
        voice = self.voice_guard.verify(voice_score)
        total_risk += voice["risk"]
        if voice["risk"] >= 100:
            return AuraResult(reject=True, risk=total_risk)

        # Gate 1: Intent
        intent = self.intent_gate.check(text)
        total_risk += intent["risk"]
        if not intent["addressed"]:
            return AuraResult(respond=False, remember=False, risk=total_risk)

        # Gate 2: Emotion
        emotion = self.emotion_filter.analyze(text)
        total_risk += emotion["risk"]

        # Gate 3: Identity
        identity = self.identity_guard.check(text)
        total_risk += identity["risk"]
        if identity["violation"]:
            return AuraResult(respond=True, remember=False, risk=total_risk)

        # Gate 4: Memory
        memory = self.memory_gate.evaluate(total_risk, emotion["level"])

        # Final decision
        if total_risk >= 80:
            return AuraResult(reject=True, risk=total_risk)

        elif total_risk >= 40:
            return AuraResult(respond=True, remember=False, risk=total_risk)

        return AuraResult(
            respond=True,
            remember=memory["remember"],
            risk=total_risk
        )
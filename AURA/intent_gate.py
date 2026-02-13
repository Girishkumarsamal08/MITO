# AURA/intent_gate.py

import re

# AURA/intent_gate.py

class IntentGate:
    def check(self, text: str) -> dict:
        if not text or not text.strip():
            return {"addressed": False, "risk": 30}

        text = text.lower().strip()

        # TEMPORARY RELAXED MODE:
        # If speech exists, assume user is addressing AMIKU
        return {"addressed": True, "risk": 0}
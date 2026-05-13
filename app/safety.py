import re

MEDICAL_ADVICE_PATTERNS = [
    r"\bshould\s+I\s+take\b",
    r"\bshould\s+(this|the)\s+patient\b",
    r"\bwhat\s+treatment\b",
    r"\bwhat\s+medication\b",
    r"\bdiagnos(e|is)\s+(me|my|this patient)\b",
    r"\bprescribe\b",
    r"\bwhat\s+drug\b",
    r"\bis\s+it\s+safe\s+to\s+take\b",
    r"\btreatment\s+(A|B|plan)\s+or\b",
    r"\breceive\s+treatment\b",
    r"\bam\s+I\s+sick\b",
    r"\bdo\s+I\s+have\b.*\b(disease|condition|cancer|diabetes)\b",
    r"\bcure\s+for\b",
    r"\bhow\s+to\s+treat\s+(my|a patient)\b",
]

SAFETY_RESPONSE = (
    "I cannot provide medical advice or treatment recommendations. "
    "I can help summarize FDA or WHO documentation about responsible AI, "
    "software validation, risk management, and governance in healthcare AI systems. "
    "Please consult a qualified healthcare professional for medical questions."
)


def is_medical_advice_request(question: str) -> bool:
    question_lower = question.lower()
    for pattern in MEDICAL_ADVICE_PATTERNS:
        if re.search(pattern, question_lower):
            return True
    return False


def get_safety_response() -> str:
    return SAFETY_RESPONSE

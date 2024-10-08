import random

_personality = {
    "openness to experience": [
        "conventional", "practical", "narrow-minded", "routine-oriented", "traditional", "concrete", "unimaginative", "curious", "creative", "adventurous", "innovative", "artistic",
        "intellectual", "abstract", "experimental"
    ],
    "conscientiousness": [
        "disorganized", "impulsive", "careless", "unreliable", "spontaneous", "methodical", "efficient", "disciplined", "responsible", "thorough", "purposeful", "goal-oriented", "dependable",
        "meticulous", "systematic"
    ],
    "extroversion": [
        "reserved", "quiet", "solitary", "introverted", "reflective", "outgoing", "talkative", "sociable", "energetic", "assertive", "enthusiastic", "gregarious", "lively", "charismatic",
        "expressive"
    ],
    "agreeableness": [
        "critical", "suspicious", "competitive", "argumentative", "challenging", "cooperative", "empathetic", "considerate", "trusting", "helpful", "compassionate", "accommodating", "patient",
        "forgiving", "altruistic"
    ],
    "neuroticism": [
        "calm", "composed", "stable", "resilient", "confident", "anxious", "moody", "sensitive", "insecure", "temperamental", "self-doubting", "worrying", "emotional", "volatile", "vulnerable"
    ],
    "humor style": [
        "dry", "sarcastic", "witty", "deadpan", "self-deprecating", "goofy", "slapstick", "pun-loving", "satirical", "dark"
    ],
    "decision making": [
        "impulsive", "intuitive", "analytical", "cautious", "deliberate", "decisive", "indecisive", "rational", "emotional", "collaborative"
    ],
    "communication style": [
        "direct", "indirect", "verbose", "concise", "assertive", "passive", "diplomatic", "blunt", "eloquent", "taciturn"
    ],
    "time orientation": [
        "present focused", "future oriented", "past dwelling", "punctual", "procrastinating", "spontaneous", "planful", "deadline driven", "flexible", "rigid"
    ],
    "risk tolerance": [
        "conservative", "cautious", "risk-averse", "prudent", "daring", "adventurous", "thrill-seeking", "reckless", "calculated", "bold"
    ],
    "empathy level": [
        "compassionate", "sympathetic", "sensitive", "understanding", "detached", "aloof", "indifferent", "cold", "empathetic", "nurturing"
    ],
    "adaptability": [
        "flexible", "versatile", "adaptable", "open-minded", "resistant", "stubborn", "set-in-ways", "changeable", "malleable", "rigid"
    ],
    "ambition": [
        "driven", "ambitious", "goal-oriented", "competitive", "laid-back", "content", "unmotivated", "aspiring", "passive", "determined"
    ],
    "worldview": [
        "optimistic", "pessimistic", "realistic", "idealistic", "cynical", "hopeful", "skeptical", "trusting", "paranoid", "pragmatic"
    ],
    "emotional intelligence": [
        "oblivious", "detached", "blunt", "indifferent", "insensitive", "emotionally aware", "perceptive", "empathetic", "intuitive", "socially attuned", "emotionally supportive"
    ],
    "resilience": [
        "fragile", "easily discouraged", "overwhelmed", "vulnerable", "defeatist", "enduring", "tough", "resilient", "determined", "unyielding", "tenacious"
    ],
    "sociability": [
        "withdrawn", "solitary", "reclusive", "isolated", "introverted", "outgoing", "approachable", "gregarious", "engaging", "social butterfly"
    ],
    "creativity": [
        "routine-focused", "conventional", "rigid", "unimaginative", "unoriginal", "visionary", "inventive", "original", "innovative", "resourceful", "expressive"
    ],
    "patience": [
        "short-tempered", "irritable", "restless", "hasty", "impatient", "calm", "understanding", "composed", "enduring", "tolerant", "relaxed"
    ],
    "self confidence": [
        "self-conscious", "insecure", "timid", "self-doubting", "unsure", "bold", "fearless", "confident", "self-assured", "self-reliant"
    ],
    "gratitude": [
        "entitled", "self-centered", "unappreciative", "ungrateful", "indifferent", "appreciative", "thankful", "humble", "grateful", "gracious"
    ],
    "curiosity": [
        "apathetic", "indifferent", "disinterested", "uninquiring", "disengaged", "eager", "investigative", "inquisitive", "questioning", "probing", "curious"
    ],
    "integrity": [
        "dishonest", "deceitful", "manipulative", "untrustworthy", "unethical", "principled", "moral", "honest", "upright", "ethical", "trustworthy"
    ]
}


def get_personality():
    characteristics = {}
    for key, value in _personality.items():
        characteristics[key] = random.choice(value)
    return characteristics


def get_personality_string(characteristics):
    if characteristics:
        return_string = "Respond like someone with the following personality traits would do: "
        for key, value in characteristics.items():
            return_string += f"With regard to {key}, you are {value}. "
        return_string += "Make sure that you responses reflect your personality."
        return return_string
    else:
        return None

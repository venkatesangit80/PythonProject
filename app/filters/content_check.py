# app/filters/content_check.py

from better_profanity import profanity

# Initialize the profanity filter
profanity.load_censor_words()

# A simple set of spam indicators (you can expand this)
SPAM_KEYWORDS = {"buy now", "free money", "click here", "subscribe", "earn $$$"}


def contains_profanity(text: str) -> bool:
    """
    Returns True if the text contains profanity.
    """
    return profanity.contains_profanity(text)


def is_spam(text: str) -> bool:
    """
    Returns True if the message appears to be spam.
    Heuristics include:
    - Length
    - Excessive repetition
    - Known spammy phrases
    """
    lower_text = text.lower()

    if len(text) > 1000:
        return True

    if any(keyword in lower_text for keyword in SPAM_KEYWORDS):
        return True

    words = lower_text.split()
    if len(set(words)) < len(words) / 4:  # too many repeated words
        return True

    return False
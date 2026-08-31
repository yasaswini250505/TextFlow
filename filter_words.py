# filter_words.py
# Filter stages: stop words, short words, duplicate sentences.


# Built-in English stopword list (no file needed)
STOPWORDS_EN = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "is", "are", "was", "were",
    "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "shall", "can",
    "this", "that", "these", "those", "i", "you", "he", "she", "it",
    "we", "they", "me", "him", "her", "us", "them", "my", "your",
    "his", "its", "our", "their", "what", "which", "who", "when",
    "where", "why", "how", "all", "each", "every", "both", "few",
    "more", "most", "other", "some", "such", "no", "not", "only",
    "same", "so", "than", "too", "very", "just", "about", "above",
    "after", "also", "as", "before", "between", "during", "into",
    "through", "under", "up", "while", "then", "now", "here", "there",
    "any", "if", "out", "well", "back", "still", "over", "even",
}


def remove_stopwords(text, lang="en", custom_stops=None, **kwargs):
    """
    Remove stopwords from text.

    Args:
        lang         : language code - currently only "en supported
        custom_stops : additional words to remove (list or set)
    """
    stops = STOPWORDS_EN.copy()
    if custom_stops:
        stops.update(set(w.lower() for w in custom_stops))
    
    words  = text.split()
    kept   = [w for w in words if w.lower().strip(".,!?;:") not in stops]
    return " ".join(kept)


def filter_short_words(text, min_length=2, **kwargs):
    """Remove words shorter than min_length characters."""
    words = text.split()
    kept  = [w for w in words if len(w.strip(".,!?;:")) >= min_length]
    return " ".join(kept)


def filter_long_words(text, max_length=30, **kwargs):
    """Remove words longer than max_length (e.g. garbled tokens)."""
    words = text.split()
    kept  = [w for w in words if len(w) <= max_length]
    return " ".join(kept)


def deduplicate_sentences(text, **kwargs):
    """
    Remove duplicate sentences preserving order of first appearance.
    Splits on '.', '!', '?' then reconstructs unique ones.
    """
    # Split into sentences on punctuation
    sentences = []
    current   = ""
    for ch in text:
        current += ch
        if ch in ".!?":
            s = current.strip()
            if s:
                sentences.append(s)
            current = ""
    if current.strip():
        sentences.append(current.strip())

    seen   = set()
    unique = []
    for s in sentences:
        key = s.lower().strip(".,!?;: ")
        if key and key not in seen:
            seen.add(key)
            unique.append(s)

    return " ".join(unique)


def remove_single_chars(text, **kwargs):
    """Remove lone single characters (not letters like 'I' or 'a')."""
    words = text.split()
    kept  = [w for w in words if len(w) > 1 or w.lower() in ("i", "a")]
    return " ".join(kept)
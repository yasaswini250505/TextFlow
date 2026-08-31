# normaliser.py
# Normalization stages: case, whitespaces, contractions, quotes.
# Only string methods and loops - no regex, no external imports.


# Full Englisg contraction map
CONTRACTIONS = {
    "don't"     : "do not", "doesn't" : "does not",
    "didn't"    : "did not", "won't" : "will not",
    "can't"     : "cannot", "couldn't" : "could not",
    "shouldn't" : "should not", "wouldn't" : "would not",
    "it's"      : "it is",       "i'm"       : "i am",
    "i've"      : "i have",      "i'll"      : "i will",
    "i'd"       : "i would",     "you're"    : "you are",
    "you've"    : "you have",    "you'll"    : "you will",
    "you'd"     : "you would",   "they're"   : "they are",
    "they've"   : "they have",   "they'll"   : "they will",
    "we're"     : "we are",      "we've"     : "we have",
    "we'll"     : "we will",     "that's"    : "that is",
    "there's"   : "there is",    "there're"  : "there are",
    "wasn't"    : "was not",     "weren't"   : "were not",
    "haven't"   : "have not",    "hasn't"    : "has not",
    "hadn't"    : "had not",     "isn't"     : "is not",
    "aren't"    : "are not",     "he's"      : "he is",
    "she's"     : "she is",      "what's"    : "what is",
    "who's"     : "who is",      "let's"     : "let us",
    "should've" : "should have", "could've"  : "could have",
    "would've"  : "would have",  "must've"   : "must have",
}

# Unicode smart quotes and special dashes to replace
UNICODE_REPLACEMENTS = {
    "\u2018": "'",   "\u2019": "'",
    "\u201c": '"',   "\u201d": '"',
    "\u2013": "-",   "\u2014": "--",
    "\u2026": "...", "\u00e9": "e",
    "\u00e0": "a",   "\u00fc": "u",
}


def to_lowercase(text, **kwargs):
    """Convert entire text to lowercase."""
    return text.lower()


def to_uppercase(text, **kwargs):
    """Convert entire text to uppercase."""
    return text.upper()


def to_titlecase(text, **kwargs):
    """
    Smart title case : capitalise first letter of each word
    but keep small connector words lowercase (unless first or last).
    """
    SMALL = {
        "a", "an", "the", "and", "but", "or", "for",
        "in", "on", "at", "to", "of", "with", "by",
    }
    words  = text.lower().split()
    result = []
    for i, word in enumerate(words):
        if i == 0 or i == len(words) - 1 or word not in SMALL:
            result.append(word.capitalize())
        else:
            result.append(word)
    return " ".join(result)


def strip_whitespace(text, **kwargs):
    """Remove leading / trailing whitespace and collapse internal spaces."""
    result = text.strip()
    while "  " in result:
        result = result.replace("  ", " ")
    return result


def normalise_unicode(text, **kwargs):
    """Replace common unicode special characters with ASCII equivalents."""
    result = text
    for original, replacement in UNICODE_REPLACEMENTS.items():
        result = result.replace(original, replacement)
    return result


def expand_contractions(text, **kwargs):
    """Expand English contractions.

    Strategy:
        Split into words.
        For each word, strip trailing punctuation, check CONTRACTIONS dict,
        reattach punctuation if it was not an apostrophe.
    """
    words  = text.split()
    result = []
    for word in words:
        base   = word
        suffix = ""

        # Preserve trailing punctuation that is not part of contraction
        if base and not base[-1].isalpha() and not base[-1] == "'":
            suffix = base[-1]
            base   = base[:-1]
            
        expanded = CONTRACTIONS.get(base.lower(), base)
        result.append(expanded + suffix)
    return " ".join(result)


def normalise_sentence_spacing(text, **kwargs):
    """
    Ensure exactly one space after sentence-ending punctuation.
    E.g. "Hello.World" -> "Hello. World"
    """
    result = ""
    for i, ch in enumerate(text):
        result += ch
        if ch in ".!?" and i + 1 < len(text) and text[i + 1].isalpha():
            result += " "
    return result
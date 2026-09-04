# analyser.py
# Analytics engine: readability, keyboards, sentiment, word stats.
import math


# ── Word statistics ───────────────────────────────────────────────────────────


def word_stats(text):
    """
    Compute word-level statistics for a text string.

    Returns a dict with: word count, unique words, avg length, longest word, shortest word, sentence count.
    """
    words     = text.split()
    sentences = max(1, sum(1 for ch in text if ch in ".!?"))

    if not words:
        return {
            "word_count"     : 0,         "unique_words" :0,
            "avg_word_len"   : 0,         "longest"      : "", "shortest" : "",
            "sentence_count" : sentences, "avg_sent_len" : 0,
        }

    clean_words = [w.strip(".,!?;:\"'") for w in words if w.strip(".,!?;:\"'")]
    lengths     = [len(w) for w in clean_words]

    return {
        "word_count"     : len(words),
        "unique_words"   : len(set(w.lower() for w in clean_words)),
        "avg_word_len"   : round(sum(lengths) / max(1, len(lengths)), 1),
        "longest"        : max(clean_words, key=len) if clean_words else "",
        "shortest"       : min(clean_words, key=len) if clean_words else "",
        "sentence_count" : sentences,
        "avg_sent_len"   : round(len(words) / sentences, 1),

    }


# ── Readability ───────────────────────────────────────────────────────────


def count_syllables(word):
    """
    Approximate syllable count for a word.

    Rules:
        Count vowel groups (consecutive vowels = one syllable).
        Subtract silent 'e' at end of word.
        Minimum 1 syllable per word.
    """
    word    = word.lower().strip(".,!?;:\"'")
    vowels  = "aeiou"
    count   = 0
    prev_v  = False

    for ch in word:
        is_v = ch in vowels
        if is_v and not prev_v:
            count += 1
        prev_v = is_v

    # Silent 'e' at end
    if word.endswith("e") and count > 1:
        count -= 1

    return max(1, count)


def flesch_reading_ease(text):
    """
    Compute Flesch Reading Ease score (0-100).

    Formula:
        206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)

    Score guide:
        90–100 : Very easy (5th grade)
        70–80  : Easy (6th grade)
        60–70  : Standard (7th grade)
        50–60  : Fairly difficult
        30–50  : Difficult
        0–30   : Very difficult
    """
    words     = text.split()
    sentences = max(1, sum(1 for ch in text if ch in ".!?"))
    syllables = sum(count_syllables(w) for w in words)
    n_words   = max(1, len(words))

    score = (
        206.835
        - 1.015  * (n_words / sentences)
        - 84.6   * (syllables / n_words)
    )
    return round(max(0.0, min(100.0, score)), 1)


def reading_level(score):
    """Return a reading level label from a Flesch score."""
    if score >= 90: return "Very Easy (5th grade)"
    if score >= 80: return "Easy (6th grade)"
    if score >= 70: return "Fairly Easy (7th grade)"
    if score >= 60: return "Standard (8th-9th grade)"
    if score >= 50: return "Fairly Difficult (10th-12th grade)"
    if score >= 30: return "Difficult (college level)"
    return "Very Difficult (professional)"


# ── Keyword density ───────────────────────────────────────────────────────────


def keyword_density(text, top_n=10, exclude_stops=True):
    """
    Compute keyword frequency and density (% of total words).

    Args:
        text : input string
        top_n : number of top keywords to return
        exclude_stops: if True, skip common stopwords

    Returns:
        list of (word, count, density_pct) tuples
    """
    STOPS = {
        "the","a","an","and","or","but","in","on","at","to",
        "for","of","with","by","is","are","was","were","be",
        "have","has","had","do","does","did","this","that",
        "i","you","he","she","it","we","they","not","so",
    }

    words     = text.lower().split()
    total     = len(words)
    freq      = {}

    for word in words:
        clean = word.strip(".,!?;:\"'()-")
        if not clean:
            continue
        if exclude_stops and clean in STOPS:
            continue
        if len(clean) < 2:
            continue
        freq[clean] = freq.get(clean, 0) + 1

    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    result = []
    for word, count in sorted_freq[:top_n]:
        density = round(count / max(1, total) * 100, 2)
        result.append((word, count, density))
    return result


# ── Sentiment ─────────────────────────────────────────────────────────────────


POSITIVE_WORDS = {
    "good","great","excellent","amazing","wonderful","fantastic","superb",
    "outstanding","perfect","love","best","awesome","brilliant","happy",
    "positive","helpful","easy","fast","smooth","reliable","clear",
    "effective","efficient","beautiful","impressive","powerful","simple",
    "clean","quick","strong","success","successful","improve","improved",
    "better","win","winning","enjoy","enjoyed","recommend","recommended",
    "innovative","smart","intelligent","creative","useful","valuable",
}

NEGATIVE_WORDS = {
    "bad","terrible","awful","worst","horrible","poor","disappointing",
    "slow","broken","useless","hate","difficult","hard","confusing",
    "error","bug","fail","failed","failure","problem","issue","crash",
    "annoying","frustrating","complex","complicated","ugly","weak",
    "missing","wrong","incorrect","false","negative","loss","losing",
    "waste","wasted","boring","dull","expensive","overpriced","defective",
}

NEGATION_WORDS = {"not", "no", "never", "barely", "hardly", "scarcely", "without"}


def analyse_sentiment(text):
    """
     Rule-based sentiment analysis.

    Strategy:
        1. Count positive and negative words.
        2. Check for negation words before each sentiment word.
            If negated positive -> flip to negative (and vice versa).
        3. Score = (pos - neg) / (pos + neg)
            Range: -1.0 (very negative) to +1.0 (very positive)
    """
    words     = text.lower().split()
    pos_count = 0
    neg_count = 0
    pos_found = []
    neg_found = []

    for i, word in enumerate(words):
        clean    = word.strip(".,!?;:\"'")
        is_neg   = (i > 0 and words[i - 1].strip(".,!?;:") in NEGATION_WORDS)
        in_pos   = clean in POSITIVE_WORDS
        in_neg   = clean in NEGATIVE_WORDS

        if in_pos and not is_neg:
            pos_count += 1
            pos_found.append(clean)
        elif in_pos and is_neg:
            neg_count += 1         # negated positive flips to negative

        if in_neg and not is_neg:
            neg_count += 1
            neg_found.append(clean)
        elif in_neg and is_neg:
            pos_count += 1         # negated negative flips to positive
        
    total = pos_count + neg_count
    if total == 0:
        score = 0.0
    else:
        score = round((pos_count - neg_count) / total, 4)

    label = (
        "Strongly Positive" if score >  0.6 else
        "Positive"          if score >  0.2 else
        "Slightly Positive" if score >  0.0 else
        "Neutral"           if score == 0.0 else
        "Slightly Negative" if score >  -0.2 else
        "Negative"          if score >  -0.6 else
        "Strongly Negative"
    )

    return {
        "score"          : score,
        "label"          : label,
        "positive_count" : pos_count,
        "negative_count" : neg_count,
        "positive_words" : pos_found[:5],
        "negative_words" : neg_found[:5],
    }


# ── Full analysis ─────────────────────────────────────────────────────────────


def analyse_text(original_text, processed_text):
    """
    Run all analytics on original and processed text.
    Returns a single dict witl all metrics.
    """
    fre_score = flesch_reading_ease(original_text)
    return {
        "original_stats" : word_stats(original_text),
        "processed_stats" : word_stats(processed_text),
        "readability" : {
            "score": fre_score,
            "level": reading_level(fre_score),
        },
        "keywords" : keyword_density(processed_text, top_n=10),
        "sentiment" : analyse_sentiment(original_text),
    }
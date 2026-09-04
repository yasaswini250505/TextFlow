# report.py
# Builds and prints the full TextFlow analysis report.
# Pure string formatting


WIDTH = 62


def divider(char='-'):
    return char * WIDTH


def section_header(title):
    return [f"\n{title}", divider()]


def header_box(pipeline_name, summary):
    lines = [
        "=" * WIDTH,
         "TextFlow — Text Analytics Report".center(WIDTH),
        "=" * WIDTH,
        f"  Pipeline      : {pipeline_name}",
        f"  Stages run    : {summary.get('stages_run', 0)}",
        f"  Input chars   : {summary.get('chars_before', 0):,}",
        f"  Output chars  : {summary.get('chars_after', 0):,}",
        f"  Chars removed : {summary.get('chars_removed', 0):,}"
        f"  ({summary.get('pct_reduced', 0)}%)",
        "=" * WIDTH,
    ]
    return lines


def format_pipeline_log(log):
    """Show what each stage did."""
    lines = section_header("PIPELINE STAGE LOG")
    lines.append(
        f" {'Stage':<25} {'Before':>7} {'After':>7} {'Removed':>8}"
    )
    lines.append(f"  {divider('-')}")
    for entry in log:
        removed_flag = " <" if entry["removed"] > 0 else ""
        lines.append(
            f" {entry['stage']:<25} "
            f" {entry['before']:>7,} "
            f" {entry['after']:>7,} "
            f" {entry['removed']:>8,}{removed_flag}"
        )
    return lines


def format_word_stats(label, stats):
    """Format word-level statistics block."""
    lines = section_header(f"WORD STATISTICS ({label})")
    lines.append(f" Word count      : {stats.get('word_count', 0):,}")
    lines.append(f" Unique words    : {stats.get('unique_words', 0):,}")
    lines.append(f" Sentence count  : {stats.get('sentence_count', 0)}")
    lines.append(f" Avg word length : {stats.get('avg_word_len', 0)} chars")
    lines.append(f" Avg sent length : {stats.get('avg_sent_len', 0)} words")
    lines.append(f" Longest word    : {stats.get('longest', '')}")
    lines.append(f" Shortest word   : {stats.get('shortest', '')}")
    return lines


def format_readability(readability):
    """Format readability section."""
    lines = section_header("READABILITY (Flesch Reading Ease)")
    score = readability.get("score", 0)
    level = readability.get("level", "")

    # Visual score bar
    filled = int(score / 100 * 30)
    bar    = "█" * filled + "░" * (30 - filled)

    lines.append(f"  Score   : {score} / 100")
    lines.append(f"  Level   : {level}")
    lines.append(f"  [{bar}]")
    lines.append("")
    lines.append("  Score guide:")
    lines.append("  90-100  Very Easy  (5th grade)")
    lines.append("  70-80   Easy        (6th-7th grade)")
    lines.append("  60-70   Standard    (8th-9th grade)")
    lines.append("  50-60   Fairly Difficult")
    lines.append("  30-50   Difficult   (college level)")
    lines.append("  0-30    Very Difficult")
    return lines


def format_keywords(keywords):
    """Format keyboard density table."""
    lines = section_header("KEYWORD DENSITY  (Top 10)")
    if not keywords:
        lines.append("  No keywords found.")
        return lines

    max_count = keywords[0][1] if keywords else 1
    lines.append(f"  {'Keyword':<20} {'Count':>6} {'Density':>8} Chart")
    lines.append(f"  {divider('-')}")

    for word, count, density in keywords:
        filled = int(count / max_count * 15)
        bar = "█" * filled + "░" * (15 - filled)
        lines.append(
            f"  {word:<20} {count:>6} {density:>7.2f}% {bar}"
        )
    return lines


def format_sentiment(sentiment):
    """Format sentiment analysis section."""
    lines = section_header("SENTIMENT ANALYSIS  (Rule-based)")
    score = sentiment.get("score", 0)
    label = sentiment.get("label", "Neutral")
    pos_c = sentiment.get("positive_count", 0)
    neg_c = sentiment.get("negative_count", 0)

    # Score bar: negative side(left) and positive side(right)
    mid    = 15
    filled = int(abs(score) * mid)
    if score >= 0:
        bar = "░" * mid + "█" * filled + "░" * (mid - filled)
    else:
        bar = "░" * (mid - filled) + "█" * filled + "░" * mid

    lines.append(f"  Score           : {score:>7} (range -1.0 to +1.0)")
    lines.append(f"  Label            : {label}")
    lines.append(f"  [{bar}]")
    lines.append(f"  Negative <──────────────────────> Positive")
    lines.append(f"\n  Positive signals: {pos_c}  words")
    lines.append(f"  Negative signals: {neg_c}  words")
    if sentiment.get("positive_words"):
        lines.append(f"  Top positive    : {sentiment['positive_words']}")
    if sentiment.get("negative_words"):
        lines.append(f"  Top negative    : {sentiment['negative_words']}")
    return lines


def format_text_preview(label, text, max_chars=200):
    """Show a truncated preview of the text."""
    lines = section_header(f"TEXT PREVIEW  ({label})")
    preview = text[:max_chars]
    if len(text) > max_chars:
        preview += "..."
    lines.append(f"  {preview}")
    return lines


def build_report(pipeline_name, log, summary, analytics, original_text, processed_text):
    """
    Assemble the complete TextFlow report as a single string.
    """
    lines = header_box(pipeline_name, summary)
    lines.extend(format_pipeline_log(log))
    lines.extend(format_text_preview("Original", original_text))
    lines.extend(format_text_preview("Processed", processed_text))
    lines.extend(format_word_stats("Original", analytics["original_stats"]))
    lines.extend(format_word_stats("Processed", analytics["processed_stats"]))
    lines.extend(format_readability(analytics["readability"]))
    lines.extend(format_keywords(analytics["keywords"]))
    lines.extend(format_sentiment(analytics["sentiment"]))
    return "\n".join(lines)
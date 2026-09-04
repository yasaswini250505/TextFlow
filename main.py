# main.py
# Run with: python main.py

from pipeline     import run_pipeline, build_stage, log_summary
from cleaner      import (remove_urls, remove_html_tags, remove_punctuation, remove_extra_spaces, remove_emails)
from normaliser   import (to_lowercase, strip_whitespace, expand_contractions, normalise_unicode)
from filter_words import (remove_stopwords, filter_short_words, deduplicate_sentences)
from analyser     import analyse_text
from reporter     import build_report


# ── Sample text — replace with any string you want to analyse ─────────────────
SAMPLE_TEXT = """
TextFlow is an amazing text processing pipeline built entirely with Python.
It doesn't use any external libraries — it can't rely on pandas or NLTK.
The system won't fail even with messy input like URLs (https://example.com) or HTML tags (<b>bold text</b> and <br/> line breaks).

The pipeline is modular, clean, and easy to extend. Each stage transforms the text independently.
You can add, remove, or reorder stages without breaking anything else.

Data engineers love modular systems because they're easier to debug and test.
The best software is built with clear boundaries between components.
This project demonstrates that excellent code doesn't need complex libraries.

I've built this to showcase real Python fundamentals — loops, functions,
data structures, and string processing — working together in a clean pipeline.
"""


# ── Define pipeline stages ────────────────────────────────────────────────────
# Each stage: (name, function, config_dict)
# Stages run left to right in the list.

STANDARD_PIPELINE = [
    build_stage("normalise_unicode",   normalise_unicode),
    build_stage("expand_contractions", expand_contractions),
    build_stage("remove_urls",         remove_urls),
    build_stage("remove_html",         remove_html_tags),
    build_stage("remove_emails",       remove_emails),
    build_stage("to_lowercase",        to_lowercase),
    build_stage("remove_punctuation",  remove_punctuation, keep=""),
    build_stage("remove_stopwords",    remove_stopwords, lang="en"),
    build_stage("filter_short",        filter_short_words, min_length=3),
    build_stage("dedup_sentences",     deduplicate_sentences),
    build_stage("strip_whitespace",    strip_whitespace),
]

LIGHT_PIPELINE = [
    build_stage("normalise_unicode",   normalise_unicode),
    build_stage("expand_contractions", expand_contractions),
    build_stage("remove_urls",         remove_urls),
    build_stage("remove_html",         remove_html_tags),
    build_stage("to_lowercase",        to_lowercase),
    build_stage("strip_whitespace",    strip_whitespace),
]

KEYWORD_PIPELINE = [
    build_stage("normalise_unicode", normalise_unicode),
    build_stage("remove_urls",         remove_urls),
    build_stage("remove_html",         remove_html_tags),
    build_stage("to_lowercase",        to_lowercase),
    build_stage("remove_punctuation",  remove_punctuation, keep=""),
    build_stage("remove_stopwords",    remove_stopwords, lang="en"),
    build_stage("filter_short",        filter_short_words, min_length=4),
    build_stage("strip_whitespace",    strip_whitespace),
]

AVAILABLE_PIPELINES = {
    "standard" : STANDARD_PIPELINE,
    "light"    : LIGHT_PIPELINE,
    "keyword"  : KEYWORD_PIPELINE,
}


def run_textflow(
    text          = SAMPLE_TEXT,
    pipeline_name = "standard",
):
    """
    Full TextFlow pipeline.

    Steps:
        1. Select pipeline stages
        2. Run each stage on the text in order
        3. Run analytics on original and processed text
        4. Build and print the report
    """
    print(f"\nTextFlow  |  Pipeline: '{pipeline_name}'")
    print("-" * 60)

    # Step 1 — Select stages
    stages = AVAILABLE_PIPELINES.get(pipeline_name, STANDARD_PIPELINE)
    print(f" Stages : {len(stages)}")
    for name, _, config in stages:
        cfg_str = f" config={config}" if config else ""
        print(f" → {name}{cfg_str}")

    # Step 2 — Run pipeline
    processed_text, log = run_pipeline(text, stages)
    summary             = log_summary(log)

    # Step 3 — Analytics
    analytics = analyse_text(text, processed_text)

    # Step 4 — Build and print report
    report = build_report(
        pipeline_name = pipeline_name,
        log = log,
        summary = summary,
        analytics = analytics,
        original_text = text,
        processed_text = processed_text,
    )
    print(report)
    return processed_text, analytics, report


if __name__ == "__main__":
    # Run with the standard pipeline
    run_textflow(
        text          = SAMPLE_TEXT,
        pipeline_name = "standard",
    )

    # Uncomment to try other pipelines:
run_textflow(pipeline_name="light")
run_textflow(pipeline_name="keyword")
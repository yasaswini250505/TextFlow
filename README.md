# TextFlow

> A configurable, dependency-free Python text-processing pipeline with built-in analytics.

TextFlow accepts raw text, runs a configurable sequence of processing stages, and returns cleaned text together with a detailed analytics report. It is designed as a lightweight demonstration of modular text processing using only the Python standard library.

## Overview

TextFlow separates text transformation from text analysis. You choose the stages you want to run, execute them in order, and receive visibility into how each stage changed the input.

The generated report includes:

- Pipeline stage-by-stage statistics
- Original and processed text previews
- Word and sentence statistics
- Flesch Reading Ease score
- Reading-level classification
- Keyword frequency and density
- Rule-based sentiment signals
- Character reduction summary

## Features

- Configurable multi-stage processing pipelines
- Reusable stage builder for custom transformations
- Unicode normalization and contraction expansion
- Lowercase, uppercase, and title-case transformations
- Whitespace cleanup and sentence-spacing normalization
- URL, email, HTML-tag, punctuation, digit, and special-character removal
- English stopword filtering
- Short-word and long-word filtering
- Duplicate line and duplicate sentence removal
- Original-versus-processed text analytics
- Flesch Reading Ease calculation
- Keyword density analysis with configurable result counts
- Rule-based sentiment analysis with negation handling
- Human-readable console reports
- Zero external dependencies

## Requirements

- Python 3.8 or newer
- No third-party packages are required

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/yasaswini250505/TextFlow.git
cd TextFlow
```

Optional: create and activate a virtual environment:

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

TextFlow uses only the Python standard library. The included requirements file documents the supported Python version, but there are no packages to install:

```bash
python -m pip install -r requirements.txt
```

## Quick Start

Run the built-in example:

```bash
python main.py
```

The example executes the standard pipeline and prints a complete text analytics report.

> **Note:** `main.py` also contains example calls for the `light` and `keyword` pipelines. Uncomment those calls if you want to run them as well.

## Basic Usage

The primary entry point is `run_textflow` in `main.py`:

```python
from main import run_textflow

text = """
TextFlow is a simple and powerful text processing tool.
It removes unnecessary content and reports useful analytics.
"""

processed_text, analytics, report = run_textflow(
    text=text,
    pipeline_name="standard",
)

print(processed_text)
print(analytics["readability"])
```

`run_textflow` returns:

1. `processed_text` — the final text after all configured stages run.
2. `analytics` — a dictionary containing statistics, readability, keywords, and sentiment results.
3. `report` — the complete formatted report as a string.

## Built-in Pipelines

TextFlow includes three predefined pipelines in `main.py`:

| Pipeline | Purpose |
| --- | --- |
| `standard` | Comprehensive cleaning, normalization, filtering, and duplicate-sentence removal. |
| `light` | Minimal cleanup while preserving more of the original text. |
| `keyword` | Prepares text for keyword analysis by removing noise, stopwords, and short words. |

Example:

```python
from main import run_textflow

processed_text, analytics, report = run_textflow(
    text="This is an example of text that needs to be analyzed.",
    pipeline_name="keyword",
)
```

If an unknown pipeline name is supplied, TextFlow falls back to the standard pipeline.

## Creating a Custom Pipeline

Each stage is represented as a tuple containing:

- A stage name
- A processing function
- A configuration dictionary

Use `build_stage` to create stages and `run_pipeline` to execute them:

```python
from pipeline import build_stage, run_pipeline
from cleaner import remove_urls, remove_extra_spaces
from normaliser import to_lowercase

custom_pipeline = [
    build_stage("remove_urls", remove_urls),
    build_stage("lowercase", to_lowercase),
    build_stage("clean_spaces", remove_extra_spaces),
]

processed_text, log = run_pipeline(
    "Visit https://example.com for more information.",
    custom_pipeline,
)

print(processed_text)
print(log)
```

A custom stage should accept a text string and return a transformed text string. Configuration values are passed to the stage as keyword arguments.

Example with configuration:

```python
from pipeline import build_stage
from filter_words import filter_short_words

stage = build_stage(
    "filter_short_words",
    filter_short_words,
    min_length=4,
)
```

## Available Processing Stages

### Cleaning Stages

Defined in `cleaner.py`:

- `remove_urls`
- `remove_html_tags`
- `remove_punctuation`
- `remove_digits`
- `remove_special_chars`
- `remove_extra_spaces`
- `duplicate_lines`
- `remove_emails`

### Normalization Stages

Defined in `normaliser.py`:

- `to_lowercase`
- `to_uppercase`
- `to_titlecase`
- `strip_whitespace`
- `normalise_unicode`
- `expand_contractions`
- `normalise_sentence_spacing`

### Filtering Stages

Defined in `filter_words.py`:

- `remove_stopwords`
- `filter_short_words`
- `filter_long_words`
- `deduplicate_sentences`
- `remove_single_chars`

## Analytics

Analytics are implemented in `analyser.py` and run against both the original and processed text where applicable.

### Word Statistics

TextFlow calculates:

- Total word count
- Number of unique words
- Sentence count
- Average word length
- Average sentence length
- Longest word
- Shortest word

### Readability

TextFlow calculates a Flesch Reading Ease score from 0 to 100 using an approximate syllable counter. It also assigns a reading-level label such as:

- Very Easy
- Easy
- Fairly Easy
- Standard
- Fairly Difficult
- Difficult
- Very Difficult

### Keyword Density

The keyword analyzer identifies frequent words, optionally excludes common English stopwords, and returns each keyword's count and percentage density.

```python
from analyser import keyword_density

keywords = keyword_density(
    "Python makes text processing simple and Python is easy to use.",
    top_n=5,
    exclude_stops=True,
)
```

### Sentiment Signals

Sentiment analysis is rule-based and uses built-in positive, negative, and negation word sets. It returns:

- Sentiment score from `-1.0` to `+1.0`
- Sentiment label
- Positive and negative signal counts
- Sample words that contributed to the result

The sentiment analyzer is intended as a lightweight signal rather than a replacement for a machine-learning or linguistic sentiment model.

## Pipeline Logging

Every stage records its effect on the text:

```python
{
    "stage": "remove_urls",
    "before": 120,
    "after": 98,
    "removed": 22,
}
```

Use `log_summary` to calculate an overall processing summary:

```python
from pipeline import log_summary

summary = log_summary(log)
print(summary)
```

The summary includes the number of stages run, input and output character counts, total characters removed, and percentage reduction.

## Project Structure

```text
TextFlow/
├── main.py             # Example entry point and built-in pipeline definitions
├── pipeline.py         # Pipeline execution, stage construction, and summaries
├── cleaner.py          # Cleaning and removal stages
├── normaliser.py       # Case, whitespace, Unicode, and contraction normalization
├── filter_words.py     # Stopword and word-level filtering stages
├── analyser.py         # Word statistics, readability, keywords, and sentiment
├── reporter.py         # Human-readable report generation
├── requirements.txt    # Runtime requirements
├── Output.txt          # Example generated output
└── .gitignore
```

## Example Report Sections

The generated report contains sections similar to:

```text
TextFlow — Text Analytics Report

PIPELINE STAGE LOG
------------------
TEXT PREVIEW (Original)
----------------------
TEXT PREVIEW (Processed)
------------------------
WORD STATISTICS (Original)
--------------------------
WORD STATISTICS (Processed)
---------------------------
READABILITY (Flesch Reading Ease)
---------------------------------
KEYWORD DENSITY (Top 10)
------------------------
SENTIMENT ANALYSIS (Rule-based)
-------------------------------
```

A complete sample report is available in [`Output.txt`](Output.txt).

## Design Principles

TextFlow follows a few straightforward design principles:

- **Modularity:** Each transformation is an independent function.
- **Configurability:** Pipelines can be reordered, reduced, or extended.
- **Transparency:** Each stage reports how it changed the text.
- **Minimal dependencies:** The project relies on the Python standard library.
- **Readable implementation:** Processing is implemented with ordinary functions, loops, string methods, and data structures.

## Limitations

- TextFlow currently focuses on English-oriented rules and built-in English stopwords.
- Readability scores depend on an approximate syllable-counting algorithm.
- Sentiment analysis is rule-based and may not understand context, sarcasm, or domain-specific language.
- URL, email, and HTML detection are intentionally lightweight and are not full standards-compliant parsers.
- The pipeline processes text in memory and does not currently provide streaming support for very large documents.
- The built-in parser and filters are not intended to replace specialized natural-language-processing libraries for production linguistic analysis.

## Development

When extending TextFlow:

1. Keep each new processing stage focused on one responsibility.
2. Make stage functions accept `text` and return transformed text.
3. Add optional behavior through keyword arguments.
4. Register reusable stages in a pipeline definition rather than embedding logic in the executor.
5. Keep reporting and analytics separate from text transformation.
6. Run the sample application after changes to verify report formatting and pipeline behavior.

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository.
2. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Implement and test your changes.
4. Run the example application:

   ```bash
   python main.py
   ```

5. Commit your changes with a clear message.
6. Push your branch and open a pull request.

Please keep contributions focused, documented, and consistent with TextFlow's modular, dependency-free design.

## License

No license file is currently included in this repository. Add an appropriate license before distributing or reusing TextFlow outside the permissions granted by the repository owner.

## Author

Created and maintained by [yasaswini250505](https://github.com/yasaswini250505).

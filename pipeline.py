# pipeline.py
# The pipeline executor. Runs a list of stage functions in sequence.
# Each stage takes a string and returns a transformed string.


def run_pipeline(text, stages):
    """
    Run a list of stage functions on text in order.

    Args:
        text   : the input string to process
        stages : list of (stage_name, stage_function, config_dict) tuples

    Returns:
        processed_text : the final string after all stages
        log            : list of dicts describing what each stage did
    """
    current = text
    log     = []

    for stage_name, stage_func, config in stages:
        print(f"Running stage: {stage_name}...")
        before  = len(current)
        current = stage_func(current, **config)
        after   = len(current)

        log.append({
            "stage"   : stage_name,
            "before"  : before,
            "after"   : after,
            "removed" : before - after,
        })
    
    return current, log


def build_stage(name, func, **config):
    """
    Helper to build a stage tuple cleanly.

    Usage:
        build_stage("lowercase", to_lowercase)
        build_stage("stopwords", remove_stopwords, lang="en")
    """
    return (name, func, config)


def log_summary(log):
    """
    Return a summary dict from the pipeline run log.
    """
    if not log:
        return {}

    total_removed = sum(entry["removed"] for entry in log)
    stages_run    = len(log)

    return {
        "stages_run"    : stages_run,
        "chars_before"  : log[0]["before"],
        "chars_after"   : log[-1]["after"],
        "chars_removed" : total_removed,
        "pct_reduced"   : round(total_removed / max(1, log[0]["before"]) * 100, 1),
    }
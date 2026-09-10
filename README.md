# NPR transcript analysis project

## Main finding

**Speakers tend to echo the language style of the person who spoke immediately before them.** When one speaker uses pronouns, articles, conjunctions, or hedge words such as “maybe” and “kind of,” the next speaker is more likely to use those same types of words. In short, the analysis finds linguistic alignment between adjacent speakers. The pattern is statistically reliable in 6 of the 8 planned tests, with the strongest association for articles, followed by hedges and conjunctions.

This repository contains a local NPR transcript analysis pipeline focused on sequential linguistic association and conversational alignment. 

## Project goal

The main research question is whether speakers become more likely to use a linguistic feature when the immediately preceding speaker used that feature. The project tests this using local NPR transcript data and a token-based feature dictionary.

## Core analysis

The main result is in the report at [reports/report.md](reports/report.md). The analysis measures sequential linguistic association across adjacent cross-speaker turns and compares observed association to an exact expected null baseline with bootstrap/permutation uncertainty.

This is exploratory linguistic analysis, not a causal claim about power, deference, or gender differences.

## What is in this repo

- [scraping/main.py](scraping/main.py): local scraping and transcript retrieval logic
- [analysis/guest_level_analysis.py](analysis/guest_level_analysis.py): builds a cleaned guest-level dataset from transcript HTML
- [analysis/thank_you_gender_correlation.py](analysis/thank_you_gender_correlation.py): supplementary gender-vs-thank-you script
- [data/guest_speaker_level.csv](data/guest_speaker_level.csv): cleaned speaker-level output used in the exploratory gender check
- [data/names.csv](data/names.csv): gender lookup used for the supplemental analysis
- [reports/report.md](reports/report.md): the main linguistic accommodation report

## Methods summary

### 1. Transcript collection
The workflow gathers NPR transcript HTML, extracts the transcript body, and parses speaker-turn structure.

### 2. Turn parsing
The parser isolates adjacent speech turns, removes boilerplate and empty paragraphs, and logs ambiguous or excluded cases.

### 3. Linguistic feature detection
The project tests feature presence for lexical categories such as pronouns, articles, conjunctions, and hedges using token-based matching.

### 4. Sequential association test
For each adjacent cross-speaker pair, the project compares:

- the probability that the reply contains the feature after a preceding feature
- the probability that the reply contains the feature after a preceding absence of the feature

This difference is the observed sequential association, with an exact null and bootstrap/permutation uncertainty.

### 5. Supplemental gender/thank-you check
A smaller exploratory script also combines speaker gender and thank-you usage. This is included as a supporting analysis, not the main project conclusion.

## Quick start

From the project root:

```bash
python analysis/thank_you_gender_correlation.py
```

To rebuild a cleaned dataset:

```bash
python analysis/guest_level_analysis.py
```

## Important interpretation

The main project is a linguistic accommodation study in NPR transcripts. It is not a production scraper and it is not causal evidence. The thank-you/gender script is supplementary, while the larger report is the primary result.

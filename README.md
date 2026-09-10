# NPR transcript analysis project

This repository contains a local NPR transcript analysis pipeline focused on linguistic accommodation and conversational alignment. The project includes the scraping and parsing workflow, a cleaned speaker-level dataset, and a report on sequential association between adjacent turns.

## Project goal

The main analysis asks whether speakers become more likely to use a linguistic feature when the immediately preceding speaker used that feature. The project tests this using local NPR transcript data and a simple token-based feature dictionary.

## Core analysis

The main result is in the report at [reports/report.md](reports/report.md). The project measures sequential linguistic association for feature classes such as:

- pronouns
- articles
- conjunctions
- hedges

It compares observed association to an exact expected null baseline and reports bootstrap/permutation uncertainty.

This is an exploratory linguistic analysis, not a causal claim about power, deference, or gender differences.

## What is in this repo

- [scraping/main.py](scraping/main.py): local scraping and transcript retrieval logic
- [analysis/guest_level_analysis.py](analysis/guest_level_analysis.py): builds a cleaned guest-level dataset from transcript HTML
- [analysis/thank_you_gender_correlation.py](analysis/thank_you_gender_correlation.py): simple gender vs thank-you correlation script
- [data/guest_speaker_level.csv](data/guest_speaker_level.csv): cleaned speaker-level output used for the gender/thank-you check
- [data/names.csv](data/names.csv): name lookup used for gender inference
- [data/responses.csv](data/responses.csv): earlier sample output
- [reports/report.md](reports/report.md): summary of the main linguistic accommodation analysis

## Methods summary

### 1. Transcript collection
The workflow gathers NPR transcript HTML, extracts the transcript body, and parses speaker-turn structure.

### 2. Turn parsing
The parser isolates adjacent speech turns, removes boilerplate and empty paragraphs, and logs ambiguous or excluded cases.

### 3. Linguistic feature detection
The project tests feature presence for lexical categories such as pronouns, articles, conjunctions, and hedges using token-based matching.

### 4. Sequential association test
For each adjacent cross-speaker pair, the code compares:

- the probability that the reply contains the feature after a preceding feature
- the probability that the reply contains the feature after a preceding absence of the feature

The difference is the observed association, with an exact null and bootstrap/permutation uncertainty.

### 5. Thank-you and gender check
A smaller exploratory analysis also combines speaker gender and whether a speaker says a thank-you phrase. This is included as a simple extension rather than the main project story.

## Quick start

From the project root:

```bash
python analysis/thank_you_gender_correlation.py
```

To rebuild the cleaned dataset:

```bash
python analysis/guest_level_analysis.py
```

## Important interpretation

The main project is a linguistic accommodation study in NPR transcripts. It is not a production scraper and it is not causal evidence. The thank-you/gender script is a supplementary analysis, while the larger report is the primary result.

This repo is intended to show a coherent local analysis pipeline with a real report, cleaned data, and a simple exploratory gender check rather than a raw dump of debugging scripts.

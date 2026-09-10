# NPR Scraping and Analysis Project

This repository contains the local NPR scraping pipeline, transcript parsing scripts, cleaned analysis outputs, and a reproducible correlation analysis for the thank-you and gender question.

## What is in here

- Scraping and collection scripts for NPR story links and transcripts
- Legacy transcript parsing and analysis scripts
- A cleaned guest-level transcript dataset
- A local corpus-analysis workflow for adjacent-turn linguistic association
- A small analysis script that combines gender and thank-you behavior for a simple correlation

## Key files

- [main.py](main.py): legacy scraper entry point
- [gender_function1.py](gender_function1.py): earlier gender logic
- [Get_one_text_and_analyze.py](Get_one_text_and_analyze.py): transcript analysis prototype
- [scraped_transcripts/guest_level_analysis.py](scraped_transcripts/guest_level_analysis.py): cleaned guest-level dataset builder
- [scraped_transcripts/guest_speaker_level.csv](scraped_transcripts/guest_speaker_level.csv): cleaned speaker-level output
- [scraped_transcripts/accommodation_corpus_results/report.md](scraped_transcripts/accommodation_corpus_results/report.md): full local corpus report
- [analysis/thank_you_gender_correlation.py](analysis/thank_you_gender_correlation.py): thank-you + gender correlation script

## Methods summary

### 1. Data collection
The scraping workflow starts from a list of NPR story URLs, opens each page, looks for a transcript link, fetches the transcript HTML, and extracts individual turns.

### 2. Transcript parsing
The parser identifies speaker labels and speech segments, strips page boilerplate, ignores empty paragraphs, and preserves adjacency across turns. It also retains metadata such as transcript ID and date when available.

### 3. Thank-you detection
The code checks for thank-you phrases such as:

- thank you
- thanks
- thank you so much
- thanks so much

This is encoded as a binary indicator (`1` if present, `0` otherwise).

### 4. Gender inference
Speaker names are reduced to first-name form and mapped via a name/gender lookup table. The project originally used a name-frequency file that compares male and female name counts; unknown names remain unresolved and are dropped from strict correlation analysis.

### 5. Analysis
The final analysis step combines:

- `gender` as a binary or categorical value
- `said_thank_you` as a binary indicator

It then computes a simple correlation between the two. This is an exploratory analysis and is not a causal claim.

## Quick start

From the project root:

```bash
python analysis/thank_you_gender_correlation.py
```

Or, if you want to regenerate the cleaned speaker dataset:

```bash
python scraped_transcripts/guest_level_analysis.py
```

## Important limitation

This is not a production-grade scraping system and it is not a causal study. The thank-you/gender correlation is descriptive and should be interpreted as exploratory evidence only.

## Repository status

This workspace was initialized as a local Git repository on the `npr-scrape-analysis` branch. A GitHub remote was not created here because no GitHub authentication or CLI tooling was available in this environment.

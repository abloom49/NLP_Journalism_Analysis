# NPR scraping and analysis report

## Project purpose

This project combines local NPR scraping, transcript parsing, and a simple analysis of whether speakers who say thank-you are more likely to be a particular gender.

## Data collection and parsing

The scraping workflow collects NPR story URLs, follows transcript links, extracts transcript HTML, and converts speech into speaker-turn records. The parser isolates turns, filters empty or boilerplate content, and keeps the relevant adjacent-turn structure for analysis.

## Thank-you detection

The thank-you logic checks for phrases such as:

- thank you
- thanks
- thank you so much
- thanks so much

This is converted into a binary variable, where `1` means the speaker appears to say thank-you and `0` otherwise.

## Gender inference

The project infers gender using a first-name lookup against a names file. Names are mapped to male/female categories where possible; unresolved names are treated as missing and removed from strict statistical comparisons.

## Analysis question

The question is whether there is a relationship between speaker gender and thank-you usage in the transcript data.

## Main result

The cleaned dataset was processed with a simple correlation between gender and the thank-you flag. The result from the local analysis was:

- correlation = -0.38005847503304596

This indicates a negative association in the local sample, meaning the observed pattern is the opposite of a strong female-higher-thank-you relationship, but the sample is small and the result should be interpreted cautiously.

## Interpretation

This is exploratory analysis, not causal inference. The project measures sequential association in transcript text rather than proving social or psychological effects. It is useful as a descriptive pilot and for method development, but it should not be treated as strong evidence of a general gender pattern.

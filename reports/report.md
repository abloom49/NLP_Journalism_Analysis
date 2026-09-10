# NPR corpus: sequential linguistic association

Analyzed 70,777 source records from a local NPR transcript CSV using read-only access. The source SHA-256 was identical before and after analysis.

36 exact normalized-text duplicate records were excluded analytically; 0 malformed/empty records and 5 unique records without parsed turns were excluded. The retained corpus contains 70,736 transcripts, 1,328,174 turns, and 1,005,194 adjacent cross-speaker pairs before feature-specific support restrictions.

## Results

Values below are percentage points; intervals are 95% whole-transcript bootstrap percentile intervals for excess association.

| Window | Feature | Pairs | Transcripts | Observed | Expected null | Excess [95% interval] | Holm p |
|---|---|---:|---:|---:|---:|---|---:|
| full | pronouns | 242,232 | 18,463 | 1.31 | 0.40 | 0.91 [0.55, 1.30] | 0.0040 |
| full | articles | 351,340 | 25,139 | 6.70 | 2.16 | 4.55 [4.23, 4.85] | 0.0040 |
| full | conjunctions | 362,848 | 26,977 | 4.37 | 1.57 | 2.80 [2.50, 3.11] | 0.0040 |
| full | hedges | 227,567 | 20,728 | 2.48 | -1.37 | 3.85 [3.57, 4.12] | 0.0040 |
| first20 | pronouns | 16,626 | 2,996 | 4.15 | 2.20 | 1.96 [0.99, 2.89] | 0.0040 |
| first20 | articles | 28,893 | 4,629 | 0.44 | 0.14 | 0.30 [-0.61, 1.17] | 0.5270 |
| first20 | conjunctions | 54,577 | 8,407 | 0.56 | 0.11 | 0.45 [-0.24, 1.21] | 0.5270 |
| first20 | hedges | 19,988 | 3,406 | 0.79 | -0.51 | 1.30 [0.41, 2.18] | 0.0300 |

6 of the eight planned comparisons have Holm-adjusted p < 0.05. The first20 window measures feature presence in exactly the first 20 tokens of both turns, requiring both to be at least 20 tokens long.

These are sequential associations, not evidence of causal accommodation, power, deference, gender differences, or a trained model. A large corpus reduces sampling noise but does not eliminate parsing errors, confounding or selection bias.

## Method

The CSV text field uses paragraph separators. The parser handles speaker labels, continuation paragraphs, mixed-case host/byline roles, title prefixes, and unique surname aliases from explicit labels. Unidentified speakers and suspicious unparsed labels break adjacency and are logged. Editorial paragraphs break adjacency, and clip turns remain excluded until a previously seen speaker returns or a music marker occurs.

Eligibility is fixed before inference: each transcript × ordered speaker-pair stratum needs at least 4 exchanges, at least 2 exposed and 2 unexposed preceding turns for the feature, and each comparison needs 2 contributing transcripts.

Observed association is defined as the difference between the probability of a reply feature after a preceding feature and the probability of the same reply feature after a preceding absence of that feature. The expected null substitutes the reply-positive fraction of its stratum, retaining interview and speaker-direction composition.

## Features

- pronouns: i, me, my, mine, myself, we, us, our, ours, ourselves, you, your, yours, yourself, yourselves, he, him, his, himself, she, her, hers, herself, it, its, itself, they, them, their, theirs, themselves
- articles: a, an, the
- conjunctions: and, but, or, nor, for, so, yet, because, although, though, while, if, unless
- hedges: maybe, perhaps, probably, possibly, apparently, seem, seems, somewhat, i think, i guess, sort of, kind of

## Interpretation

These estimates describe sequential linguistic association in a large local NPR transcript corpus. They do not establish accommodation as a causal process, power, deference, gender differences, or population-level effects. The language analysis is the primary result of this project.

A smaller exploratory script, included in this repo, also checks whether speaker gender is associated with saying thank-you. That script is supplemental and not the main project conclusion.

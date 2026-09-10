from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
TRANSCRIPT_DIR = ROOT
NAMES_PATH = ROOT.parent / 'names.csv'
OUTPUT_PATH = ROOT / 'guest_speaker_level.csv'


def load_gender_lookup(path: Path):
    """Recreate the earlier names-based gender logic without touching legacy scripts."""
    name_dict = {}
    with path.open('r', encoding='utf-8') as f:
        next(f, None)
        for line in f:
            line = line.strip()
            if not line:
                continue
            items = [x.strip() for x in line.split(',')]
            if len(items) < 3:
                continue
            boy = items[1].lower()
            girl = items[2].lower()
            if boy not in name_dict:
                name_dict[boy] = [0, 0]
            if girl not in name_dict:
                name_dict[girl] = [0, 0]

    with path.open('r', encoding='utf-8') as f:
        next(f, None)
        for line in f:
            line = line.strip()
            if not line:
                continue
            items = [x.strip() for x in line.split(',')]
            if len(items) < 3:
                continue
            count = int(items[0])
            boy = items[1].lower()
            girl = items[2].lower()
            name_dict[boy][0] = count
            name_dict[girl][1] = count
    return name_dict


def genderfinder(name: str, name_dict):
    if not name:
        return 'unknown'

    key = name.lower().strip().replace("'", "").replace('-', '')
    if key in name_dict:
        boys_count, girls_count = name_dict[key]
        if boys_count - girls_count < 0:
            return "m"
        if boys_count - girls_count > 0:
            return "f"
        return "unknown"

    # Fallback: keep the older name-list logic but with a better first-name extraction.
    # This preserves compatibility with the original project while improving real transcript matching.
    return 'unknown'


def normalize_speaker_label(label: str) -> str:
    label = re.sub(r'\s+', ' ', label).strip()
    label = label.replace('BYLINE', '').strip()
    label = label.replace('NPR', '').strip()
    return label


def extract_first_name(speaker_name: str) -> str:
    """Use the true first given name instead of the last token."""
    if not speaker_name:
        return ""

    cleaned = normalize_speaker_label(speaker_name)
    cleaned = cleaned.replace('"', '').replace("'", "")
    pieces = re.split(r'[\s\-]+', cleaned)

    title_words = {
        'PRESIDENT', 'DR', 'MR', 'MRS', 'MS', 'PROF', 'REV', 'SEN', 'SENATOR',
        'REP', 'REPRESENTATIVE', 'JUDGE', 'CHIEF', 'DEPUTY', 'DIRECTOR', 'EDITOR'
    }
    suffix_words = {'JR', 'SR', 'II', 'III', 'IV', 'V'}

    first_name = ""
    for piece in pieces:
        token = piece.strip(".,;:()[]{}\"").upper()
        if not token:
            continue
        if token in title_words:
            continue
        if token in suffix_words:
            continue
        if token.isdigit():
            continue
        first_name = token
        break

    return first_name


def parse_transcript_speaker_turns(html_text: str):
    """Extract speaker-turn rows in the form NAME: text from NPR transcript HTML."""
    soup = BeautifulSoup(html_text, 'lxml')

    transcript_container = None
    for selector in ['div.transcript.storytext', 'div.transcript', 'article', 'main']:
        transcript_container = soup.select_one(selector)
        if transcript_container:
            break

    if transcript_container is None:
        return []

    turns = []
    for paragraph in transcript_container.find_all('p'):
        text = ' '.join(paragraph.get_text(' ', strip=True).split())
        if not text:
            continue
        match = re.match(r'^([A-Z][A-Z0-9\'\-. ]{1,60})\s*:\s*(.*)$', text)
        if match:
            speaker = normalize_speaker_label(match.group(1))
            speech = match.group(2).strip()
            if speakable_speaker(speaker):
                turns.append({'speaker': speaker, 'text': speech})
    return turns


def speakable_speaker(speaker: str) -> bool:
    return bool(speaker) and len(speaker) >= 2 and not re.fullmatch(r'\d+', speaker)


def detect_host(speaker_turns):
    if not speaker_turns:
        return None
    counts = Counter(turn['speaker'] for turn in speaker_turns)
    if not counts:
        return None
    return counts.most_common(1)[0][0]


def transcript_text(html_text: str) -> str:
    soup = BeautifulSoup(html_text, 'lxml')
    for selector in ['div.transcript.storytext', 'div.transcript', 'article', 'main']:
        container = soup.select_one(selector)
        if container:
            return ' '.join(container.get_text(' ', strip=True).split())
    return ''


def infer_full_names_from_text(speaker_turns, html_text):
    """Find unique title-case full names used with surname-only speaker labels."""
    surname_labels = {
        turn['speaker'] for turn in speaker_turns if len(turn['speaker'].split()) == 1
    }
    text = transcript_text(html_text)
    inferred = defaultdict(set)
    for surname in surname_labels:
        pattern = re.compile(
            r"\b((?:[A-Z][a-z]+\s+){1,2}" + re.escape(surname.title()) + r")\b"
        )
        for match in pattern.finditer(text):
            candidate = re.sub(r'\s+', ' ', match.group(1)).strip()
            inferred[surname].add(candidate.upper())
    return inferred


def resolve_surname_only_labels(speaker_turns, html_text):
    """Merge surname-only labels with unique full names found in the transcript."""
    full_names_by_surname = defaultdict(set)
    for turn in speaker_turns:
        speaker = turn['speaker']
        parts = speaker.split()
        if len(parts) < 2:
            continue
        surname = re.sub(r'[^A-Z0-9\'-]', '', parts[-1]).upper()
        if surname in {'JR', 'SR', 'II', 'III', 'IV', 'V'} and len(parts) > 2:
            surname = re.sub(r'[^A-Z0-9\'-]', '', parts[-2]).upper()
        if surname:
            full_names_by_surname[surname].add(speaker)

    for surname, candidates in infer_full_names_from_text(speaker_turns, html_text).items():
        full_names_by_surname[surname].update(candidates)

    resolved = []
    for turn in speaker_turns:
        speaker = turn['speaker']
        if len(speaker.split()) != 1:
            resolved.append(turn)
            continue
        surname = re.sub(r'[^A-Z0-9\'-]', '', speaker).upper()
        candidates = full_names_by_surname.get(surname, set())
        if len(candidates) == 1:
            turn = {**turn, 'speaker': next(iter(candidates))}
        resolved.append(turn)
    return resolved


def contains_thank_you(text: str) -> int:
    lowered = text.lower()
    patterns = ['thank you', 'thanks', 'thank you so much', 'thanks so much', 'many thanks']
    for pat in patterns:
        if pat in lowered:
            return 1
    return 0


def build_guest_level_dataset(transcript_files):
    name_dict = load_gender_lookup(NAMES_PATH)
    rows = []

    for path in transcript_files:
        html_text = path.read_text(encoding='utf-8', errors='ignore')
        turns = parse_transcript_speaker_turns(html_text)
        if not turns:
            continue

        turns = resolve_surname_only_labels(turns, html_text)
        host = detect_host(turns)
        guest_turns = defaultdict(list)
        for turn in turns:
            speaker = turn['speaker']
            if host and speaker == host:
                continue
            guest_turns[speaker].append(turn['text'])

        for speaker, text_list in guest_turns.items():
            text_blob = ' '.join(text_list)
            first_name = extract_first_name(speaker)
            gender = genderfinder(first_name, name_dict)
            rows.append({
                'transcript_id': path.stem,
                'source': 'npr',
                'speaker_name': speaker,
                'first_name': first_name,
                'gender': gender,
                'said_thank_you': contains_thank_you(text_blob),
                'total_turns': len(text_list),
                'speaker_role': 'guest',
            })

    return rows


def main():
    transcript_files = sorted(TRANSCRIPT_DIR.glob('transcript_*.html'))
    rows = build_guest_level_dataset(transcript_files)

    with OUTPUT_PATH.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['transcript_id', 'source', 'speaker_name', 'first_name', 'gender', 'said_thank_you', 'total_turns', 'speaker_role'],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f'Wrote {len(rows)} guest-level rows to {OUTPUT_PATH}')
    for row in rows[:10]:
        print(row)


if __name__ == '__main__':
    main()

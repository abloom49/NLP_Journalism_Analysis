from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / 'scraped_transcripts' / 'guest_speaker_level.csv'


def load_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f'Missing dataset: {path}')
    df = pd.read_csv(path)
    return df


def build_gender_code(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    mapping = {
        'female': 1,
        'male': 0,
        'f': 1,
        'm': 0,
        'unknown': None,
        None: None,
        '': None,
    }
    out['gender_code'] = out['gender'].map(mapping)
    return out


def main() -> None:
    df = load_dataset(DATA_PATH)
    df = build_gender_code(df)

    valid = df.dropna(subset=['gender_code', 'said_thank_you']).copy()
    valid['said_thank_you'] = valid['said_thank_you'].astype(int)

    print(f'Total rows: {len(df)}')
    print(f'Rows kept for correlation: {len(valid)}')
    print(valid[['gender', 'said_thank_you', 'gender_code']].head(10).to_string(index=False))

    if len(valid) >= 2:
        corr = valid['gender_code'].corr(valid['said_thank_you'])
        print(f'Corr(gender_code, said_thank_you) = {corr}')
    else:
        print('Not enough rows for a valid correlation.')

    # Simple cross-tab for a quick readout
    ctab = pd.crosstab(valid['gender'], valid['said_thank_you'])
    print('\nCross-tab (gender x thank-you):')
    print(ctab)


if __name__ == '__main__':
    main()

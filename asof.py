"""Lab 16 provenance gate; fictional course data, standard library only.

Run: python asof.py
Optional probe: python asof.py --decision-date 2026-04-15
"""
import argparse
from dataclasses import dataclass
from datetime import date
import math

# Editable inputs: row number, ticker, month measured, publication date, price.
DECISION_DATE = '2026-03-31'
TABLE = [
    (1, 'AAA', '2026-01', '2026-02-10', 101.0),
    (2, 'AAA', '2026-02', '2026-03-10', 104.0),
    (3, 'AAA', '2026-03', '2026-04-10', 109.0),
    (4, 'AAA', '2026-02', '2026-03-25', 103.0),
    (5, 'BBB', '2026-01', '2026-02-10', 98.0),
    (6, 'BBB', '2026-02', '2026-03-10', 97.0),
    (7, 'BBB', '2026-02', '2026-03-10', 97.0),
    (8, 'BBB', '2026-03', '2026-04-10', 92.0),
    (9, 'CCC', '2026-01', '2026-02-10', 110.0),
    (10, 'CCC', '2026-02', '2026-04-05', 112.0),
    (11, '', '2026-02', '2026-03-10', 99.0),
    (12, 'CCC', '2026-02', '2026-03-10', 111.0),
]


@dataclass(frozen=True)
class Record:
    row: int
    ticker: str
    month: str
    published: date
    price: float


def parse_table(table):
    records = []
    ids = set()
    for row, ticker, month, published, price in table:
        if row in ids:
            raise ValueError(f'Duplicate row identifier: {row}')
        ids.add(row)
        date.fromisoformat(month + '-01')
        if not math.isfinite(price) or price <= 0:
            raise ValueError(f'Row {row}: price must be finite and positive.')
        records.append(Record(row, ticker, month, date.fromisoformat(published), price))
    return records


def clean_records(records):
    """Rules 1 and 2; row identifiers are metadata, not duplicate-key fields."""
    missing = [r for r in records if not r.ticker.strip()]
    retained, duplicates, seen = [], [], set()
    for record in records:
        if not record.ticker.strip():
            continue
        key = (record.ticker, record.month, record.published, record.price)
        if key in seen:
            duplicates.append(record)
        else:
            seen.add(key)
            retained.append(record)
    return retained, [('Quarantined: missing ticker', missing), ('Removed: exact duplicate', duplicates)]


def latest_vintages(records):
    """One record per ticker/month, retaining the latest publication."""
    latest = {}
    for record in records:
        key = (record.ticker, record.month)
        previous = latest.get(key)
        if previous is not None and record.published == previous.published and record.price != previous.price:
            raise ValueError(f'Conflicting same-date values for {key}; source clarification needed.')
        if previous is None or record.published > previous.published:
            latest[key] = record
    panel = sorted(latest.values(), key=lambda r: (r.ticker, r.month))
    kept = {record.row for record in panel}
    removed = [record for record in records if record.row not in kept]
    return panel, removed


def asof_panel(records, cutoff):
    cleaned, audit = clean_records(records)
    late = [r for r in cleaned if r.published > cutoff]
    knowable = [r for r in cleaned if r.published <= cutoff]
    audit.append(('Removed: publication after cutoff', late))
    panel, superseded = latest_vintages(knowable)
    audit.append(('Removed: superseded vintage', superseded))
    return panel, audit


def naive_panel(records):
    # Missing identifiers and duplicates remain invalid; only timing is ignored.
    cleaned, _ = clean_records(records)
    return latest_vintages(cleaned)[0]


def previous_month(month):
    year, number = map(int, month.split('-'))
    return f'{year - 1}-12' if number == 1 else f'{year}-{number - 1:02d}'


def signals(panel):
    groups = {}
    for record in panel:
        groups.setdefault(record.ticker, {})[record.month] = record
    result = {}
    for ticker, months in sorted(groups.items()):
        latest_month = max(months)
        earlier = previous_month(latest_month)
        change = None
        if earlier in months:
            change = (months[latest_month].price / months[earlier].price - 1) * 100
        result[ticker] = dict(month=latest_month, previous_month=earlier, percent=change)
    return result


def signal_text(signal):
    if signal is None:
        return 'N/A (no observations)'
    if signal['percent'] is None:
        return f"N/A (missing {signal['previous_month']} price; latest {signal['month']})"
    return f"{signal['percent']:+.2f}% ({signal['month']})"


def zero_coupon_yield(price):
    return (100 / price - 1) * 100


def sanity_flags(record, panel):
    """Separate classroom checks; never silently change the provenance panel."""
    flags = []
    if zero_coupon_yield(record.price) < 0:
        flags.append('negative yield (classroom flag)')
    rank = {'AAA': 0, 'BBB': 1, 'CCC': 2}
    if record.ticker in rank:
        for other in panel:
            if (other.month == record.month and other.ticker in rank
                    and rank[record.ticker] > rank[other.ticker] and record.price >= other.price):
                flags.append(f'not priced below safer {other.ticker}')
    return '; '.join(flags) or 'none'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--decision-date', default=DECISION_DATE)
    args = parser.parse_args()
    try:
        cutoff = date.fromisoformat(args.decision_date)
        records = parse_table(TABLE)
        panel, audit = asof_panel(records, cutoff)
        naive = naive_panel(records)
    except ValueError as error:
        parser.error(str(error))
    print(f'Lab 16 fictional training data | Decision date: {cutoff}')
    print(f'Input rows: {len(records)}')
    for label, removed in audit:
        ids = ', '.join(str(r.row) for r in removed) or 'none'
        print(f'{label}: {len(removed)} row(s); row IDs: {ids}')
    print(f"As-of panel: {len(panel)} row(s); row IDs: {', '.join(str(r.row) for r in panel) or 'none'}")
    print('\nAS-OF PANEL')
    print('Row | Ticker | Month | Published | Price')
    for r in panel:
        print(f'{r.row} | {r.ticker} | {r.month} | {r.published} | {r.price:.1f}')
    actual, hindsight = signals(panel), signals(naive)
    print('\nSIGNALS: month-over-month price changes')
    for ticker in sorted(set(actual) | set(hindsight)):
        print(f'{ticker}: as-of {signal_text(actual.get(ticker))} | naive {signal_text(hindsight.get(ticker))}')
    print('\nSEPARATE SANITY REVIEW: not applied to the four-rule panel')
    for r in panel:
        print(f'Row {r.row}: yield {zero_coupon_yield(r.price):+.2f}% | {sanity_flags(r, panel)}')


if __name__ == '__main__':
    main()

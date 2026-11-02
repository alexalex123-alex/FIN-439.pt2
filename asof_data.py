"""FRED/ALFRED downloads and comparison logic; no API key needed."""
import csv
import io
import math
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime
from zoneinfo import ZoneInfo
import streamlit as st

LOCAL_ZONE = ZoneInfo('America/Indianapolis')
SERIES = {
    'BAA': "Moody's Baa corporate bond yield",
    'FEDFUNDS': 'Effective federal funds rate',
    'DGS10': '10-year Treasury yield',
    'MORTGAGE30US': '30-year fixed mortgage rate',
    'CPIAUCSL': 'Consumer Price Index: all urban consumers, seasonally adjusted',
    'PAYEMS': 'All employees: total nonfarm payrolls',
}
UNITS = {**{s: 'Percent' for s in ['BAA','FEDFUNDS','DGS10','MORTGAGE30US']},
         'CPIAUCSL': 'Index, 1982–1984 = 100; seasonally adjusted',
         'PAYEMS': 'Thousands of persons; seasonally adjusted'}


def local_today():
    return datetime.now(LOCAL_ZONE).date()


def validate_id(series_id):
    value = series_id.strip().upper()
    if not re.fullmatch(r'[A-Z0-9_]{1,80}', value):
        raise ValueError('Series ID must contain only letters, digits or underscores.')
    return value


def parse_csv(text, expected_column, vintage_cutoff=None):
    reader = csv.reader(io.StringIO(text.lstrip('\ufeff')))
    header = next(reader, None)
    if not header or len(header) != 2 or header[0] not in ('observation_date','DATE'):
        raise ValueError(f'Unexpected CSV header; expected observation_date and {expected_column}.')
    if vintage_cutoff is None:
        if header[1] != expected_column:
            raise ValueError('Current download does not match the requested series.')
    else:
        match = re.fullmatch(re.escape(expected_column) + r'_(\d{8})', header[1])
        if not match:
            raise ValueError('Vintage download lacks a matching dated series column.')
        effective = datetime.strptime(match.group(1), '%Y%m%d').date()
        if effective > vintage_cutoff:
            raise ValueError('Returned vintage is later than the requested cutoff.')
    values = {}
    for row in reader:
        if not row:
            continue
        if len(row) != 2:
            raise ValueError('Unexpected CSV row shape.')
        measured = date.fromisoformat(row[0])
        if row[1].strip() in ('', '.'):
            continue
        value = float(row[1])
        if not math.isfinite(value):
            raise ValueError('Nonfinite observation in source.')
        if measured in values:
            raise ValueError('Duplicate observation date in source.')
        values[measured] = value
    if not values:
        raise ValueError('No numeric observations in this download/vintage.')
    return values


def download_csv(url, expected_column, vintage_cutoff=None):
    request = urllib.request.Request(url, headers={'User-Agent': 'Lab17 educational FRED viewer'})
    try:
        with urllib.request.urlopen(request, timeout=35) as response:
            text = response.read().decode('utf-8-sig')
    except (urllib.error.URLError, TimeoutError, UnicodeError) as error:
        raise ValueError(f'Download failed: {error}') from error
    return dict(values=parse_csv(text, expected_column, vintage_cutoff), url=url,
                source_column=next(csv.reader(io.StringIO(text.lstrip('\ufeff'))))[1],
                downloaded_at=datetime.now(LOCAL_ZONE).isoformat(timespec='seconds'))


@st.cache_data(ttl=3600, max_entries=128, show_spinner=False)
def download_current(series_id, download_day):
    """One public FRED request per series; day parameter prevents overnight cache reuse."""
    series_id = validate_id(series_id)
    url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?' + urllib.parse.urlencode({'id':series_id})
    return download_csv(url, series_id)


@st.cache_data(ttl=3600, max_entries=128, show_spinner=False)
def download_vintage(series_id, vintage_date, download_day):
    """One public ALFRED request; its column identifies the requested vintage."""
    series_id = validate_id(series_id)
    cutoff = date.fromisoformat(str(vintage_date))
    url = 'https://alfred.stlouisfed.org/graph/alfredgraph.csv?' + urllib.parse.urlencode(
        {'id':series_id, 'vintage_date':cutoff.isoformat()})
    result = download_csv(url, series_id, cutoff)
    if max(result['values']) > cutoff:
        raise ValueError('Vintage contains an observation dated after the cutoff.')
    return result


def compare(current, vintage, start):
    now = {day:value for day,value in current.items() if day >= start}
    then = {day:value for day,value in vintage.items() if day >= start}
    now_last = max(now) if now else None
    then_last = max(then) if then else None
    common = set(now) & set(then)
    revised = sum(not math.isclose(now[day], then[day], rel_tol=0, abs_tol=1e-9) for day in common)
    late = sum(day > then_last for day in now) if then_last else len(now)
    return dict(known_date=then_last, known_value=then.get(then_last),
                current_date=now_last, current_value=now.get(now_last),
                later_count=late, revised_count=revised, overlap_count=len(common))

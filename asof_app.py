"""Run: python -m streamlit run asof_app.py"""
from datetime import date
import pandas as pd
import streamlit as st
from asof_data import SERIES, UNITS, local_today, validate_id, download_current, download_vintage, compare

st.set_page_config(page_title='Rates and point-in-time audit', layout='wide')
today = local_today()
st.title('Rates and point-in-time audit')
st.caption(f'Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today ({today}); built with AI help, a learning demonstration, not investment advice.')
st.caption('Downloads are live and cached for up to one hour; actual retrieval timestamps appear below. Observation dates are not publication dates.')
defaults = ['BAA', 'FEDFUNDS', 'DGS10', 'MORTGAGE30US']
selected = st.sidebar.multiselect('Series', defaults, default=defaults,
                                 format_func=lambda s:f'{s} — {SERIES[s]}', key='selected')
extra = st.sidebar.text_input('Add any other FRED series ID', placeholder='CPIAUCSL or PAYEMS', key='extra')
start = st.sidebar.date_input('Start date', value=date(2020,1,1), max_value=today,
                              min_value=date(1776,1,1), key='start')
cutoff = st.sidebar.date_input('As known on', value=today, min_value=date(1776,1,1), max_value=today, key='cutoff')
if st.sidebar.button('Refresh downloads'):
    download_current.clear()
    download_vintage.clear()
st.sidebar.caption('Counts and latest observations are restricted to the selected start date. Add CPIAUCSL for the Northbridge project or PAYEMS for the revision probe.')
if extra.strip():
    try:
        extra_id = validate_id(extra)
        if extra_id not in selected:
            selected = [*selected, extra_id]
    except ValueError as error:
        st.error(f'Additional series: {error}')

rows = []
for series in selected:
    st.subheader(f'{series} — {SERIES.get(series, "Additional FRED series")}')
    st.markdown(f'[FRED source page](https://fred.stlouisfed.org/series/{series})')
    try:
        with st.spinner(f'Loading {series}…'):
            current = download_current(series, today.isoformat())
            vintage = download_vintage(series, cutoff.isoformat(), today.isoformat())
        points = sorted((day,value) for day,value in current['values'].items() if day >= start)
        if points:
            frame = pd.DataFrame(points, columns=['Observation date','Value']).set_index('Observation date')
            st.line_chart(frame)
        else:
            st.info('No current observations in the selected window.')
        metrics = compare(current['values'], vintage['values'], start)
        last = metrics['known_date']
        st.caption(f'Last observation known on {cutoff}: {last or "none in window"}. Units: {UNITS.get(series, "native source units; check the linked FRED page")}.')
        st.caption(f"FRED retrieved: {current['downloaded_at']} | ALFRED retrieved: {vintage['downloaded_at']}")
        st.caption(f"ALFRED returned column {vintage['source_column']} (its effective vintage may precede the requested date).")
        rows.append({'Series':series, 'FRED page':f'https://fred.stlouisfed.org/series/{series}',
                     'Last measured date known then':str(last) if last else None,
                     'Value known then':metrics['known_value'],
                     'Last measured date today':str(metrics['current_date']) if metrics['current_date'] else None,
                     'Value today':metrics['current_value'],
                     'Values after last known date':metrics['later_count'],
                     'Revised values on shared dates':metrics['revised_count']})
    except (ValueError, OSError) as error:
        st.error(f'{series}: {error}. Other series continue to load.')

st.subheader('Point-in-time comparison')
st.caption('Revisions compare numeric observations on shared dates; missing days (.) are excluded. A vintage is a dated snapshot, not an exact release-time log. An old vintage can be absent for an otherwise valid series.')
if rows:
    st.dataframe(pd.DataFrame(rows), hide_index=True,
                 column_config={'FRED page':st.column_config.LinkColumn('Series (FRED)', display_text=r'https://fred\.stlouisfed\.org/series/(.*)')}, width='stretch')
else:
    st.info('Select a series with available data to show the comparison table.')

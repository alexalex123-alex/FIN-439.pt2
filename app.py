"""Run with: python -m streamlit run app.py"""
import importlib.util
import json
import os
from pathlib import Path
from datetime import date
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('panel', ROOT / '.agents/skills/legend-panel/scripts/panel.py')
panel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(panel)
edgar = panel.edgar

st.set_page_config(page_title='Legend Panel', page_icon='📊', layout='wide')
st.title('Legend Panel')
st.caption(edgar.DISCLOSURE)
st.write('One set of annual facts. Three investor lenses. Evidence before judgment.')
with st.sidebar:
    st.header('Company')
    ticker = st.text_input('Ticker', 'COST').strip().upper()
    as_of = st.date_input('Filing cutoff', date(2026, 11, 5))
    threshold = st.number_input('Wood revenue growth threshold (%)', min_value=0.0, max_value=100.0, value=15.0, step=1.0)
    st.caption('Set this to 5 for the COST probe; restore 15 for the saved screen.')
    user_agent = st.text_input('SEC contact: your name and email', value=os.getenv('SEC_USER_AGENT', ''), type='password')
    fetch = st.button('Download live SEC facts', type='primary')
    st.caption('Contact information is sent to SEC and is not saved.')
    st.divider()
    st.write('Saved runs: COST, NVDA and JPM. NVIDIA is the largest company in VT in the dated Vanguard holdings used here.')

if not edgar.re.fullmatch(r'[A-Z0-9.-]{1,12}', ticker):
    st.error('Enter a valid ticker.')
    st.stop()
if fetch:
    try:
        with st.spinner('Downloading SEC facts…'):
            edgar.download(ticker, user_agent, ROOT / 'reports/raw')
        for investor in panel.INVESTORS:
            st.session_state.pop(f'memo_{ticker}_{investor}', None)
    except (ValueError, RuntimeError, OSError) as exc:
        st.error(str(exc))

raw_path = ROOT / 'reports/raw' / f'{ticker}_companyfacts.json'
if not raw_path.exists():
    st.info('Download this ticker to begin, or enter COST, NVDA or JPM for a saved run.')
    st.stop()
try:
    company, provenance = panel.load_snapshot(raw_path)
    report = panel.analyze(company, ticker, as_of.isoformat(), provenance, threshold)
except (ValueError, OSError) as exc:
    st.error(str(exc))
    st.stop()
printed = panel.render_report(report)
st.subheader(f"{report['company']} · {ticker}")
st.caption(f"Snapshot retrieved {provenance.get('retrieved_at_utc', 'unknown')} · Filing cutoff {report['as_of']}")
st.subheader('Investor × check')
st.dataframe(pd.DataFrame(panel.panel_rows(report)), hide_index=True, width='stretch')
st.caption(f"Revenue CAGR: {panel.pct(report['revenue_cagr_pct'])} · Latest R&D / revenue: {panel.pct(report['rows'][-1]['rd_pct'])} · Latest liabilities / equity: {panel.multiple(report['rows'][-1]['liabilities_equity'])}")

st.subheader('Investor verdicts and memos')
meta_path = ROOT / 'reports' / f'{ticker}_memo_review.json'
meta = json.loads(meta_path.read_text(encoding='utf-8')) if meta_path.exists() else {}
if meta.get('evidence_sha256') != panel.evidence_hash(report):
    st.warning('These saved memos have not been reviewed against the selected evidence and threshold. Review them before relying on their verdicts.')
all_flags, missing = [], []
for col, investor in zip(st.columns(3), panel.INVESTORS):
    with col:
        path = panel.memo_path(ticker, investor)
        initial = path.read_text(encoding='utf-8') if path.exists() else ''
        st.markdown(f'### {investor}')
        memo = st.text_area(f'{investor} memo — edit to test the number guard', initial, height=320, key=f'memo_{ticker}_{investor}')
        st.metric('Business verdict', panel.verdict(memo))
        all_flags.extend([f"{investor}: {f['token']} (line {f['line']})" for f in edgar.unsupported_numbers(memo, printed)])
        if not memo.strip():
            missing.append(investor)
        st.markdown(memo)
        st.download_button(f'Download {investor} memo', memo, file_name=path.name, mime='text/markdown')
if all_flags:
    st.error('Unsupported numbers across memos: ' + '; '.join(all_flags))
elif missing:
    st.info('Memos still needed: ' + ', '.join(missing))
else:
    st.success('All three memos contain only numbers supported by the printed evidence. Review meaning and units too.')
st.caption('Memos are AI-authored judgments saved from the skill workflow; the app does not call a model. Edits here affect this session; download them to retain your changes.')

frame = pd.DataFrame(report['rows'])
chart = frame.set_index('fiscal_year_end')[['owner_earnings', 'net_income']] / 1_000_000
chart.columns = ['Owner earnings', 'Net income']
st.subheader('Cash generation and accounting profit')
st.caption('USD millions; missing values remain gaps.')
st.line_chart(chart)
st.subheader('Five-year financials')
display = []
for row in report['rows']:
    display.append({'Fiscal year end': row['fiscal_year_end'], **{
        key.replace('_', ' ').title(): edgar.formatted(row[key], key == 'roe_pct')
        for key in (*edgar.TAGS, 'roe_pct', 'owner_earnings', *panel.EXTRA_TAGS)},
        'R&D / revenue': panel.pct(row['rd_pct']), 'Liabilities / equity': panel.multiple(row['liabilities_equity'])})
st.caption('USD millions except percentages and liabilities / equity.')
st.dataframe(pd.DataFrame(display), hide_index=True, width='stretch')
st.download_button('Download printed evidence', printed, file_name=f'{ticker}_panel.md', mime='text/markdown')
with st.expander('Source tags, filing accessions and calculations'):
    st.markdown(printed)
    st.json(provenance)
with st.expander('Lab decision and student checkout'):
    path = ROOT / 'LAB19.md'
    if path.exists():
        st.markdown(path.read_text(encoding='utf-8'))

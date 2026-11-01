"""Run: python -m streamlit run app.py"""
import copy
import hashlib
import io
from pathlib import Path
import streamlit as st
import portfolio as engine

st.set_page_config(page_title='Portfolio stability lab', layout='wide')
st.title('Portfolio stability lab')
st.caption('Built with AI help, a learning demonstration, not investment advice.')

mode = st.sidebar.radio('Universe', ['Meridian training', 'Northbridge funds'], key='universe')
objective = st.sidebar.number_input('Objective return (%)', value=6.5 if mode == 'Meridian training' else 5.5,
                                    step=0.1, key=f'objective_{mode}') / 100
minimum = st.sidebar.number_input('Reserve minimum (%)', min_value=0.0, max_value=100.0,
                                  value=3.0, step=1.0, key=f'minimum_{mode}') / 100
uploaded = st.sidebar.file_uploader('Upload monthly adjusted prices (CSV)', type=['csv'])
last36 = st.sidebar.checkbox('Use last 36 months', key='last36')

try:
    if uploaded is not None:
        raw = uploaded.getvalue()
    elif mode == 'Northbridge funds':
        raw = Path(__file__).with_name('prices.csv').read_bytes()
    else:
        raw = None
    if raw is None:
        loaded_assets = copy.deepcopy(engine.ASSETS)
        correlations = engine.CORRELATIONS
        active_assets = copy.deepcopy(loaded_assets)
        scope = 'Meridian: course-authored training values'
        identity = 'meridian'
        if last36:
            st.info('The 36-month switch applies to CSV data; Meridian uses fixed training inputs.')
    else:
        text = raw.decode('utf-8-sig')
        loaded = engine.estimate_from_csv(io.StringIO(text))
        active = engine.estimate_from_csv(io.StringIO(text), last36)
        loaded_assets = loaded['assets']
        active_assets = copy.deepcopy(active['assets'])
        correlations = active['correlations']
        identity = hashlib.sha256(raw).hexdigest()[:12] + str(last36)
        scope = f"Historical estimates: {active['observations']} monthly returns, {active['first_return']} to {active['last_return']}"
        st.caption('Only BIL is reserve-eligible by default. Adjust eligibility to match your mandate.')
    st.subheader(scope)
    st.write('Edit return estimates or reserve eligibility to test stability. The comparison keeps the original loaded inputs and all months, using the same objective and reserve minimum.')
    for index, asset in enumerate(active_assets):
        left, right = st.columns([3, 1])
        asset['return'] = left.number_input(f"{asset['name']} expected return (%) — estimate" if raw else f"{asset['name']} expected return (%) — training",
                                           value=float(asset['return'] * 100), step=0.1,
                                           key=f'return_{identity}_{index}') / 100
        asset['reserve'] = right.checkbox(f"{asset['name']}: reserve-eligible", value=asset['reserve'],
                                          key=f'reserve_{identity}_{index}')
    base_correlations = engine.CORRELATIONS if raw is None else loaded['correlations']
    baseline = engine.search_portfolios(loaded_assets, base_correlations, objective, minimum)
    current = engine.search_portfolios(active_assets, correlations, objective, minimum)

    def show_result(title, result, assets):
        st.subheader(title)
        if result is None:
            st.warning('No mix meets the objective')
            return
        st.table([{'Asset': asset['name'], 'Weight (%)': f'{weight * 100:.2f}'}
                  for asset, weight in zip(assets, result['weights'])])
        st.metric('Expected return', f"{result['expected_return']:.2%}")
        st.metric('Volatility', f"{result['volatility']:.2%}")
        st.metric('Reserve-eligible weight', f"{result['reserve']:.2%}")

    first, second = st.columns(2)
    with first:
        show_result('As loaded — all months', baseline, loaded_assets)
    with second:
        show_result('Current inputs', current, active_assets)
    change = engine.largest_weight_change(baseline, current)
    st.metric('Largest weight change (percentage points)', 'N/A' if change is None else f'{change:.2f}')
    st.caption('Search: long-only, fully funded, 5-percentage-point grid. A 3% reserve minimum requires at least 5% on this grid. Returns are estimates, not guarantees; the model does not verify turnover or future spending coverage.')
except (ValueError, UnicodeError, OSError) as error:
    st.error(f'Cannot use these inputs: {error}')

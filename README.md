
  <h1>World Bank Indicators Dashboard</h1>
  <p class="lead">Interactive Streamlit dashboard for Data Cleaning & Exploratory Data Analysis (EDA) on World Bank development indicators: GDP per capita, Income Growth, Life Expectancy, Population.</p>

  <div class="badges">
    <img src="https://img.shields.io/badge/python-3.10-blue" alt="python"/>
    <img src="https://img.shields.io/badge/streamlit-1.0-orange" alt="streamlit"/>
    <img src="https://img.shields.io/badge/plotly-graph-green" alt="plotly"/>
  </div>

  <h2>Demo</h2>
  <p>Live demo: <a class="btn" href="https://www.youtube.com/watch?v=RqYpfMbiT-g" target="_blank" rel="noopener">Open Dashboard</a></p>

  <h2>Features</h2>
  <div class="kpis">
    <div class="card"><strong>Data Cleaning</strong><div>Wide → long reshape, missing handling, ISO3 standardization</div></div>
    <div class="card"><strong>EDA & Visuals</strong><div>KPI cards, trends, rankings, bubble charts, heatmaps</div></div>
    <div class="card"><strong>Forecasting</strong><div>Linear regression & exponential smoothing</div></div>
    <div class="card"><strong>Exports</strong><div>CSV/JSON/Excel & PDF report generation</div></div>
  </div>

  <h2>Quick Start</h2>
  <ol>
    <li>Clone the repo: <pre>git clone https://github.com/swairariaz/Worldbank-dashboard.git</pre></li>
    <li>Create environment & install: <pre>python -m venv venv && source venv/bin/activate
pip install -r requirements.txt</pre></li>
    <li>Run the app: <pre>streamlit run app.py --server.port 8501</pre></li>
    <li>Sample data: place your CSV in <code>/data/path.csv</code>. See <code>data_loader.py</code>.</li>
  </ol>

  <section id="project-structure" style="font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial;max-width:980px;margin:20px auto;padding:18px;background:#fff;border-radius:10px;border:1px solid #eef2f7;">
  <h2 style="margin-top:0;color:#0b1220;">Project structure & file purposes</h2>
  <p style="color:#475569;margin-top:4px;">Clear mapping of files to purpose — quick reference for clients and reviewers.</p>

  <table style="width:100%;border-collapse:collapse;margin-top:12px;">
    <colgroup><col style="width:39%"><col style="width:61%"></colgroup>
    <thead>
      <tr style="text-align:left;border-bottom:2px solid #eef2f7;">
        <th style="padding:10px 8px;color:#0b1220;">File / Path</th>
        <th style="padding:10px 8px;color:#0b1220;">Purpose (one line)</th>
      </tr>
    </thead>
    <tbody style="color:#334155;">
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 8px;font-family:monospace;">Data/processed/features/latest_snapshot.csv</td>
        <td style="padding:10px 8px;">Latest snapshot of processed indicators used for quick demo and small queries.</td>
      </tr>
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 8px;font-family:monospace;">Data/processed/features/main_data.csv</td>
        <td style="padding:10px 8px;">Master long-format dataset (merged, cleaned, canonical source for analysis).</td>
      </tr>
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 8px;font-family:monospace;">Data/processed/features/world_aggregates.csv</td>
        <td style="padding:10px 8px;">Precomputed country/region aggregates & summary metrics for fast rendering.</td>
      </tr>
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 8px;font-family:monospace;">Data/processed/features/worldbank_indicators_cleaned.csv</td>
        <td style="padding:10px 8px;">Cleaned raw indicators (standardized and validated).</td>
      </tr>
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 8px;font-family:monospace;">Data/processed/features/path.csv</td>
        <td style="padding:10px 8px;">Config paths / raw indicators (originally from World Bank).</td>
      </tr>
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 8px;font-family:monospace;">src/__pycache__/</td>
        <td style="padding:10px 8px;">Python bytecode cache (auto-generated; ignore / not committed).</td>
      </tr>
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 8px;font-family:monospace;">src/data_loader.py</td>
        <td style="padding:10px 8px;">Load & clean pipeline: wide→long reshape, missing-value strategy, ISO3 standardization.</td>
      </tr>
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 8px;font-family:monospace;">src/features.py</td>
        <td style="padding:10px 8px;">Feature engineering: rankings, rolling averages, year-over-year changes, aggregates.</td>
      </tr>
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 8px;font-family:monospace;">src/charts.py</td>
        <td style="padding:10px 8px;">Plotly visualizations: KPI cards, line/bar charts, bubble chart, correlation heatmap.</td>
      </tr>
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 8px;font-family:monospace;">src/forecast.py</td>
        <td style="padding:10px 8px;">Forecasting logic: linear regression helpers and exponential smoothing routines.</td>
      </tr>
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 8px;font-family:monospace;">src/styles.py</td>
        <td style="padding:10px 8px;">UI theming & small CSS tweaks used by Streamlit to ensure a polished look.</td>
      </tr>
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 8px;font-family:monospace;">src/utils.py</td>
        <td style="padding:10px 8px;">Helper utilities: exports (CSV/JSON/Excel), report generation, common IO helpers.</td>
      </tr>
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 8px;font-family:monospace;">src/app.py</td>
        <td style="padding:10px 8px;">Main Streamlit application wiring together loader → features → charts → UI components.</td>
      </tr>
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 8px;font-family:monospace;">requirements.txt</td>
        <td style="padding:10px 8px;">Pinned Python dependencies for reproducible installs (use with a venv).</td>
      </tr>
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 8px;font-family:monospace;">test_data_loading.py</td>
        <td style="padding:10px 8px;">Unit tests verifying data loader behavior and basic integrity checks.</td>
      </tr>
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 8px;font-family:monospace;">test_features.py</td>
        <td style="padding:10px 8px;">Unit tests for feature engineering (ranks, rolling averages, YoY calculations).</td>
      </tr>
      <tr>
        <td style="padding:10px 8px;font-family:monospace;">test_setup.py</td>
        <td style="padding:10px 8px;">Lightweight environment checks & smoke tests (CI-friendly sanity checks).</td>
      </tr>
    </tbody>
  </table>

  <p style="margin-top:14px;color:#475569;">Tip: keep `Data/processed/features/` populated with a small sample CSV for quick demos; provide full dataset on request for paid gigs.</p>
</section>


  <h2>Screenshots</h2>
  <div class="screens">
    <img src="screenshot_kpis.png" alt="KPI view">
    <img src="screenshot_compare.png" alt="Comparison charts">
    <img src="screenshot_bubble.png" alt="Bubble & heatmap">
  </div>

  <h2>Notes & Recommendations</h2>
  <ul>
    <li>For production hosting, use Streamlit Cloud or Docker.</li>
    <li>Small datasets (≤100k rows) are supported; for large datasets, enable server-side paging.</li>
    <li>Adjust forecasting horizon in <code>forecast.py</code> as required.</li>
  </ul>

  <h2>Contact</h2>
  <p>If you want a custom dashboard or want this hosted for your organization, email: <strong>swairariaz101@gmail.com</strong>.</p>

  <footer>
    <small>Built with ❤️ by Swaira Riaz • Last updated: 2025</small>
  </footer>
</body>
</html>

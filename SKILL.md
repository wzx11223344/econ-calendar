---
slug: econ-calendar
displayName: "全球经济日历"
version: 1.0.0
summary: "Global economic events calendar with pre-built event database (50+ events for 2026 Q3-Q4), live data fetching via akshare, market impact analysis, and interactive HTML dashboard."
tags:
  - economics
  - calendar
  - events
  - trading
license: MIT
author: "Econ Calendar Contributors"
---

# 全球经济日历 (Global Economic Calendar)

## Overview

A comprehensive economic events calendar covering four major regions -- China (NBS, PBoC), United States (FOMC, BLS), European Union (ECB, Eurostat), and Japan (BOJ, MoF) -- plus global events (OPEC, G20). Includes 50+ pre-scheduled events for 2026 Q3-Q4 with market impact ratings, historical volatility context, and affected asset classes.

## Key Features

1. **Pre-built Event Database**: 50+ economic events with realistic 2026 Q3-Q4 dates (FOMC, NBS, ECB, BOJ, OPEC, CPI releases) rated 1-5 stars for market impact.

2. **Live Data Fetching**: Pulls actual China macro data (CPI, PMI, LPR, trade balance, M2) via akshare when installed. Falls back to web sources (Forex Factory, Investing.com).

3. **Market Impact Analysis**: Each event tagged with:
   - Markets impacted (A-share, US Equity, Commodities, FX, Gold, Oil, Crypto)
   - Direction bias (bullish / bearish / neutral / data-dependent)
   - Historical volatility context (low / medium / high)

4. **Interactive HTML Dashboard**: Month-view calendar with:
   - Color-coded events by impact level
   - Region filter toggle (CN/US/EU/JP)
   - Event detail popovers with full metadata
   - Weekly Focus section highlighting top-impact events
   - Navigation between months

5. **CLI Interface**: Rich-formatted terminal output with `today`, `week`, `month`, `dashboard`, `stats`, `live`, `search` commands.

## Usage

### CLI Commands

```bash
# Today's events
python econcal.py today

# This week's events (high impact only)
python econcal.py week --min-impact 4

# September 2026 events, China + US only
python econcal.py month -m 9 -r CN,US

# Generate HTML dashboard for September 2026
python econcal.py dashboard -m 9 -o dashboard.html

# Show database statistics
python econcal.py stats

# Fetch live China macro data
python econcal.py live

# Search events
python econcal.py search FOMC
```

### Python API

```python
from econ_calendar.events import EventDatabase

db = EventDatabase()

# Get September 2026 events
events = db.by_month(2026, 9)
for e in events:
    print(f"{e.date} | {'\u2605'*e.impact} | {e.title}")

# Get upcoming events in next 14 days
from datetime import date
upcoming = db.upcoming(ref_date=date.today(), days=14)
```
```python
from econ_calendar.dashboard import generate_dashboard

# Generate HTML dashboard
path = generate_dashboard("september_2026.html", year=2026, month=9)
print(f"Dashboard: {path}")
```
```python
from econ_calendar.fetcher import MacroFetcher, fetch_cn_macro

# Fetch live China macro data
fetcher = MacroFetcher()
upcoming = fetcher.fetch_upcoming(days=7)
cn_data = fetch_cn_macro()
```

## Installation

```bash
pip install -r requirements.txt
```

Optional for live data fetching:
```bash
pip install akshare
```

## Event Coverage (2026 Q3-Q4)

| Month | China | US | EU | Japan | Global |
|-------|-------|----|----|-------|--------|
| Jul   | PMI, CPI, GDP, LPR, Trade | FOMC, NFP, CPI, PCE, GDP | ECB, CPI, PMI | BOJ, CPI, Tankan | -- |
| Aug   | PMI, CPI, Activity Data, LPR | CPI, NFP, Jackson Hole, PCE | CPI, GDP | -- | -- |
| Sep   | PMI, CPI, Activity Data, LPR | FOMC, CPI, NFP, PCE | ECB | BOJ | OPEC JMMC |
| Oct   | Golden Week, GDP, CPI, Plenum, LPR | CPI, NFP, GDP, PCE | ECB | BOJ | G20 |
| Nov   | PMI, CPI, 11.11, Activity Data, LPR | FOMC, Election, CPI, NFP | -- | -- | OPEC Full |
| Dec   | PMI, CEWC, CPI, Activity Data, LPR | FOMC, CPI, NFP, PCE, Quad Witching | ECB | BOJ, Tankan | Christmas, NYE |

## Data Sources

- **Pre-built events**: Manually curated from official central bank and statistics bureau release calendars.
- **Live China data**: [akshare](https://github.com/akfamily/akshare) Python library.
- **Web fallback**: Forex Factory RSS, Investing.com economic calendar.
- **Historical patterns**: NBS monthly release schedule, FOMC meeting calendar, ECB/BOJ policy meeting schedules.

## Limitations

- Pre-built dates for 2026 H2 are based on historical release patterns; actual dates may shift by 1-2 days.
- Live data via akshare requires the library to be installed and functional.
- Web scraping sources may be rate-limited or change their HTML structure.
- This tool is for informational purposes only and does not constitute financial advice.

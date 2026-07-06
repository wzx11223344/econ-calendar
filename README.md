# Global Economic Calendar

A comprehensive economic events calendar with market impact analysis covering China, US, EU, and Japan. Features 50+ pre-built events for 2026 Q3-Q4, live data fetching, and an interactive HTML dashboard.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Show today's events
python econcal.py today

# Show this month's events
python econcal.py month

# Generate HTML dashboard
python econcal.py dashboard -o dashboard.html

# Show help
python econcal.py --help
```

## Features

- **50+ Pre-built Events**: Realistic 2026 Q3-Q4 schedule (FOMC, NBS, ECB, BOJ, OPEC, CPI releases)
- **Impact Ratings**: 1-5 star market impact classification
- **Market Analysis**: Which markets each event affects, direction bias, volatility context
- **4 Regions + Global**: China, US, Eurozone, Japan, plus OPEC/G20/holidays
- **Interactive Dashboard**: Color-coded month-view HTML calendar with filters and popovers
- **Live Data**: akshare integration for China macro data, web scraping fallback

## CLI Commands

```bash
python econcal.py today                        # Today's events
python econcal.py week                         # This week's events
python econcal.py week --min-impact 4          # High-impact only
python econcal.py month -m 9                   # September 2026
python econcal.py month -r CN,US -m 9          # Filter by region
python econcal.py dashboard -o cal.html        # HTML dashboard
python econcal.py stats                        # Database stats
python econcal.py search CPI                   # Search events
python econcal.py live                         # Live China macro data
```

## Python API

```python
from econ_calendar.events import EventDatabase
from econ_calendar.dashboard import generate_dashboard

db = EventDatabase()

# Get events by month
events = db.by_month(2026, 9)
for e in events:
    print(f"{e.date} | {'\u2605'*e.impact} | {e.title}")

# Generate dashboard
generate_dashboard("dashboard.html", year=2026, month=9)
```

## File Structure

```
econ-calendar/
├── econcal.py               # CLI entry point
├── econ_calendar/
│   ├── __init__.py          # Package init with exports
│   ├── events.py            # 50+ pre-built events + EventDatabase class
│   ├── fetcher.py           # Live data fetcher (akshare + web)
│   └── dashboard.py         # HTML dashboard generator
├── SKILL.md                 # Skill definition with frontmatter
├── README.md                # This file
└── requirements.txt         # Python dependencies
```

## Requirements

- Python 3.9+
- `click` - CLI framework
- `rich` - Terminal formatting
- `requests` - HTTP client (web fetcher)
- `akshare` (optional) - China macro data

## License

MIT

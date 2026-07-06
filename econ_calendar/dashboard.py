"""
HTML Calendar Dashboard Generator
==================================

Generates a standalone HTML dashboard showing:
- Month-view calendar with color-coded economic events
- Impact indicators (1-5 stars)
- Event detail popovers on click
- Weekly focus section highlighting top events
- Region filter toggle (CN/US/EU/JP)

Usage::

    from econ_calendar.dashboard import DashboardGenerator, generate_dashboard

    gen = DashboardGenerator()
    html = gen.render(year=2026, month=9, regions=["CN", "US"])
    # or:
    generate_dashboard("dashboard.html", year=2026, month=9)
"""

from datetime import date, datetime, timedelta
import calendar as cal_mod
import json
import os
from typing import Dict, List, Optional

from econ_calendar.events import EventDatabase, EconomicEvent, Region

# ──────────────────────────────────────────────────────────
# Impact color scheme
# ──────────────────────────────────────────────────────────

IMPACT_COLORS = {
    1: {"bg": "#e8f5e9", "border": "#81c784", "text": "#2e7d32", "label": "Low"},
    2: {"bg": "#e3f2fd", "border": "#64b5f6", "text": "#1565c0", "label": "Minor"},
    3: {"bg": "#fff3e0", "border": "#ffb74d", "text": "#e65100", "label": "Moderate"},
    4: {"bg": "#fce4ec", "border": "#e57373", "text": "#c62828", "label": "High"},
    5: {"bg": "#f3e5f5", "border": "#ab47bc", "text": "#6a1b9a", "label": "Critical"},
}

REGION_COLORS = {
    "CN": "#de2910",
    "US": "#002868",
    "EU": "#003399",
    "JP": "#bc002d",
    "GLOBAL": "#333333",
}

REGION_LABELS = {
    "CN": "China",
    "US": "United States",
    "EU": "Eurozone",
    "JP": "Japan",
    "GLOBAL": "Global",
}


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Global Economic Calendar - {title_month}</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC',
      'Microsoft YaHei', sans-serif;
    background: #f0f2f5;
    margin: 0; padding: 0; color: #1a1a2e;
  }}
  .container {{ max-width: 1400px; margin: 0 auto; padding: 24px; }}

  /* Header */
  .header {{
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: #fff; padding: 32px 40px; border-radius: 16px;
    margin-bottom: 24px; position: relative; overflow: hidden;
  }}
  .header::after {{
    content: ''; position: absolute; top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
    border-radius: 50%;
  }}
  .header h1 {{ font-size: 28px; margin: 0 0 8px; font-weight: 700; letter-spacing: -0.5px; }}
  .header .subtitle {{ font-size: 14px; opacity: 0.75; }}
  .header .nav {{ margin-top: 16px; display: flex; gap: 8px; flex-wrap: wrap; }}
  .header .nav a {{
    background: rgba(255,255,255,0.12); color: #fff; text-decoration: none;
    padding: 6px 16px; border-radius: 20px; font-size: 13px;
    transition: background 0.2s;
  }}
  .header .nav a:hover, .header .nav a.active {{
    background: rgba(255,255,255,0.25);
  }}

  /* Filters */
  .filters {{
    display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; align-items: center;
  }}
  .filters .label {{ font-size: 13px; color: #666; font-weight: 600; margin-right: 4px; }}
  .filter-btn {{
    border: 2px solid #ddd; background: #fff; padding: 6px 14px;
    border-radius: 20px; cursor: pointer; font-size: 13px; font-weight: 500;
    transition: all 0.2s; color: #555;
  }}
  .filter-btn:hover {{ border-color: #999; }}
  .filter-btn.active {{ border-color: #302b63; background: #302b63; color: #fff; }}

  /* Stats bar */
  .stats-bar {{
    display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap;
  }}
  .stat-card {{
    background: #fff; border-radius: 12px; padding: 16px 24px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06); flex: 1; min-width: 120px;
  }}
  .stat-card .stat-num {{ font-size: 32px; font-weight: 800; color: #302b63; }}
  .stat-card .stat-label {{ font-size: 12px; color: #888; margin-top: 2px; }}

  /* Calendar Grid */
  .calendar {{ background: #fff; border-radius: 16px; overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  }}
  .month-header {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 20px 28px; border-bottom: 1px solid #eee;
  }}
  .month-header h2 {{ margin: 0; font-size: 22px; font-weight: 700; }}
  .month-header .month-nav {{ display: flex; gap: 4px; }}
  .month-header .month-nav button {{
    background: #f5f5f5; border: none; padding: 6px 14px; border-radius: 8px;
    cursor: pointer; font-size: 14px; transition: background 0.2s;
  }}
  .month-header .month-nav button:hover {{ background: #e0e0e0; }}
  .day-headers {{
    display: grid; grid-template-columns: repeat(7, 1fr);
    padding: 12px 20px; background: #fafafa; border-bottom: 1px solid #eee;
  }}
  .day-headers span {{
    text-align: center; font-size: 12px; font-weight: 600; color: #888;
    text-transform: uppercase; letter-spacing: 0.5px;
  }}
  .days-grid {{
    display: grid; grid-template-columns: repeat(7, 1fr);
    min-height: 480px;
  }}
  .day-cell {{
    border-right: 1px solid #f0f0f0; border-bottom: 1px solid #f0f0f0;
    padding: 6px; min-height: 90px; cursor: pointer; transition: background 0.15s;
    position: relative;
  }}
  .day-cell:nth-child(7n) {{ border-right: none; }}
  .day-cell:hover {{ background: #f8f9ff; }}
  .day-cell.other-month {{ opacity: 0.35; }}
  .day-cell.today {{ background: #eef1ff; }}
  .day-cell .day-num {{
    font-size: 13px; font-weight: 600; color: #555; margin-bottom: 3px;
  }}
  .day-cell.today .day-num {{
    display: inline-block; background: #302b63; color: #fff;
    width: 24px; height: 24px; border-radius: 50%; text-align: center;
    line-height: 24px; font-size: 12px;
  }}
  .day-cell .event-dot {{
    display: flex; align-items: center; gap: 3px; margin: 2px 0;
    padding: 2px 4px; border-radius: 4px; font-size: 10px; line-height: 1.3;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  }}
  .day-cell .event-dot .badge {{
    width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0;
  }}
  .day-cell .more-link {{
    font-size: 10px; color: #999; cursor: pointer; padding: 2px 4px;
  }}
  .day-cell .more-link:hover {{ color: #302b63; }}

  /* Weekly Focus */
  .weekly-focus {{
    background: #fff; border-radius: 16px; padding: 24px 28px;
    margin-top: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  }}
  .weekly-focus h3 {{
    margin: 0 0 16px; font-size: 18px; display: flex; align-items: center; gap: 8px;
  }}
  .weekly-focus h3 .icon {{ font-size: 20px; }}
  .focus-grid {{
    display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 12px;
  }}
  .focus-card {{
    border: 2px solid #eee; border-radius: 12px; padding: 14px 18px;
    transition: all 0.2s; cursor: pointer;
  }}
  .focus-card:hover {{ border-color: #302b63; box-shadow: 0 2px 8px rgba(48,43,99,0.08); }}
  .focus-card .fc-date {{ font-size: 11px; color: #999; font-weight: 600; }}
  .focus-card .fc-title {{ font-size: 14px; font-weight: 700; margin: 4px 0; }}
  .focus-card .fc-desc {{ font-size: 12px; color: #666; line-height: 1.5; }}
  .focus-card .fc-tags {{ display: flex; gap: 6px; margin-top: 8px; flex-wrap: wrap; }}
  .focus-card .fc-tag {{
    font-size: 10px; padding: 3px 8px; border-radius: 10px;
    font-weight: 600;
  }}
  .tag-region {{ background: #eef1ff; color: #302b63; }}
  .tag-market {{ background: #fff3e0; color: #e65100; }}

  /* Modal */
  .modal-overlay {{
    position: fixed; inset: 0; background: rgba(0,0,0,0.45);
    display: none; justify-content: center; align-items: center; z-index: 1000;
  }}
  .modal-overlay.active {{ display: flex; }}
  .modal {{
    background: #fff; border-radius: 16px; max-width: 520px; width: 90%;
    max-height: 80vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0,0,0,0.2);
    animation: modalIn 0.2s ease;
  }}
  @keyframes modalIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  .modal-header {{
    padding: 20px 24px 0; display: flex; justify-content: space-between;
    align-items: flex-start;
  }}
  .modal-header h2 {{ margin: 0; font-size: 18px; }}
  .modal-close {{
    background: none; border: none; font-size: 24px; cursor: pointer;
    color: #999; padding: 0; line-height: 1;
  }}
  .modal-close:hover {{ color: #333; }}
  .modal-body {{ padding: 16px 24px 24px; }}
  .modal .field {{ margin-bottom: 12px; }}
  .modal .field-label {{ font-size: 11px; color: #999; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
  .modal .field-value {{ font-size: 14px; color: #333; margin-top: 2px; }}
  .modal .stars {{ color: #f59e0b; font-size: 16px; letter-spacing: 2px; }}
  .modal .markets {{ display: flex; gap: 6px; flex-wrap: wrap; margin-top: 4px; }}
  .modal .mkt-tag {{
    font-size: 11px; padding: 3px 10px; border-radius: 12px;
    background: #f0f2f5; color: #555; font-weight: 500;
  }}

  /* Footer */
  .footer {{
    text-align: center; padding: 32px; color: #bbb; font-size: 12px;
  }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>Global Economic Calendar</h1>
    <div class="subtitle">{title_month} | China &middot; US &middot; EU &middot; Japan &middot; Global</div>
    <div class="nav">
      {nav_links}
    </div>
  </div>

  <!-- Filters -->
  <div class="filters">
    <span class="label">Region:</span>
    <button class="filter-btn active region-filter" data-region="all">All</button>
    <button class="filter-btn region-filter" data-region="CN">China</button>
    <button class="filter-btn region-filter" data-region="US">US</button>
    <button class="filter-btn region-filter" data-region="EU">EU</button>
    <button class="filter-btn region-filter" data-region="JP">Japan</button>
    <span class="label" style="margin-left: 16px;">Impact:</span>
    <button class="filter-btn active impact-filter" data-impact="all">All</button>
    <button class="filter-btn impact-filter" data-impact="4">4+ Stars</button>
    <button class="filter-btn impact-filter" data-impact="5">5 Stars Only</button>
  </div>

  <!-- Stats -->
  <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-num">{total_events}</div>
      <div class="stat-label">Total Events This Month</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">{high_impact}</div>
      <div class="stat-label">High Impact (4-5 Stars)</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">{critical_events}</div>
      <div class="stat-label">Critical (5 Stars)</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">{regions_count}</div>
      <div class="stat-label">Regions Active</div>
    </div>
  </div>

  <!-- Monthly Calendar -->
  <div class="calendar">
    <div class="month-header">
      <h2>{month_name} {year}</h2>
      <div class="month-nav">
        <button onclick="window.location.href='?month={prev_month}&year={prev_year}'">&larr; Prev</button>
        <button onclick="window.location.href='?month={cur_month}&year={cur_year}'">Today</button>
        <button onclick="window.location.href='?month={next_month}&year={next_year}'">Next &rarr;</button>
      </div>
    </div>
    <div class="day-headers">
      <span>Sun</span><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span>
    </div>
    <div class="days-grid">
      {calendar_cells}
    </div>
  </div>

  <!-- Weekly Focus -->
  <div class="weekly-focus">
    <h3><span class="icon">&#128197;</span> Weekly Focus &mdash; Top Events</h3>
    <div class="focus-grid" id="focusGrid">
      {focus_cards}
    </div>
  </div>

  <div class="footer">
    Global Economic Calendar v1.0 | Data sourced from public schedules. Not financial advice.
  </div>
</div>

<!-- Modal -->
<div class="modal-overlay" id="modalOverlay">
  <div class="modal">
    <div class="modal-header">
      <h2 id="modalTitle"></h2>
      <button class="modal-close" onclick="closeModal()">&times;</button>
    </div>
    <div class="modal-body" id="modalBody"></div>
  </div>
</div>

<script>
  const EVENTS = {events_json};

  function renderEvents() {{
    const activeRegion = document.querySelector('.region-filter.active')?.dataset.region || 'all';
    const activeImpact = document.querySelector('.impact-filter.active')?.dataset.impact || 'all';
    const minImpact = activeImpact === 'all' ? 0 : parseInt(activeImpact);

    // Filter day cells
    document.querySelectorAll('.day-cell').forEach(cell => {{
      const cellEvents = JSON.parse(cell.dataset.events || '[]');
      const visible = cellEvents.some(e => {{
        const regionMatch = activeRegion === 'all' || e.region === activeRegion;
        const impactMatch = e.impact >= minImpact;
        return regionMatch && impactMatch;
      }});
      cell.style.opacity = visible || cellEvents.length === 0 ? '' : '0.4';
    }});

    // Filter focus cards
    document.querySelectorAll('.focus-card').forEach(card => {{
      const region = card.dataset.region;
      const impact = parseInt(card.dataset.impact);
      const regionMatch = activeRegion === 'all' || region === activeRegion;
      const impactMatch = impact >= minImpact;
      card.style.display = (regionMatch && impactMatch) ? '' : 'none';
    }});
  }}

  // Filter buttons
  document.querySelectorAll('.region-filter').forEach(btn => {{
    btn.addEventListener('click', function() {{
      document.querySelectorAll('.region-filter').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      renderEvents();
    }});
  }});
  document.querySelectorAll('.impact-filter').forEach(btn => {{
    btn.addEventListener('click', function() {{
      document.querySelectorAll('.impact-filter').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      renderEvents();
    }});
  }});

  // Modal
  function showModal(eventId) {{
    const evt = EVENTS.find(e => e.event_id === eventId);
    if (!evt) return;
    const impacts = ['','\u2605','\u2605\u2605','\u2605\u2605\u2605','\u2605\u2605\u2605\u2605','\u2605\u2605\u2605\u2605\u2605'];
    const regions = {{'CN':'China','US':'United States','EU':'Eurozone','JP':'Japan','GLOBAL':'Global'}};
    document.getElementById('modalTitle').textContent = evt.title;
    document.getElementById('modalBody').innerHTML = `
      <div class="field"><div class="field-label">Date</div><div class="field-value">${{evt.date}}</div></div>
      <div class="field"><div class="field-label">Region</div><div class="field-value">${{regions[evt.region] || evt.region}}</div></div>
      <div class="field"><div class="field-label">Impact</div><div class="field-value stars">${{impacts[evt.impact] || ''}}</div></div>
      <div class="field"><div class="field-label">Category</div><div class="field-value">${{evt.category}}</div></div>
      <div class="field"><div class="field-label">Description</div><div class="field-value">${{evt.description}}</div></div>
      <div class="field"><div class="field-label">Markets Impacted</div><div class="markets">${{(evt.markets_impacted || []).map(m => `<span class="mkt-tag">${{m}}</span>`).join('')}}</div></div>
      <div class="field"><div class="field-label">Direction Bias</div><div class="field-value">${{evt.direction_bias}}</div></div>
      <div class="field"><div class="field-label">Historical Volatility</div><div class="field-value">${{evt.historical_volatility}}</div></div>
      ${{evt.notes ? `<div class="field"><div class="field-label">Notes</div><div class="field-value">${{evt.notes}}</div></div>` : ''}}
    `;
    document.getElementById('modalOverlay').classList.add('active');
  }}
  function closeModal() {{
    document.getElementById('modalOverlay').classList.remove('active');
  }}
  document.getElementById('modalOverlay').addEventListener('click', function(e) {{
    if (e.target === this) closeModal();
  }});
  document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape') closeModal();
  }});
</script>
</body>
</html>"""


class DashboardGenerator:
    """Generates the HTML economic calendar dashboard."""

    def __init__(self, events_db: Optional[EventDatabase] = None):
        self._db = events_db or EventDatabase()

    def _build_calendar_grid(
        self, year: int, month: int, events_by_day: Dict[int, List[Dict]]
    ) -> str:
        """Build the calendar day cells HTML."""
        today = date.today()
        first_weekday, num_days = cal_mod.monthrange(year, month)

        cells = []

        # Previous month's trailing days
        if first_weekday > 0:
            prev_month = month - 1 if month > 1 else 12
            prev_year = year if month > 1 else year - 1
            _, prev_days = cal_mod.monthrange(prev_year, prev_month)
            for d in range(prev_days - first_weekday + 1, prev_days + 1):
                cells.append(self._day_cell(prev_year, prev_month, d, [], today, is_other=True))

        # Current month
        for d in range(1, num_days + 1):
            day_events = events_by_day.get(d, [])
            cells.append(self._day_cell(year, month, d, day_events, today, is_other=False))

        # Next month's leading days
        remaining = 42 - len(cells)  # 6 rows * 7 cols
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
        for d in range(1, remaining + 1):
            cells.append(self._day_cell(next_year, next_month, d, [], today, is_other=True))

        return "\n".join(cells)

    def _day_cell(self, year: int, month: int, day: int,
                  events: List[Dict], today: date, is_other: bool) -> str:
        """Build a single day cell HTML."""
        d = date(year, month, day)
        is_today = (d == today)
        classes = ["day-cell"]
        if is_other:
            classes.append("other-month")
        if is_today:
            classes.append("today")

        events_json = json.dumps(
            [{"event_id": e["event_id"], "region": e["region"], "impact": e["impact"]}
             for e in events]
        )

        # Top 3 events visible in cell
        shown = events[:3]
        event_html = ""
        for e in shown:
            ci = IMPACT_COLORS.get(e["impact"], IMPACT_COLORS[1])
            rc = REGION_COLORS.get(e["region"], "#999")
            title = e["title"][:28]
            event_html += (
                f'<div class="event-dot" style="background:{ci["bg"]};border-left:3px solid {ci["border"]};" '
                f'onclick="event.stopPropagation();showModal(\'{e["event_id"]}\')" '
                f'title="{e["title"]}">'
                f'<span class="badge" style="background:{rc};"></span>'
                f'{title}'
                f'</div>'
            )

        if len(events) > 3:
            event_html += f'<div class="more-link">+{len(events) - 3} more</div>'

        day_attr = f'data-events=\'{events_json}\''

        return (
            f'<div class="{" ".join(classes)}" {day_attr}>'
            f'<div class="day-num">{day}</div>'
            f'{event_html}'
            f'</div>'
        )

    def _build_focus_cards(self, events: List[Dict]) -> str:
        """Build the weekly focus section with top events."""
        if not events:
            return '<p style="color:#999;">No events in this period.</p>'

        cards = []
        for e in events[:12]:
            stars = "\u2605" * e["impact"]
            region = REGION_LABELS.get(e["region"], e["region"])
            markets = ", ".join(e.get("markets_impacted", [])[:3])
            cards.append(
                f'<div class="focus-card" data-region="{e["region"]}" '
                f'data-impact="{e["impact"]}" onclick="showModal(\'{e["event_id"]}\')">'
                f'<div class="fc-date">{e["date"]} &middot; {stars}</div>'
                f'<div class="fc-title">{e["title"]}</div>'
                f'<div class="fc-desc">{e.get("description", "")[:120]}...</div>'
                f'<div class="fc-tags">'
                f'<span class="fc-tag tag-region">{region}</span>'
                f'<span class="fc-tag tag-market">{markets}</span>'
                f'</div></div>'
            )
        return "\n".join(cards)

    def render(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        regions: Optional[List[str]] = None,
    ) -> str:
        """
        Render the full HTML dashboard.

        Args:
            year: Year (default: current year).
            month: Month 1-12 (default: current month).
            regions: Filter to specific regions (default: all).

        Returns:
            Complete HTML string.
        """
        today = date.today()
        if year is None:
            year = today.year
        if month is None:
            month = today.month

        # Get events
        all_events = self._db.by_month(year, month)
        if regions:
            region_set = {r.upper() for r in regions}
            all_events = [e for e in all_events if e.region.value in region_set]

        # Index by day
        events_by_day: Dict[int, List[Dict]] = {}
        for e in all_events:
            d = e.date.day
            if d not in events_by_day:
                events_by_day[d] = []
            events_by_day[d].append(e.to_dict())

        # Sort events in each day by impact (desc)
        for d in events_by_day:
            events_by_day[d].sort(key=lambda x: -x["impact"])

        # Calendar grid
        calendar_cells = self._build_calendar_grid(year, month, events_by_day)

        # Focus cards: top events by impact this month
        sorted_events = sorted(all_events, key=lambda e: (-e.impact, e.date))
        focus_cards = self._build_focus_cards([e.to_dict() for e in sorted_events])

        # All events JSON for client-side filtering
        events_json = json.dumps([e.to_dict() for e in all_events], ensure_ascii=False)

        # Stats
        total = len(all_events)
        high = sum(1 for e in all_events if e.impact >= 4)
        critical = sum(1 for e in all_events if e.impact == 5)
        region_set = {e.region.value for e in all_events}

        # Navigation
        nav_links = ""
        for m_name, m_num in [("Jul", 7), ("Aug", 8), ("Sep", 9),
                                ("Oct", 10), ("Nov", 11), ("Dec", 12)]:
            cls = ' class="active"' if m_num == month else ""
            nav_links += f'<a href="?month={m_num}&year=2026"{cls}>{m_name}</a>'

        # Month navigation
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1

        return HTML_TEMPLATE.format(
            title_month=f"{cal_mod.month_name[month]} {year}",
            nav_links=nav_links,
            total_events=total,
            high_impact=high,
            critical_events=critical,
            regions_count=len(region_set),
            month_name=cal_mod.month_name[month],
            year=year,
            calendar_cells=calendar_cells,
            focus_cards=focus_cards,
            events_json=events_json,
            prev_month=prev_month,
            prev_year=prev_year,
            next_month=next_month,
            next_year=next_year,
            cur_month=today.month,
            cur_year=today.year,
        )

    def write(self, path: str, **kwargs) -> str:
        """Render and write dashboard to an HTML file."""
        html = self.render(**kwargs)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return path


def generate_dashboard(
    output_path: str = "dashboard.html",
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> str:
    """
    Convenience function: generate and save the HTML dashboard.

    Args:
        output_path: File path for the output HTML.
        year: Target year.
        month: Target month.

    Returns:
        Absolute path to the generated file.
    """
    gen = DashboardGenerator()
    path = gen.write(output_path, year=year, month=month)
    return os.path.abspath(path)

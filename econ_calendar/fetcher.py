"""
Live Economic Data Fetcher
===========================

Pulls upcoming economic release dates and actual data via:
- akshare (primary source for China macro data)
- Web scraping (fallback for international data)
- Combines with pre-built event database

Usage::

    from econ_calendar.fetcher import MacroFetcher, fetch_cn_macro

    fetcher = MacroFetcher()
    events = fetcher.fetch_upcoming(days=7)
"""

import logging
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional

import requests

from econ_calendar.events import (
    Direction,
    EconomicEvent,
    EventDatabase,
    Market,
    Region,
)

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────

FOREX_FACTORY_URL = "https://www.forexfactory.com/calendar"
INVESTING_COM_URL = "https://www.investing.com/economic-calendar/"
RSS_FEED_URL = "https://www.forexfactory.com/ffcal_week_this.xml"


class MacroFetcher:
    """
    Fetches economic event data from multiple sources.

    1. Primary: akshare for China macro data
    2. Secondary: Pre-built database as fallback
    3. Web: Scraping forex factory / investing.com
    """

    def __init__(self):
        self._db = EventDatabase()
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/125.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        })

    # ── akshare integration ──

    def fetch_cn_macro_calendar(self, year: Optional[int] = None) -> List[Dict]:
        """
        Fetch China macro release calendar from akshare.

        Uses the macro_china interface to get scheduled release dates
        for NBS data (CPI, PMI, GDP, etc.).
        """
        if year is None:
            year = date.today().year

        results = []
        try:
            import akshare as ak

            # Try getting China macro data release schedule
            try:
                df = ak.macro_china_lpr()
                if df is not None and not df.empty:
                    for _, row in df.tail(6).iterrows():
                        results.append({
                            "source": "akshare",
                            "title": f"PBoC LPR Rate ({row.get('TRADE_DATE', 'N/A')})",
                            "indicator": "LPR",
                            "value": str(row.get('LPR1Y', 'N/A')),
                            "region": "CN",
                        })
            except Exception:
                logger.debug("akshare LPR fetch skipped")

            # Try PMI
            try:
                df = ak.macro_china_pmi()
                if df is not None and not df.empty:
                    latest = df.iloc[-1]
                    results.append({
                        "source": "akshare",
                        "title": f"NBS Manufacturing PMI ({latest.get('日期', 'N/A')})",
                        "indicator": "PMI",
                        "value": str(latest.get('制造业', 'N/A')),
                        "region": "CN",
                    })
            except Exception:
                logger.debug("akshare PMI fetch skipped")

            # Try CPI
            try:
                df = ak.macro_china_cpi_monthly()
                if df is not None and not df.empty:
                    latest = df.iloc[-1]
                    results.append({
                        "source": "akshare",
                        "title": f"China CPI YoY ({latest.get('日期', 'N/A')})",
                        "indicator": "CPI",
                        "value": str(latest.get('全国-当月', 'N/A')),
                        "region": "CN",
                    })
            except Exception:
                logger.debug("akshare CPI fetch skipped")

            # Try trade balance
            try:
                df = ak.macro_china_trade_balance()
                if df is not None and not df.empty:
                    latest = df.iloc[-1]
                    results.append({
                        "source": "akshare",
                        "title": f"China Trade Balance ({latest.get('日期', 'N/A')})",
                        "indicator": "Trade Balance",
                        "value": str(latest.get('贸易差额', 'N/A')),
                        "region": "CN",
                    })
            except Exception:
                logger.debug("akshare trade balance fetch skipped")

        except ImportError:
            logger.warning(
                "akshare not installed. Run: pip install akshare\n"
                "Using pre-built event database as fallback."
            )
        except Exception as e:
            logger.error(f"akshare fetch error: {e}")

        return results

    def fetch_cn_money_supply(self) -> List[Dict]:
        """Fetch China money supply and credit data."""
        results = []
        try:
            import akshare as ak
            df = ak.macro_china_money_supply()
            if df is not None and not df.empty:
                latest = df.iloc[-1]
                results.append({
                    "source": "akshare",
                    "title": f"China M2 Money Supply ({latest.get('月份', 'N/A')})",
                    "indicator": "M2",
                    "value": str(latest.get('货币和准货币(M2)-期末同比', 'N/A')),
                    "region": "CN",
                })
        except Exception:
            logger.debug("M2 data fetch skipped")
        return results

    # ── Web scrape (fallback) ──

    def fetch_forex_factory(self) -> List[Dict]:
        """
        Attempt to scrape Forex Factory calendar RSS feed.
        Returns structured event data if successful.
        """
        results = []
        try:
            resp = self._session.get(RSS_FEED_URL, timeout=15)
            if resp.status_code == 200:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(resp.text)
                for item in root.findall(".//item"):
                    title = item.findtext("title", "")
                    pub_date = item.findtext("pubDate", "")
                    description = item.findtext("description", "")
                    if title:
                        results.append({
                            "source": "forexfactory",
                            "title": title,
                            "date": pub_date,
                            "description": description,
                        })
            if results:
                logger.info(f"Fetched {len(results)} events from Forex Factory RSS")
        except Exception as e:
            logger.debug(f"Forex Factory RSS fetch skipped: {e}")
        return results

    def fetch_investing_calendar(self) -> List[Dict]:
        """
        Fallback attempt to get economic calendar from investing.com.
        Uses their lightweight mobile API endpoint.
        """
        results = []
        try:
            today = date.today()
            end_date = today + timedelta(days=30)
            url = (
                "https://www.investing.com/economic-calendar/Service/getCalendarFilteredData"
            )
            headers = {
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.investing.com/economic-calendar/",
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36"
                ),
            }
            resp = self._session.post(url, headers=headers, data={
                "dateFrom": today.strftime("%Y-%m-%d"),
                "dateTo": end_date.strftime("%Y-%m-%d"),
            }, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                for event in data.get("data", [])[:20]:
                    results.append({
                        "source": "investing.com",
                        "title": event.get("name", ""),
                        "date": event.get("date", ""),
                        "country": event.get("country", ""),
                        "impact": event.get("impact", ""),
                        "actual": event.get("actual", ""),
                        "forecast": event.get("forecast", ""),
                        "previous": event.get("previous", ""),
                    })
            if results:
                logger.info(f"Fetched {len(results)} events from Investing.com")
        except Exception as e:
            logger.debug(f"Investing.com fetch skipped: {e}")
        return results

    # ── Composite fetch ──

    def fetch_upcoming(self, days: int = 7) -> List[Dict]:
        """
        Fetch upcoming economic events from all available sources.

        Combines:
        1. Pre-built event database (filtered by date range)
        2. akshare live data (China macro)
        3. Web-sourced events (if available)

        Args:
            days: Number of days to look ahead.

        Returns:
            List of event dictionaries sorted by date and impact.
        """
        today = date.today()
        end_date = today + timedelta(days=days)

        events = []

        # 1. Pre-built database
        db_events = self._db.by_date_range(today, end_date)
        for e in db_events:
            events.append(e.to_dict())

        # 2. akshare live data
        live_data = self.fetch_cn_macro_calendar()
        for item in live_data:
            events.append({
                "event_id": f"live-{item.get('indicator', 'unknown')}",
                "title": item.get("title", "Unknown"),
                "date": today.isoformat(),
                "region": "CN",
                "category": item.get("indicator", "Other"),
                "impact": 3,
                "description": f"Live data: {item.get('value', 'N/A')}",
                "markets_impacted": ["A-share", "CN Bond", "FX"],
                "direction_bias": "data-dependent",
                "historical_volatility": "medium",
                "frequency": "monthly",
                "notes": f"Source: {item.get('source', 'akshare')}",
                "source": item.get("source", "akshare"),
            })

        # 3. Web sources (optional, lightweight)
        web_events = self.fetch_forex_factory()
        for item in web_events[:10]:
            events.append({
                "event_id": f"ff-{item.get('title', 'unknown')[:30]}",
                "title": item.get("title", "Unknown"),
                "date": today.isoformat(),
                "region": "US",
                "category": "Web",
                "impact": 2,
                "description": item.get("description", ""),
                "markets_impacted": ["US Equity", "FX"],
                "direction_bias": "data-dependent",
                "historical_volatility": "low",
                "frequency": "ad-hoc",
                "notes": f"Source: {item.get('source', 'web')}",
                "source": item.get("source", "web"),
            })

        # Deduplicate by title similarity (simple)
        seen = set()
        unique = []
        for e in events:
            key = e.get("title", "")[:50].lower().strip()
            if key not in seen:
                seen.add(key)
                unique.append(e)

        # Sort by date then impact (descending)
        unique.sort(key=lambda x: (x.get("date", ""), -x.get("impact", 0)))
        return unique

    def fetch_month(self, year: int, month: int) -> List[Dict]:
        """Fetch events for a specific month from the pre-built database."""
        return [e.to_dict() for e in self._db.by_month(year, month)]

    @staticmethod
    def check_akshare_available() -> bool:
        """Check if akshare is installed and functional."""
        try:
            import akshare as ak  # noqa: F401
            return True
        except ImportError:
            return False


def fetch_cn_macro() -> List[Dict]:
    """Convenience function: fetch China macro data via akshare."""
    fetcher = MacroFetcher()
    results = []
    results.extend(fetcher.fetch_cn_macro_calendar())
    results.extend(fetcher.fetch_cn_money_supply())
    return results


# ──────────────────────────────────────────────────────────
# Self-test
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    fetcher = MacroFetcher()
    print(f"akshare available: {MacroFetcher.check_akshare_available()}")
    print(f"\nUpcoming events (next 7 days):")
    upcoming = fetcher.fetch_upcoming(days=7)
    for evt in upcoming:
        impact_stars = "\u2605" * evt.get("impact", 0)
        print(f"  {evt['date']} | {impact_stars} | {evt['region']} | {evt['title']}")

    if MacroFetcher.check_akshare_available():
        print(f"\nChina live macro data:")
        cn_data = fetch_cn_macro()
        for item in cn_data:
            print(f"  {item['title']}: {item['value']}")

"""
Global Economic Events Calendar
================================

A comprehensive economic events calendar with market impact analysis
covering China (NBS, PBoC), United States (FOMC, BLS), European Union
(ECB, Eurostat), and Japan (BOJ, MoF).

Usage::

    from econ_calendar.events import get_events
    from econ_calendar.fetcher import fetch_cn_macro
    from econ_calendar.dashboard import generate_dashboard
"""

__version__ = "1.0.0"
__author__ = "Econ Calendar Contributors"
__license__ = "MIT"

from econ_calendar.events import EventDatabase, get_events, list_regions
from econ_calendar.fetcher import MacroFetcher, fetch_cn_macro
from econ_calendar.dashboard import DashboardGenerator, generate_dashboard

__all__ = [
    "EventDatabase",
    "get_events",
    "list_regions",
    "MacroFetcher",
    "fetch_cn_macro",
    "DashboardGenerator",
    "generate_dashboard",
]

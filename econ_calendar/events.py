"""
Pre-built Economic Events Database
====================================

50+ scheduled economic events for 2026 Q3-Q4 across four major regions:
China (CN), United States (US), European Union (EU), Japan (JP).

Each event carries:
- Date (actual or estimated based on historical release patterns)
- Impact rating: 1-5 stars (5 = highest market impact)
- Markets impacted: A-share, US equities, commodities, FX, bonds
- Direction bias: bullish / bearish / neutral / data-dependent
- Historical volatility context: low / medium / high
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional, Dict
from enum import Enum


class Region(str, Enum):
    CN = "CN"
    US = "US"
    EU = "EU"
    JP = "JP"
    GLOBAL = "GLOBAL"


class Market(str, Enum):
    A_SHARE = "A-share"
    US_EQUITY = "US Equity"
    CN_BOND = "CN Bond"
    US_BOND = "US Bond"
    COMMODITY = "Commodity"
    FX = "FX"
    GOLD = "Gold"
    OIL = "Oil"
    CRYPTO = "Crypto"


class Direction(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"
    DATA_DEPENDENT = "data-dependent"


@dataclass
class EconomicEvent:
    """A single economic event entry."""

    event_id: str
    title: str
    date: date
    region: Region
    category: str
    impact: int  # 1-5 stars
    description: str
    markets_impacted: List[str] = field(default_factory=list)
    direction_bias: str = "data-dependent"
    historical_volatility: str = "medium"
    frequency: str = "monthly"  # monthly, quarterly, ad-hoc
    notes: str = ""

    def to_dict(self) -> Dict:
        return {
            "event_id": self.event_id,
            "title": self.title,
            "date": self.date.isoformat(),
            "region": self.region.value if isinstance(self.region, Region) else self.region,
            "category": self.category,
            "impact": self.impact,
            "description": self.description,
            "markets_impacted": self.markets_impacted,
            "direction_bias": self.direction_bias,
            "historical_volatility": self.historical_volatility,
            "frequency": self.frequency,
            "notes": self.notes,
        }


# ──────────────────────────────────────────────────────────
# 2026 Q3-Q4 PRE-BUILT EVENTS (realistic schedule)
# ──────────────────────────────────────────────────────────

EVENTS: List[EconomicEvent] = [

    # ═══ JULY 2026 ═══
    # ── China ──
    EconomicEvent(
        event_id="CN-PMI-20260701",
        title="NBS Manufacturing & Non-Manufacturing PMI (Jun)",
        date=date(2026, 7, 1),
        region=Region.CN,
        category="PMI",
        impact=4,
        description="Official Purchasing Managers' Index for manufacturing and services sectors. A reading above 50 indicates expansion. A key leading indicator for China's economic momentum.",
        markets_impacted=[Market.A_SHARE, Market.COMMODITY, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
        notes="Released on the last day of the month or first day of the following month.",
    ),
    EconomicEvent(
        event_id="CN-CPI-20260709",
        title="NBS CPI & PPI (Jun)",
        date=date(2026, 7, 9),
        region=Region.CN,
        category="Inflation",
        impact=4,
        description="Consumer Price Index and Producer Price Index. CPI measures consumer inflation; PPI reflects factory-gate price changes. Critical for PBoC policy outlook.",
        markets_impacted=[Market.A_SHARE, Market.CN_BOND, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
        notes="Usually released around the 9th of each month.",
    ),
    EconomicEvent(
        event_id="CN-TRADE-20260713",
        title="China Trade Balance (Jun)",
        date=date(2026, 7, 13),
        region=Region.CN,
        category="Trade",
        impact=3,
        description="Monthly export, import values and trade surplus/deficit. A bellwether for global demand and China's external sector health.",
        markets_impacted=[Market.A_SHARE, Market.FX, Market.COMMODITY],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="medium",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-INDPROD-20260715",
        title="NBS Industrial Production, Retail Sales, FAI (Jun)",
        date=date(2026, 7, 15),
        region=Region.CN,
        category="Activity Data",
        impact=5,
        description="Monthly trio: industrial production (IP), retail sales, and fixed asset investment (FAI). The most comprehensive snapshot of China's real economy.",
        markets_impacted=[Market.A_SHARE, Market.COMMODITY, Market.CN_BOND, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
        notes="Released together around the 15th of each month.",
    ),
    EconomicEvent(
        event_id="CN-GDP-Q3-20260716",
        title="NBS Q2 GDP Growth Rate",
        date=date(2026, 7, 16),
        region=Region.CN,
        category="GDP",
        impact=5,
        description="Quarterly GDP growth (YoY and QoQ). The most-watched single number for China's economic trajectory. Also includes sector breakdown.",
        markets_impacted=[Market.A_SHARE, Market.COMMODITY, Market.FX, Market.CN_BOND],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="quarterly",
        notes="Q2 data released mid-July.",
    ),
    EconomicEvent(
        event_id="CN-LPR-20260720",
        title="PBoC Loan Prime Rate (LPR) Fixing",
        date=date(2026, 7, 20),
        region=Region.CN,
        category="Monetary Policy",
        impact=5,
        description="1-year and 5-year LPR rate decisions. The 5-year LPR serves as the reference for mortgage rates and heavily influences the property market.",
        markets_impacted=[Market.A_SHARE, Market.CN_BOND, Market.FX],
        direction_bias=Direction.NEUTRAL,
        historical_volatility="high",
        frequency="monthly",
        notes="Announced at 9:15 AM Beijing time on the 20th of each month (or next business day).",
    ),
    EconomicEvent(
        event_id="CN-MLF-20260715",
        title="PBoC Medium-term Lending Facility (MLF) Operation",
        date=date(2026, 7, 15),
        region=Region.CN,
        category="Monetary Policy",
        impact=4,
        description="MLF rate and volume. The MLF rate is the policy benchmark for the LPR. Changes signal PBoC's monetary stance.",
        markets_impacted=[Market.CN_BOND, Market.A_SHARE],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
        notes="Typically announced around the 15th of each month.",
    ),

    # ── US ──
    EconomicEvent(
        event_id="US-FOMC-20260729",
        title="FOMC Interest Rate Decision (July)",
        date=date(2026, 7, 29),
        region=Region.US,
        category="Monetary Policy",
        impact=5,
        description="Federal Open Market Committee decision on the federal funds rate. Includes the policy statement, dot plot projections, and Summary of Economic Projections (SEP). Jackson Hole and Powell press conference to follow.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD, Market.CRYPTO],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="ad-hoc",
        notes="Two-day meeting Jul 28-29. Decision at 2:00 PM ET, press conference at 2:30 PM ET.",
    ),
    EconomicEvent(
        event_id="US-CPI-20260714",
        title="US CPI (Jun) - Consumer Price Index",
        date=date(2026, 7, 14),
        region=Region.US,
        category="Inflation",
        impact=5,
        description="Headline and core CPI MoM/YoY. The single most important inflation print for Fed policy expectations. Core CPI (ex food & energy) is the market's focus.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="US-NFP-20260703",
        title="US Non-Farm Payrolls (Jun)",
        date=date(2026, 7, 3),
        region=Region.US,
        category="Employment",
        impact=5,
        description="Non-farm payrolls, unemployment rate, and average hourly earnings. The monthly employment report is the most comprehensive labor market snapshot.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
        notes="Released first Friday of each month at 8:30 AM ET.",
    ),
    EconomicEvent(
        event_id="US-PCE-20260731",
        title="US PCE Price Index (Jun) - Fed's Preferred Inflation Gauge",
        date=date(2026, 7, 31),
        region=Region.US,
        category="Inflation",
        impact=5,
        description="Personal Consumption Expenditures (PCE) price index - the Fed's preferred measure of inflation. Core PCE is closely watched for policy signals.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="US-RETAIL-20260716",
        title="US Retail Sales (Jun)",
        date=date(2026, 7, 16),
        region=Region.US,
        category="Consumption",
        impact=4,
        description="Monthly retail sales data including the control group (ex autos, gas, building materials). A direct gauge of consumer spending strength.",
        markets_impacted=[Market.US_EQUITY, Market.FX, Market.US_BOND],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="medium",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="US-GDP-Q2-20260730",
        title="US GDP Q2 2026 (Advance Estimate)",
        date=date(2026, 7, 30),
        region=Region.US,
        category="GDP",
        impact=5,
        description="Advance estimate of Q2 GDP growth (annualized QoQ). The first look at economic growth for the quarter.",
        markets_impacted=[Market.US_EQUITY, Market.FX, Market.US_BOND],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="quarterly",
    ),

    # ── EU ──
    EconomicEvent(
        event_id="ECB-20260723",
        title="ECB Monetary Policy Decision (July)",
        date=date(2026, 7, 23),
        region=Region.EU,
        category="Monetary Policy",
        impact=5,
        description="European Central Bank Governing Council interest rate decision. Includes the monetary policy statement and President Lagarde's press conference.",
        markets_impacted=[Market.FX, Market.US_EQUITY, Market.COMMODITY],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="ad-hoc",
        notes="Decision at 14:15 CET, press conference at 14:45 CET.",
    ),
    EconomicEvent(
        event_id="EU-CPI-20260717",
        title="Eurozone CPI (Jun, Final)",
        date=date(2026, 7, 17),
        region=Region.EU,
        category="Inflation",
        impact=4,
        description="Final harmonised CPI for the Eurozone. Confirms the flash estimate and provides detailed component breakdown.",
        markets_impacted=[Market.FX, Market.US_EQUITY],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="medium",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="EU-PMI-20260701",
        title="HCOB Eurozone Manufacturing PMI (Jun, Final)",
        date=date(2026, 7, 1),
        region=Region.EU,
        category="PMI",
        impact=3,
        description="Final S&P Global/HCOB Manufacturing PMI for the Eurozone. A diffusion index tracking manufacturing sector health.",
        markets_impacted=[Market.FX, Market.US_EQUITY],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="low",
        frequency="monthly",
    ),

    # ── Japan ──
    EconomicEvent(
        event_id="BOJ-20260716",
        title="BOJ Monetary Policy Meeting (July)",
        date=date(2026, 7, 16),
        region=Region.JP,
        category="Monetary Policy",
        impact=5,
        description="Bank of Japan interest rate decision and Outlook Report. Includes Governor Ueda's press conference. Markets closely watch for any hint of further rate normalization.",
        markets_impacted=[Market.FX, Market.US_EQUITY, Market.COMMODITY],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="ad-hoc",
        notes="Two-day meeting Jul 15-16. JPY carry trade implications make this globally significant.",
    ),
    EconomicEvent(
        event_id="JP-CPI-20260724",
        title="Japan National CPI (Jun)",
        date=date(2026, 7, 24),
        region=Region.JP,
        category="Inflation",
        impact=3,
        description="National Consumer Price Index including core CPI (ex fresh food) and core-core CPI (ex fresh food & energy).",
        markets_impacted=[Market.FX, Market.COMMODITY],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="medium",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="JP-TANKAN-20260701",
        title="BOJ Tankan Survey (Q2)",
        date=date(2026, 7, 1),
        region=Region.JP,
        category="Business Sentiment",
        impact=4,
        description="BOJ's quarterly Tankan survey of business conditions. The most comprehensive measure of Japanese corporate sentiment.",
        markets_impacted=[Market.FX, Market.A_SHARE],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="quarterly",
    ),

    # ═══ AUGUST 2026 ═══
    # ── China ──
    EconomicEvent(
        event_id="CN-PMI-20260803",
        title="NBS Manufacturing & Non-Manufacturing PMI (Jul)",
        date=date(2026, 8, 3),
        region=Region.CN,
        category="PMI",
        impact=4,
        description="Official PMI for July. The first major data point each month and a leading indicator for the Chinese economy.",
        markets_impacted=[Market.A_SHARE, Market.COMMODITY, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-CPI-20260810",
        title="NBS CPI & PPI (Jul)",
        date=date(2026, 8, 10),
        region=Region.CN,
        category="Inflation",
        impact=4,
        description="July CPI and PPI. PPI trends are crucial for industrial sector profitability assessment.",
        markets_impacted=[Market.A_SHARE, Market.CN_BOND, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-TRADE-20260807",
        title="China Trade Balance (Jul)",
        date=date(2026, 8, 7),
        region=Region.CN,
        category="Trade",
        impact=3,
        description="July trade data. Export growth trajectory is vital given tariff and trade policy uncertainties.",
        markets_impacted=[Market.A_SHARE, Market.FX, Market.COMMODITY],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="medium",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-INDPROD-20260814",
        title="NBS Industrial Production, Retail Sales, FAI (Jul)",
        date=date(2026, 8, 14),
        region=Region.CN,
        category="Activity Data",
        impact=5,
        description="July activity data trio. Industrial production, retail sales, and fixed asset investment.",
        markets_impacted=[Market.A_SHARE, Market.COMMODITY, Market.CN_BOND, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-LPR-20260820",
        title="PBoC Loan Prime Rate (LPR) Fixing",
        date=date(2026, 8, 20),
        region=Region.CN,
        category="Monetary Policy",
        impact=5,
        description="August LPR decision. A key signal for PBoC's policy direction and housing market support.",
        markets_impacted=[Market.A_SHARE, Market.CN_BOND, Market.FX],
        direction_bias=Direction.NEUTRAL,
        historical_volatility="high",
        frequency="monthly",
    ),

    # ── US ──
    EconomicEvent(
        event_id="US-CPI-20260812",
        title="US CPI (Jul) - Consumer Price Index",
        date=date(2026, 8, 12),
        region=Region.US,
        category="Inflation",
        impact=5,
        description="July CPI. The print ahead of the September FOMC meeting carries extra weight. Markets will gauge whether the Fed's inflation fight is working.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="US-NFP-20260807",
        title="US Non-Farm Payrolls (Jul)",
        date=date(2026, 8, 7),
        region=Region.US,
        category="Employment",
        impact=5,
        description="July employment report. The penultimate payrolls before the September FOMC meeting.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="US-JACKSON-20260827",
        title="Jackson Hole Economic Symposium",
        date=date(2026, 8, 27),
        region=Region.US,
        category="Central Bank",
        impact=5,
        description="Annual Federal Reserve Bank of Kansas City symposium. Fed Chair Powell's speech is often used to signal major policy shifts. A globally-watched event.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD, Market.A_SHARE],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="annual",
        notes="Aug 27-29. Powell typically speaks on Friday morning.",
    ),
    EconomicEvent(
        event_id="US-PCE-20260828",
        title="US PCE Price Index (Jul)",
        date=date(2026, 8, 28),
        region=Region.US,
        category="Inflation",
        impact=5,
        description="July PCE price index. Released during Jackson Hole week, adding to market volatility.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="US-RETAIL-20260814",
        title="US Retail Sales (Jul)",
        date=date(2026, 8, 14),
        region=Region.US,
        category="Consumption",
        impact=4,
        description="July retail sales. Consumer resilience is a key narrative for the 'soft landing' thesis.",
        markets_impacted=[Market.US_EQUITY, Market.FX, Market.US_BOND],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="medium",
        frequency="monthly",
    ),

    # ── EU ──
    EconomicEvent(
        event_id="EU-CPI-20260819",
        title="Eurozone CPI (Jul, Final)",
        date=date(2026, 8, 19),
        region=Region.EU,
        category="Inflation",
        impact=4,
        description="Final July Eurozone harmonised CPI. Service sector inflation is the ECB's current focus.",
        markets_impacted=[Market.FX, Market.US_EQUITY],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="medium",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="EU-GDP-Q2-20260814",
        title="Eurozone GDP Q2 2026 (Second Estimate)",
        date=date(2026, 8, 14),
        region=Region.EU,
        category="GDP",
        impact=4,
        description="Second estimate of Q2 GDP. Provides a more detailed breakdown of growth components.",
        markets_impacted=[Market.FX, Market.US_EQUITY],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="medium",
        frequency="quarterly",
    ),

    # ═══ SEPTEMBER 2026 ═══
    # ── China ──
    EconomicEvent(
        event_id="CN-PMI-20260901",
        title="NBS Manufacturing & Non-Manufacturing PMI (Aug)",
        date=date(2026, 9, 1),
        region=Region.CN,
        category="PMI",
        impact=4,
        description="August official PMI. First look at Q3 economic momentum.",
        markets_impacted=[Market.A_SHARE, Market.COMMODITY, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-CPI-20260909",
        title="NBS CPI & PPI (Aug)",
        date=date(2026, 9, 9),
        region=Region.CN,
        category="Inflation",
        impact=4,
        description="August CPI and PPI. Deflation concerns remain a key market theme for China.",
        markets_impacted=[Market.A_SHARE, Market.CN_BOND, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-INDPROD-20260914",
        title="NBS Industrial Production, Retail Sales, FAI (Aug)",
        date=date(2026, 9, 14),
        region=Region.CN,
        category="Activity Data",
        impact=5,
        description="August activity data. Mid-Q3 snapshot of economic performance.",
        markets_impacted=[Market.A_SHARE, Market.COMMODITY, Market.CN_BOND, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-LPR-20260921",
        title="PBoC Loan Prime Rate (LPR) Fixing",
        date=date(2026, 9, 21),
        region=Region.CN,
        category="Monetary Policy",
        impact=5,
        description="September LPR. The 20th falls on a Sunday, so announced on Monday the 21st.",
        markets_impacted=[Market.A_SHARE, Market.CN_BOND, Market.FX],
        direction_bias=Direction.NEUTRAL,
        historical_volatility="high",
        frequency="monthly",
    ),

    # ── US ──
    EconomicEvent(
        event_id="US-FOMC-20260916",
        title="FOMC Interest Rate Decision (September)",
        date=date(2026, 9, 16),
        region=Region.US,
        category="Monetary Policy",
        impact=5,
        description="September FOMC meeting with updated Summary of Economic Projections (SEP) and dot plot. One of the four 'big' meetings each year with fresh projections.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD, Market.CRYPTO],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="ad-hoc",
        notes="Two-day meeting Sep 15-16. Decision with dot plot at 2:00 PM ET.",
    ),
    EconomicEvent(
        event_id="US-CPI-20260911",
        title="US CPI (Aug)",
        date=date(2026, 9, 11),
        region=Region.US,
        category="Inflation",
        impact=5,
        description="August CPI. The final CPI print before the September FOMC meeting. Could be decisive for rate decision.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="US-NFP-20260904",
        title="US Non-Farm Payrolls (Aug)",
        date=date(2026, 9, 4),
        region=Region.US,
        category="Employment",
        impact=5,
        description="August employment report. The last payrolls before the September FOMC. Tremendous market sensitivity.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="US-PCE-20260930",
        title="US PCE Price Index (Aug)",
        date=date(2026, 9, 30),
        region=Region.US,
        category="Inflation",
        impact=5,
        description="August PCE. Post-FOMC inflation data for assessing the Fed's decision.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),

    # ── EU ──
    EconomicEvent(
        event_id="ECB-20260910",
        title="ECB Monetary Policy Decision (September)",
        date=date(2026, 9, 10),
        region=Region.EU,
        category="Monetary Policy",
        impact=5,
        description="ECB Governing Council decision. Includes updated staff macroeconomic projections.",
        markets_impacted=[Market.FX, Market.US_EQUITY, Market.COMMODITY],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="ad-hoc",
        notes="Meeting with updated projections. Press conference at 14:45 CET.",
    ),

    # ── Japan ──
    EconomicEvent(
        event_id="BOJ-20260918",
        title="BOJ Monetary Policy Meeting (September)",
        date=date(2026, 9, 18),
        region=Region.JP,
        category="Monetary Policy",
        impact=5,
        description="BOJ policy decision with Outlook Report update. Markets are watching for clues on the pace of rate normalization and JGB purchase tapering.",
        markets_impacted=[Market.FX, Market.US_EQUITY, Market.COMMODITY, Market.A_SHARE],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="ad-hoc",
        notes="Two-day meeting Sep 17-18.",
    ),

    # ── Global / Commodities ──
    EconomicEvent(
        event_id="OPEC-20260925",
        title="OPEC+ Joint Ministerial Monitoring Committee (JMMC)",
        date=date(2026, 9, 25),
        region=Region.GLOBAL,
        category="Energy",
        impact=4,
        description="OPEC+ monitoring committee reviews production quotas and compliance. Can recommend policy adjustments affecting global oil supply.",
        markets_impacted=[Market.OIL, Market.COMMODITY, Market.US_EQUITY, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="ad-hoc",
    ),

    # ═══ OCTOBER 2026 ═══
    # ── China ──
    EconomicEvent(
        event_id="CN-PMI-20260930",
        title="NBS Manufacturing & Non-Manufacturing PMI (Sep)",
        date=date(2026, 9, 30),
        region=Region.CN,
        category="PMI",
        impact=4,
        description="September official PMI. End-of-Q3 reading.",
        markets_impacted=[Market.A_SHARE, Market.COMMODITY, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-GOLDENWEEK-20261001",
        title="China National Day Golden Week Holiday",
        date=date(2026, 10, 1),
        region=Region.CN,
        category="Holiday",
        impact=3,
        description="One-week national holiday. Chinese markets closed. Consumption data (tourism, box office, retail) from Golden Week is closely watched as a gauge of consumer confidence.",
        markets_impacted=[Market.A_SHARE, Market.COMMODITY],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="low",
        frequency="annual",
        notes="Oct 1-7. A-share market closed. Key consumption metric: tourism revenue vs 2019 benchmark.",
    ),
    EconomicEvent(
        event_id="CN-CPI-20261012",
        title="NBS CPI & PPI (Sep)",
        date=date(2026, 10, 12),
        region=Region.CN,
        category="Inflation",
        impact=4,
        description="September inflation data, released after Golden Week.",
        markets_impacted=[Market.A_SHARE, Market.CN_BOND, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-TRADE-20261013",
        title="China Trade Balance (Sep)",
        date=date(2026, 10, 13),
        region=Region.CN,
        category="Trade",
        impact=3,
        description="September trade data. Post-Golden Week momentum assessment.",
        markets_impacted=[Market.A_SHARE, Market.FX, Market.COMMODITY],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="medium",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-GDP-Q3-20261018",
        title="NBS Q3 GDP Growth Rate",
        date=date(2026, 10, 18),
        region=Region.CN,
        category="GDP",
        impact=5,
        description="Q3 GDP data. The most important single release for assessing China's 2026 growth trajectory. Includes sectoral breakdowns.",
        markets_impacted=[Market.A_SHARE, Market.COMMODITY, Market.FX, Market.CN_BOND],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="quarterly",
        notes="Q3 GDP and September activity data released together.",
    ),
    EconomicEvent(
        event_id="CN-INDPROD-20261018",
        title="NBS Industrial Production, Retail Sales, FAI (Sep)",
        date=date(2026, 10, 18),
        region=Region.CN,
        category="Activity Data",
        impact=5,
        description="September activity data released alongside Q3 GDP. A data-heavy morning for China markets.",
        markets_impacted=[Market.A_SHARE, Market.COMMODITY, Market.CN_BOND, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-PLENUM-20261025",
        title="CCP Central Committee Plenary Session",
        date=date(2026, 10, 25),
        region=Region.CN,
        category="Policy",
        impact=5,
        description="Central Committee Plenum. Major policy announcements, economic reforms, and leadership decisions are typically unveiled. Markets watch for fiscal stimulus signals.",
        markets_impacted=[Market.A_SHARE, Market.CN_BOND, Market.FX, Market.COMMODITY],
        direction_bias=Direction.BULLISH,
        historical_volatility="high",
        frequency="annual",
        notes="Expected policy-heavy meeting. Historically a catalyst for A-share rallies.",
    ),
    EconomicEvent(
        event_id="CN-LPR-20261020",
        title="PBoC Loan Prime Rate (LPR) Fixing",
        date=date(2026, 10, 20),
        region=Region.CN,
        category="Monetary Policy",
        impact=5,
        description="October LPR. Post-GDP data, PBoC may adjust rates in response to Q3 economic performance.",
        markets_impacted=[Market.A_SHARE, Market.CN_BOND, Market.FX],
        direction_bias=Direction.NEUTRAL,
        historical_volatility="high",
        frequency="monthly",
    ),

    # ── US ──
    EconomicEvent(
        event_id="US-CPI-20261013",
        title="US CPI (Sep)",
        date=date(2026, 10, 13),
        region=Region.US,
        category="Inflation",
        impact=5,
        description="September CPI. Key input for the November FOMC meeting.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="US-NFP-20261002",
        title="US Non-Farm Payrolls (Sep)",
        date=date(2026, 10, 2),
        region=Region.US,
        category="Employment",
        impact=5,
        description="September employment. Q4-opening payroll data.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="US-GDP-Q3-20261029",
        title="US GDP Q3 2026 (Advance Estimate)",
        date=date(2026, 10, 29),
        region=Region.US,
        category="GDP",
        impact=5,
        description="Advance Q3 GDP estimate. The first read on Q3 growth, just one week before the presidential election.",
        markets_impacted=[Market.US_EQUITY, Market.FX, Market.US_BOND],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="quarterly",
    ),
    EconomicEvent(
        event_id="US-PCE-20261030",
        title="US PCE Price Index (Sep)",
        date=date(2026, 10, 30),
        region=Region.US,
        category="Inflation",
        impact=5,
        description="September PCE. The Fed's preferred inflation gauge just days before the FOMC and election.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),

    # ── EU ──
    EconomicEvent(
        event_id="ECB-20261029",
        title="ECB Monetary Policy Decision (October)",
        date=date(2026, 10, 29),
        region=Region.EU,
        category="Monetary Policy",
        impact=5,
        description="October ECB decision. No updated projections at this meeting, but policy statement and press conference remain market-moving.",
        markets_impacted=[Market.FX, Market.US_EQUITY, Market.COMMODITY],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="ad-hoc",
    ),

    # ── Japan ──
    EconomicEvent(
        event_id="BOJ-20261030",
        title="BOJ Monetary Policy Meeting (October)",
        date=date(2026, 10, 30),
        region=Region.JP,
        category="Monetary Policy",
        impact=5,
        description="October BOJ decision. No Outlook Report at this meeting, but policy statement and press conference will be parsed for normalization signals.",
        markets_impacted=[Market.FX, Market.US_EQUITY, Market.COMMODITY],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="ad-hoc",
        notes="Two-day meeting Oct 29-30.",
    ),

    # ── Global ──
    EconomicEvent(
        event_id="G20-20261022",
        title="G20 Finance Ministers & Central Bank Governors Meeting",
        date=date(2026, 10, 22),
        region=Region.GLOBAL,
        category="Summit",
        impact=3,
        description="G20 finance track meeting. Joint communique on global economic outlook, financial stability, and international tax cooperation.",
        markets_impacted=[Market.FX, Market.US_EQUITY, Market.COMMODITY],
        direction_bias=Direction.NEUTRAL,
        historical_volatility="low",
        frequency="ad-hoc",
    ),

    # ═══ NOVEMBER 2026 ═══
    # ── China ──
    EconomicEvent(
        event_id="CN-PMI-20261102",
        title="NBS Manufacturing & Non-Manufacturing PMI (Oct)",
        date=date(2026, 11, 2),
        region=Region.CN,
        category="PMI",
        impact=4,
        description="October official PMI. Post-Golden Week and Plenum-era activity reading.",
        markets_impacted=[Market.A_SHARE, Market.COMMODITY, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-CPI-20261110",
        title="NBS CPI & PPI (Oct)",
        date=date(2026, 11, 10),
        region=Region.CN,
        category="Inflation",
        impact=4,
        description="October inflation data. Food and energy price trends in focus.",
        markets_impacted=[Market.A_SHARE, Market.CN_BOND, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-INDPROD-20261116",
        title="NBS Industrial Production, Retail Sales, FAI (Oct)",
        date=date(2026, 11, 16),
        region=Region.CN,
        category="Activity Data",
        impact=5,
        description="October activity data. Key assessment of stimulus effectiveness post-Plenum.",
        markets_impacted=[Market.A_SHARE, Market.COMMODITY, Market.CN_BOND, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-SINGLESDAY-20261111",
        title="Singles' Day (11.11) Shopping Festival",
        date=date(2026, 11, 11),
        region=Region.CN,
        category="Consumption",
        impact=3,
        description="The world's largest online shopping event. GMV figures from Alibaba, JD.com, and PDD serve as a real-time consumer sentiment barometer for China.",
        markets_impacted=[Market.A_SHARE, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="medium",
        frequency="annual",
        notes="E-commerce stocks show elevated volatility in the week leading up to 11.11.",
    ),
    EconomicEvent(
        event_id="CN-LPR-20261120",
        title="PBoC Loan Prime Rate (LPR) Fixing",
        date=date(2026, 11, 20),
        region=Region.CN,
        category="Monetary Policy",
        impact=5,
        description="November LPR. Year-end policy assessment.",
        markets_impacted=[Market.A_SHARE, Market.CN_BOND, Market.FX],
        direction_bias=Direction.NEUTRAL,
        historical_volatility="high",
        frequency="monthly",
    ),

    # ── US ──
    EconomicEvent(
        event_id="US-FOMC-20261105",
        title="FOMC Interest Rate Decision (November)",
        date=date(2026, 11, 5),
        region=Region.US,
        category="Monetary Policy",
        impact=5,
        description="November FOMC meeting. Post-election meeting adds political dimension to market interpretation. No SEP/dot plot at this meeting.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD, Market.CRYPTO],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="ad-hoc",
        notes="Two-day meeting Nov 4-5. Held just after the US presidential election (Nov 3).",
    ),
    EconomicEvent(
        event_id="US-ELECTION-20261103",
        title="US Midterm Congressional Elections",
        date=date(2026, 11, 3),
        region=Region.US,
        category="Political",
        impact=5,
        description="2026 US midterm elections. All 435 House seats and 33 Senate seats are contested. Market implications for fiscal policy, regulation, and trade.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD, Market.CRYPTO, Market.A_SHARE],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="ad-hoc",
        notes="November 3, 2026. Historically, equity markets rally in the 12 months following midterms.",
    ),
    EconomicEvent(
        event_id="US-CPI-20261112",
        title="US CPI (Oct)",
        date=date(2026, 11, 12),
        region=Region.US,
        category="Inflation",
        impact=5,
        description="October CPI. Post-election inflation data. Market interpretation may be colored by election outcomes.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="US-NFP-20261106",
        title="US Non-Farm Payrolls (Oct)",
        date=date(2026, 11, 6),
        region=Region.US,
        category="Employment",
        impact=5,
        description="October employment data. Released in the immediate aftermath of the election and FOMC meeting.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="US-THANKSGIVING-20261126",
        title="US Thanksgiving Holiday",
        date=date(2026, 11, 26),
        region=Region.US,
        category="Holiday",
        impact=2,
        description="US markets closed Thursday. Half-day Friday (Black Friday). Low liquidity conditions can amplify volatility.",
        markets_impacted=[Market.US_EQUITY, Market.FX],
        direction_bias=Direction.NEUTRAL,
        historical_volatility="low",
        frequency="annual",
    ),

    # ── Global ──
    EconomicEvent(
        event_id="OPEC-20261128",
        title="OPEC+ Ministerial Meeting (Full)",
        date=date(2026, 11, 28),
        region=Region.GLOBAL,
        category="Energy",
        impact=5,
        description="Full OPEC+ ministerial meeting to set production policy for 2027. Decisions on quotas and voluntary cuts have direct impact on oil prices and inflation expectations globally.",
        markets_impacted=[Market.OIL, Market.COMMODITY, Market.US_EQUITY, Market.FX, Market.A_SHARE],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="ad-hoc",
        notes="End-of-year meeting sets production baseline for the following year.",
    ),

    # ═══ DECEMBER 2026 ═══
    # ── China ──
    EconomicEvent(
        event_id="CN-PMI-20261202",
        title="NBS Manufacturing & Non-Manufacturing PMI (Nov)",
        date=date(2026, 12, 2),
        region=Region.CN,
        category="PMI",
        impact=4,
        description="November official PMI. Late-year activity gauge.",
        markets_impacted=[Market.A_SHARE, Market.COMMODITY, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-CEWC-20261210",
        title="Central Economic Work Conference (CEWC)",
        date=date(2026, 12, 10),
        region=Region.CN,
        category="Policy",
        impact=5,
        description="China's most important annual economic policy meeting. Sets the GDP growth target, fiscal deficit ratio, and policy priorities for 2027. A major catalyst for A-shares.",
        markets_impacted=[Market.A_SHARE, Market.CN_BOND, Market.FX, Market.COMMODITY],
        direction_bias=Direction.BULLISH,
        historical_volatility="high",
        frequency="annual",
        notes="Dec 10-12. Readout expected Dec 12 evening. Historically a strong seasonal catalyst for A-shares.",
    ),
    EconomicEvent(
        event_id="CN-CPI-20261209",
        title="NBS CPI & PPI (Nov)",
        date=date(2026, 12, 9),
        region=Region.CN,
        category="Inflation",
        impact=4,
        description="November inflation data. The last CPI print before CEWC.",
        markets_impacted=[Market.A_SHARE, Market.CN_BOND, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-INDPROD-20261215",
        title="NBS Industrial Production, Retail Sales, FAI (Nov)",
        date=date(2026, 12, 15),
        region=Region.CN,
        category="Activity Data",
        impact=5,
        description="November activity data. Final comprehensive data release before year-end.",
        markets_impacted=[Market.A_SHARE, Market.COMMODITY, Market.CN_BOND, Market.FX],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="CN-LPR-20261221",
        title="PBoC Loan Prime Rate (LPR) Fixing",
        date=date(2026, 12, 21),
        region=Region.CN,
        category="Monetary Policy",
        impact=5,
        description="December LPR. The 20th falls on Sunday, pushed to Monday. Sets the tone for 2027 rate expectations.",
        markets_impacted=[Market.A_SHARE, Market.CN_BOND, Market.FX],
        direction_bias=Direction.NEUTRAL,
        historical_volatility="high",
        frequency="monthly",
    ),

    # ── US ──
    EconomicEvent(
        event_id="US-FOMC-20261216",
        title="FOMC Interest Rate Decision (December)",
        date=date(2026, 12, 16),
        region=Region.US,
        category="Monetary Policy",
        impact=5,
        description="December FOMC meeting with updated SEP and dot plot. The final meeting of 2026 sets the tone for 2027 rate expectations. Dot plot receives maximum attention.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD, Market.CRYPTO],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="ad-hoc",
        notes="Two-day meeting Dec 15-16. SEP and dot plot included.",
    ),
    EconomicEvent(
        event_id="US-CPI-20261210",
        title="US CPI (Nov)",
        date=date(2026, 12, 10),
        region=Region.US,
        category="Inflation",
        impact=5,
        description="November CPI. The last CPI print before the December FOMC. Extremely high market sensitivity.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="US-NFP-20261204",
        title="US Non-Farm Payrolls (Nov)",
        date=date(2026, 12, 4),
        region=Region.US,
        category="Employment",
        impact=5,
        description="November employment report. Final payrolls of 2026. Holiday hiring effects and year-end labor market snapshot.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="US-PCE-20261223",
        title="US PCE Price Index (Nov)",
        date=date(2026, 12, 23),
        region=Region.US,
        category="Inflation",
        impact=5,
        description="November PCE. Released just before Christmas. Low holiday liquidity can amplify market reactions to surprises.",
        markets_impacted=[Market.US_EQUITY, Market.US_BOND, Market.FX, Market.GOLD],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="monthly",
    ),
    EconomicEvent(
        event_id="US-QUADWITCH-20261218",
        title="US Quadruple Witching Day",
        date=date(2026, 12, 18),
        region=Region.US,
        category="Derivatives",
        impact=4,
        description="Simultaneous expiration of stock index futures, stock index options, stock options, and single stock futures. Highest trading volume day of the quarter.",
        markets_impacted=[Market.US_EQUITY],
        direction_bias=Direction.NEUTRAL,
        historical_volatility="high",
        frequency="quarterly",
    ),

    # ── EU ──
    EconomicEvent(
        event_id="ECB-20261217",
        title="ECB Monetary Policy Decision (December)",
        date=date(2026, 12, 17),
        region=Region.EU,
        category="Monetary Policy",
        impact=5,
        description="December ECB decision with updated staff macroeconomic projections through 2029. Sets the tone for 2027 policy path.",
        markets_impacted=[Market.FX, Market.US_EQUITY, Market.COMMODITY],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="ad-hoc",
        notes="Meeting with updated projections.",
    ),

    # ── Japan ──
    EconomicEvent(
        event_id="BOJ-20261218",
        title="BOJ Monetary Policy Meeting (December)",
        date=date(2026, 12, 18),
        region=Region.JP,
        category="Monetary Policy",
        impact=5,
        description="December BOJ decision with Outlook Report. The final policy meeting of 2026. Market focus on 2027 rate path and JGB purchase plan.",
        markets_impacted=[Market.FX, Market.US_EQUITY, Market.COMMODITY, Market.A_SHARE],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="ad-hoc",
        notes="Two-day meeting Dec 17-18.",
    ),
    EconomicEvent(
        event_id="JP-TANKAN-20261214",
        title="BOJ Tankan Survey (Q3)",
        date=date(2026, 12, 14),
        region=Region.JP,
        category="Business Sentiment",
        impact=4,
        description="BOJ Q3 Tankan. Final Tankan of 2026. Capex plans for FY2026 are a key focus.",
        markets_impacted=[Market.FX, Market.A_SHARE],
        direction_bias=Direction.DATA_DEPENDENT,
        historical_volatility="high",
        frequency="quarterly",
    ),

    # ── Global ──
    EconomicEvent(
        event_id="CHRISTMAS-20261225",
        title="Christmas Holiday - Global Markets Closed",
        date=date(2026, 12, 25),
        region=Region.GLOBAL,
        category="Holiday",
        impact=2,
        description="Christmas Day. Most global markets closed or half-day. Extremely low liquidity.",
        markets_impacted=[Market.US_EQUITY, Market.FX, Market.A_SHARE],
        direction_bias=Direction.NEUTRAL,
        historical_volatility="low",
        frequency="annual",
    ),
    EconomicEvent(
        event_id="NEWYEAR-20261231",
        title="New Year's Eve - Year-End Positioning",
        date=date(2026, 12, 31),
        region=Region.GLOBAL,
        category="Holiday",
        impact=3,
        description="Year-end portfolio rebalancing and window dressing. Thin liquidity can cause exaggerated moves.",
        markets_impacted=[Market.US_EQUITY, Market.FX, Market.A_SHARE],
        direction_bias=Direction.NEUTRAL,
        historical_volatility="medium",
        frequency="annual",
    ),
]


# ──────────────────────────────────────────────────────────
# Event Database Class
# ──────────────────────────────────────────────────────────

class EventDatabase:
    """Query interface for the pre-built economic events database."""

    def __init__(self, events: Optional[List[EconomicEvent]] = None):
        self._events = events or EVENTS
        self._index = {e.event_id: e for e in self._events}

    @property
    def events(self) -> List[EconomicEvent]:
        return list(self._events)

    def by_region(self, region: str) -> List[EconomicEvent]:
        """Filter events by region code (CN/US/EU/JP/GLOBAL)."""
        r = Region(region.upper())
        return [e for e in self._events if e.region == r]

    def by_date_range(self, start: date, end: date) -> List[EconomicEvent]:
        """Filter events within a date range."""
        return [e for e in self._events if start <= e.date <= end]

    def by_impact(self, min_impact: int) -> List[EconomicEvent]:
        """Filter events with impact rating >= min_impact."""
        return [e for e in self._events if e.impact >= min_impact]

    def by_category(self, category: str) -> List[EconomicEvent]:
        """Filter events by category."""
        cat_lower = category.lower()
        return [e for e in self._events if cat_lower in e.category.lower()]

    def upcoming(self, ref_date: Optional[date] = None, days: int = 7) -> List[EconomicEvent]:
        """Get events in the next N days from reference date."""
        ref = ref_date or date.today()
        end = date(ref.year, ref.month, ref.day)
        # Simple approach: use ref_date through ref_date + timedelta(days)
        from datetime import timedelta
        end_date = ref + timedelta(days=days)
        return sorted(
            [e for e in self._events if ref <= e.date <= end_date],
            key=lambda e: (e.date, -e.impact),
        )

    def by_month(self, year: int, month: int) -> List[EconomicEvent]:
        """Get all events for a specific month."""
        return sorted(
            [e for e in self._events if e.date.year == year and e.date.month == month],
            key=lambda e: (e.date, -e.impact),
        )

    def get(self, event_id: str) -> Optional[EconomicEvent]:
        """Get a specific event by ID."""
        return self._index.get(event_id)

    def to_dict_list(self) -> List[Dict]:
        """Export all events as a list of dictionaries."""
        return [e.to_dict() for e in self._events]

    def summary(self) -> Dict:
        """Get summary statistics."""
        regions = {}
        impacts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        categories = {}
        for e in self._events:
            r = e.region.value if isinstance(e.region, Region) else e.region
            regions[r] = regions.get(r, 0) + 1
            impacts[e.impact] = impacts.get(e.impact, 0) + 1
            categories[e.category] = categories.get(e.category, 0) + 1
        return {
            "total_events": len(self._events),
            "by_region": regions,
            "by_impact": impacts,
            "by_category": categories,
        }


# ──────────────────────────────────────────────────────────
# Convenience Functions
# ──────────────────────────────────────────────────────────

_db = EventDatabase()


def get_events(**filters) -> List[Dict]:
    """Get events with optional filters (region, start, end, min_impact, category).

    Returns a list of event dictionaries.
    """
    events = list(_db.events)

    if "region" in filters:
        r = Region(filters["region"].upper())
        events = [e for e in events if e.region == r]
    if "start" in filters:
        events = [e for e in events if e.date >= filters["start"]]
    if "end" in filters:
        events = [e for e in events if e.date <= filters["end"]]
    if "min_impact" in filters:
        events = [e for e in events if e.impact >= filters["min_impact"]]
    if "category" in filters:
        cat = filters["category"].lower()
        events = [e for e in events if cat in e.category.lower()]

    events.sort(key=lambda e: (e.date, -e.impact))
    return [e.to_dict() for e in events]


def list_regions() -> List[str]:
    """Return list of available region codes."""
    return [r.value for r in Region]

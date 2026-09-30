#!/usr/bin/env python3
"""Refresh data/mmri.json with the current DXY and US 10-year Treasury yield.

Run hourly by .github/workflows/mmri.yml. Standard library only, so the
workflow needs no pip install step.

The MMRI itself (DXY x US10Y / 1.61) is computed by the page; this only has
to store the two inputs honestly. Three sources are tried in order and every
value is sanity-checked, because a wrong number here is worse than a stale
one: the page already has a "last close / last update" badge that tells the
truth about age, and nothing tells the truth about a bad figure.

Exit codes: 0 = wrote a fresh reading, or nothing needed doing.
            1 = could not get a trustworthy pair (nothing written).
"""

import json
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
    EASTERN = ZoneInfo("America/New_York")
except Exception:  # no tzdata on the runner — fall back to a fixed EDT offset
    EASTERN = timezone(timedelta(hours=-4))

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "mmri.json"

MAX_HISTORY = 2000
DEDUPE_MINUTES = 50

# Sanity bounds. Outside these, assume the source broke rather than that the
# world did; the DXY has not been below 70 or above 165 in fifty years.
DXY_RANGE = (70.0, 140.0)
Y10_RANGE = (0.2, 12.0)

UA = "magickmica-mmri/1.0 (+https://magickmica.github.io/risk-indicator.html)"
TIMEOUT = 20


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


def note(msg):
    print(msg, file=sys.stderr)


# ── sources ────────────────────────────────────────────────────────────────
# Each returns a float or None. None means "this source had nothing for me",
# never "the value is zero".

def yahoo(symbol):
    """Yahoo's chart endpoint. Intraday, no key. Occasionally rate-limits."""
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/"
           f"{urllib.parse.quote(symbol)}?interval=1d&range=5d")
    try:
        meta = json.loads(get(url))["chart"]["result"][0]["meta"]
    except Exception as e:
        note(f"  yahoo {symbol}: {e}")
        return None
    for key in ("regularMarketPrice", "previousClose", "chartPreviousClose"):
        v = meta.get(key)
        if isinstance(v, (int, float)) and v > 0:
            return float(v)
    return None


def stooq(symbol):
    """Stooq's CSV quote. Columns: Symbol,Date,Time,Open,High,Low,Close."""
    url = f"https://stooq.com/q/l/?s={symbol}&f=sd2t2ohlc&h&e=csv"
    try:
        rows = [r for r in get(url).strip().splitlines() if r.strip()]
        close = rows[1].split(",")[-1]
        return float(close)
    except Exception as e:
        note(f"  stooq {symbol}: {e}")
        return None


def fred_latest(series):
    """Newest usable observation from FRED's keyless CSV export.

    FRED writes "." for a missing observation, so rows are walked newest
    first until one parses.
    """
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
    rows = [r for r in get(url).strip().splitlines() if r.strip()]
    for row in reversed(rows[1:]):
        parts = row.split(",")
        if len(parts) < 2:
            continue
        try:
            return float(parts[1]), parts[0]
        except ValueError:
            continue
    raise ValueError(f"{series}: no usable observation")


def treasury_debt():
    """Total public debt outstanding, in dollars, from the Treasury's own
    daily figure. No key, updated every business day."""
    url = ("https://api.fiscaldata.treasury.gov/services/api/fi/v1/accounting/"
           "od/debt_to_penny?sort=-record_date&page%5Bsize%5D=1&format=json")
    rec = json.loads(get(url))["data"][0]
    return float(rec["tot_pub_debt_out_amt"]), rec["record_date"]


def debt_to_gdp():
    """Federal debt as a share of GDP, as the MMMRI's fourth input.

    Computed the way Mannarino's own page does it — the Treasury's daily debt
    figure over the latest nominal GDP — rather than from FRED's quarterly
    published ratio, which lags by a quarter and currently reads about seven
    points lower. Falls back to that published ratio, and then to whatever
    the file already held, because a stale ratio is far better than none:
    it moves a fraction of a point a week.
    """
    try:
        debt, debt_date = treasury_debt()
        gdp_bn, gdp_date = fred_latest("GDP")     # billions, annualised
        ratio = debt / (gdp_bn * 1e9)
        if 0.5 <= ratio <= 3.0:
            note(f"  debt/GDP: {ratio * 100:.1f}% "
                 f"(Treasury {debt_date} \u00f7 GDP {gdp_date})")
            return round(ratio, 4)
        note(f"  debt/GDP: computed {ratio:.3f}, outside 0.5-3.0 \u2014 ignoring")
    except Exception as e:
        note(f"  debt/GDP live: {e}")

    try:
        pct, when = fred_latest("GFDEGDQ188S")    # the published ratio, percent
        if 30.0 <= pct <= 400.0:
            note(f"  debt/GDP: {pct}% of GDP (FRED published, {when})")
            return round(pct / 100.0, 4)
    except Exception as e:
        note(f"  debt/GDP published: {e}")

    return None


def treasury_10y():
    """The official daily par yield curve. Authoritative but once-a-day,
    published around 3:30pm ET, so it is the backstop rather than the lead."""
    today = datetime.now(timezone.utc)
    for month in (today, today - timedelta(days=28)):
        url = ("https://home.treasury.gov/resource-center/data-chart-center/"
               "interest-rates/pages/xml?data=daily_treasury_yield_curve"
               f"&field_tdr_date_value_month={month:%Y%m}")
        try:
            xml = get(url)
        except Exception as e:
            note(f"  treasury {month:%Y-%m}: {e}")
            continue
        hits = re.findall(r"<d:BC_10YEAR[^>]*>([\d.]+)</d:BC_10YEAR>", xml)
        if hits:
            return float(hits[-1])
    return None


def first_sane(label, bounds, candidates):
    """Take the first candidate that is a number inside the bounds."""
    lo, hi = bounds
    for name, fn in candidates:
        v = fn()
        if v is None:
            continue
        if lo <= v <= hi:
            note(f"  {label}: {v} (from {name})")
            return v, name
        note(f"  {label}: rejected {v} from {name} — outside {lo}-{hi}")
    return None, None


# ── the reading ────────────────────────────────────────────────────────────

def read_existing():
    try:
        d = json.loads(OUT.read_text(encoding="utf-8"))
        if isinstance(d.get("history"), list):
            return d
    except Exception:
        pass
    return {"history": []}


def main():
    note("Fetching DXY...")
    dxy, dxy_src = first_sane("DXY", DXY_RANGE, [
        ("Yahoo DX-Y.NYB", lambda: yahoo("DX-Y.NYB")),
        ("Stooq dx.f", lambda: stooq("dx.f")),
    ])

    note("Fetching US 10-year yield...")
    # ^TNX is quoted as the yield times ten: 42.6 means 4.26%.
    y10, y10_src = first_sane("US10Y", Y10_RANGE, [
        ("Yahoo ^TNX", lambda: (lambda v: v / 10 if v and v > 12 else v)(yahoo("^TNX"))),
        ("Stooq 10usy.b", lambda: stooq("10usy.b")),
        ("US Treasury", treasury_10y),
    ])

    if dxy is None or y10 is None:
        note("No trustworthy pair this run — leaving the file untouched.")
        return 1

    dxy = round(dxy, 3)
    y10 = round(y10, 3)
    now = datetime.now(EASTERN)
    stamp = now.isoformat(timespec="seconds")
    source = dxy_src if dxy_src == y10_src else f"{dxy_src} / {y10_src}"

    # Quarterly, so keep the previous value when the fetch comes back empty
    # rather than dropping the field and breaking the MMMRI.
    data_seed = read_existing()
    note("Fetching debt-to-GDP...")
    gdp = debt_to_gdp() or data_seed.get("debt_gdp")

    data = data_seed
    hist = data["history"]
    entry = {"t": stamp, "dxy": dxy, "us10y": y10}

    # If the market has not moved since the last reading, replace that reading
    # rather than stacking identical points on the chart.
    if hist:
        last = hist[-1]
        try:
            age = now - datetime.fromisoformat(last["t"])
            same = last.get("dxy") == dxy and last.get("us10y") == y10
            if same and age < timedelta(minutes=DEDUPE_MINUTES):
                hist[-1] = entry
            else:
                hist.append(entry)
        except Exception:
            hist.append(entry)
    else:
        hist.append(entry)

    out = {
        "updated": stamp,
        "dxy": dxy,
        "us10y": y10,
        "source": source,
        "history": hist[-MAX_HISTORY:],
    }
    if gdp:
        out["debt_gdp"] = gdp
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, separators=(",", ":")) + "\n", encoding="utf-8")
    mmri = dxy * y10 / 1.61
    line = f"Wrote {OUT.relative_to(ROOT)}: MMRI = {mmri:.1f}"
    if gdp:
        line += f", MMMRI = {mmri * gdp:.1f}"
    note(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())

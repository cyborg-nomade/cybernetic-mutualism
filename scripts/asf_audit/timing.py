"""Calendar intervals, response horizons, and the complete-day washout."""

from __future__ import annotations

from datetime import UTC, date, datetime, time, timedelta

from scripts.asf_audit.protocol import HORIZONS, RULES, Row


def event_date(value: str) -> date:
    """Normalize offset timestamps to UTC dates; date-only values stay dates."""
    if "T" not in value:
        return date.fromisoformat(value)
    return timestamp(value).date()


def timestamp(value: str) -> datetime:
    """Require timezone-aware timestamps and normalize them to UTC."""
    result = datetime.fromisoformat(value)
    if result.tzinfo is None:
        raise ValueError("Timestamp must include a UTC offset")
    return result.astimezone(UTC)


def interval(earliest: str, latest: str) -> tuple[date, date] | None:
    """Read an inclusive interval or a wholly unknown interval."""
    if earliest == latest == "unknown":
        return None
    result = event_date(earliest), event_date(latest)
    if result[0] > result[1]:
        raise ValueError("Reversed event interval")
    return result


def horizon_result(row: Row) -> dict[str, str | int | None]:
    """Calculate order and interval lags without forward-filling dispositions."""
    days = int(row["horizon"])
    if days not in HORIZONS:
        raise ValueError("Unregistered horizon")
    sender = interval(row["sender_earliest"], row["sender_latest"])
    receiver = interval(row["receiver_earliest"], row["receiver_latest"])
    if sender is None or receiver is None:
        return {
            "order": "unknown",
            "minimum_lag": None,
            "maximum_lag": None,
            "status": "unknown",
        }
    minimum = (receiver[0] - sender[1]).days
    maximum = (receiver[1] - sender[0]).days
    order = temporal_order(sender, receiver, row["within_day_order"])
    if minimum > days:
        status = "beyond"
    elif order not in ("sender_first", "documented_within_day_order"):
        status = "unknown" if order == "unknown" else "reversed"
    else:
        status = "within" if maximum <= days else "unknown"
    return {
        "order": order,
        "minimum_lag": minimum,
        "maximum_lag": maximum,
        "status": status,
    }


def temporal_order(
    sender: tuple[date, date],
    receiver: tuple[date, date],
    within_day: str,
) -> str:
    """Treat a within-day sequence as established only on the same exact day."""
    if sender[1] < receiver[0]:
        return "sender_first"
    if receiver[1] < sender[0]:
        return "receiver_first"
    if sender[0] == sender[1] == receiver[0] == receiver[1] and within_day == "yes":
        return "documented_within_day_order"
    return "unknown"


def primary_interval(earliest: str, latest: str) -> bool:
    """Require the whole possible onset interval to lie in the primary window."""
    dates = interval(earliest, latest)
    return dates is not None and (
        RULES["primary_start"] <= dates[0] <= dates[1] <= RULES["primary_end"]
    )


def recode_not_before(lock: str) -> datetime:
    """Wait fourteen full UTC calendar days, excluding a partial lock day."""
    locked = timestamp(lock)
    start = datetime.combine(locked.date(), time.min, tzinfo=UTC)
    if locked > start:
        start += timedelta(days=1)
    return start + timedelta(days=RULES["solo_recode_washout_days"])


def authority_shift(before: str, after: str) -> str:
    """Map only the documented binding-authority transitions in the codebook."""
    known = {
        "pmc_binding",
        "foundation_case_specific_authorization",
        "shared_authorization",
    }
    if before not in known or after not in known:
        return "unknown"
    if before == after:
        return "unchanged"
    return {
        "pmc_binding": "toward_pmc",
        "foundation_case_specific_authorization": "toward_foundation",
        "shared_authorization": "toward_shared",
    }[after]

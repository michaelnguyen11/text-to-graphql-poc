"""Load sample JSON data for the GraphQL facade."""

import json
import logging
from pathlib import Path
from typing import Any

from src.config import settings

logger = logging.getLogger(__name__)

# In-memory data store
_customer_info: list[dict[str, Any]] = []
_finance_profiles: list[dict[str, Any]] = []
_data_loaded = False


def load_data(data_dir: Path | None = None) -> None:
    """Load sample JSON data into memory."""
    global _customer_info, _finance_profiles, _data_loaded

    data_dir = data_dir or settings.data_path

    # Load customer info
    customer_file = data_dir / "ai_frontline_customer_info.json"
    if customer_file.exists():
        with open(customer_file, encoding="utf-8") as f:
            data = json.load(f)
            _customer_info = data.get("customer_info", [])
        logger.info("Loaded %d customer info records", len(_customer_info))

    # Load finance profiles
    finance_file = data_dir / "ai_frontline_finance_profile.json"
    if finance_file.exists():
        with open(finance_file, encoding="utf-8") as f:
            data = json.load(f)
            _finance_profiles = data.get("finance_profile", [])
        logger.info("Loaded %d finance profile records", len(_finance_profiles))

    _data_loaded = True


def ensure_loaded() -> None:
    """Ensure data is loaded."""
    if not _data_loaded:
        load_data()


def get_all_customers() -> list[dict[str, Any]]:
    """Get all customer info records."""
    ensure_loaded()
    return _customer_info


def get_customer_by_id(customer_id: str) -> dict[str, Any] | None:
    """Get customer info by ID."""
    ensure_loaded()
    for c in _customer_info:
        if c.get("customer_id", "").lower() == customer_id.lower():
            return c
    return None


def get_customer_by_name(name: str) -> list[dict[str, Any]]:
    """Get customers matching a name (case-insensitive, partial match)."""
    ensure_loaded()
    name_lower = name.lower().strip()
    results = []
    for c in _customer_info:
        cname = c.get("customer_name", "").lower()
        if name_lower in cname or cname in name_lower:
            results.append(c)
    return results


def get_finance_profile_latest(customer_id: str) -> dict[str, Any] | None:
    """Get the latest finance profile for a customer."""
    ensure_loaded()
    customer_profiles = [
        p for p in _finance_profiles
        if p.get("customer_id", "").lower() == customer_id.lower()
    ]
    if not customer_profiles:
        return None

    # Sort by date_key (DD/MM/YYYY format) and get latest
    def parse_date(date_str: str) -> tuple:
        parts = date_str.split("/")
        if len(parts) == 3:
            return (int(parts[2]), int(parts[1]), int(parts[0]))
        return (0, 0, 0)

    customer_profiles.sort(key=lambda p: parse_date(p.get("date_key", "01/01/1900")), reverse=True)
    return customer_profiles[0]


def get_finance_profiles_series(customer_id: str, months: int = 3) -> list[dict[str, Any]]:
    """Get a series of finance profiles for a customer, ordered by date."""
    ensure_loaded()
    customer_profiles = [
        p for p in _finance_profiles
        if p.get("customer_id", "").lower() == customer_id.lower()
    ]

    def parse_date(date_str: str) -> tuple:
        parts = date_str.split("/")
        if len(parts) == 3:
            return (int(parts[2]), int(parts[1]), int(parts[0]))
        return (0, 0, 0)

    customer_profiles.sort(key=lambda p: parse_date(p.get("date_key", "01/01/1900")))
    return customer_profiles[-months:]

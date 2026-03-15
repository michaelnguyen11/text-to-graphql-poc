"""Strawberry GraphQL schema for the banking data facade."""

from enum import Enum
import strawberry
from datetime import date
from typing import Optional

from src.graphql_facade import data_loader


# --- Enums ---

@strawberry.enum
class CustomerResolveStatus(Enum):
    RESOLVED = "RESOLVED"
    AMBIGUOUS = "AMBIGUOUS"
    NOT_FOUND = "NOT_FOUND"


@strawberry.enum
class FinanceMetric(Enum):
    AUM_EOP = "AUM_EOP"
    AUM_AVG_LAST_3M = "AUM_AVG_LAST_3M"
    CASA_EOP = "CASA_EOP"
    TD_EOP = "TD_EOP"
    TOTAL_ASSETS = "TOTAL_ASSETS"
    TOTAL_LIABILITIES = "TOTAL_LIABILITIES"
    NET_MONTHLY_INCOME = "NET_MONTHLY_INCOME"


@strawberry.enum
class TrendDirection(Enum):
    UP = "UP"
    DOWN = "DOWN"
    FLAT = "FLAT"
    UNKNOWN = "UNKNOWN"


# --- Types ---

@strawberry.type
class CustomerRef:
    customer_id: str
    customer_name: str
    rm_id: Optional[str] = None
    tier: Optional[str] = None
    confidence: Optional[float] = None


@strawberry.type
class CustomerResolveResult:
    status: str
    candidates: list[CustomerRef]


@strawberry.type
class CustomerInfo:
    customer_id: str
    customer_name: str
    rm_id: Optional[str] = None
    age: Optional[int] = None
    age_group: Optional[str] = None
    occupation: Optional[str] = None
    nationality: Optional[str] = None
    gender: Optional[str] = None
    tier: Optional[str] = None
    sub_tier: Optional[str] = None
    program_code: Optional[str] = None
    lavender_group: Optional[str] = None
    risk_appetite: Optional[str] = None
    cic_score: Optional[int] = None
    economic_segment: Optional[str] = None
    marketing_segment: Optional[str] = None
    tactical_segment: Optional[str] = None
    customer_journey: Optional[str] = None
    customer_persona: Optional[str] = None
    investment_needs_persona: Optional[str] = None
    professional_investor_flag: Optional[bool] = None
    customer_since: Optional[str] = None
    membership_effective_date: Optional[str] = None
    membership_review_date: Optional[str] = None
    membership_expiration_date: Optional[str] = None
    managing_branch: Optional[str] = None
    family_member_count: Optional[int] = None


@strawberry.type
class FinanceProfileLatest:
    customer_id: str
    date_key: str
    aum_eop_amount: Optional[float] = None
    aum_avg_last_3m_amount: Optional[float] = None
    casa_eop_amount: Optional[float] = None
    td_eop_amount: Optional[float] = None
    cd_max_eop_amount: Optional[float] = None
    bond_eop_amount: Optional[float] = None
    fund_eop_amount: Optional[float] = None
    ape_ytd_amount: Optional[float] = None
    total_asset_value_amount: Optional[float] = None
    total_liabilities_value_amount: Optional[float] = None
    net_assets_value_amount: Optional[float] = None
    total_casa_at_tcb_eop_amount: Optional[float] = None
    total_liquid_asset_at_tcb_amount: Optional[float] = None
    total_shared_capital_asset_value_amount: Optional[float] = None
    total_fixed_asset_value_amount: Optional[float] = None
    total_mortgage_and_auto_eop_amount: Optional[float] = None
    total_unsecured_loan_at_tcb_amount: Optional[float] = None
    total_secured_loan_amount: Optional[float] = None
    secured_lending_eop_amount: Optional[float] = None
    unsecured_lending_eop_amount: Optional[float] = None
    lending_credit_card_eop_amount: Optional[float] = None
    mycash_eop_amount: Optional[float] = None
    product_used_count: Optional[int] = None
    total_monthly_salary_income_amount: Optional[float] = None
    total_monthly_real_estate_rental_income_amount: Optional[float] = None
    total_monthly_car_rental_income_amount: Optional[float] = None
    total_monthly_entrepreneurial_income_amount: Optional[float] = None
    total_monthly_other_income_amount: Optional[float] = None
    total_monthly_income_amount: Optional[float] = None
    total_monthly_fixed_expense_amount: Optional[float] = None
    total_monthly_medical_expense_amount: Optional[float] = None
    total_monthly_education_expense_amount: Optional[float] = None
    total_monthly_holiday_expense_amount: Optional[float] = None
    total_monthly_other_expense_amount: Optional[float] = None
    total_monthly_expense_amount: Optional[float] = None
    net_monthly_income_amount: Optional[float] = None
    nbo_1: Optional[str] = None
    nbo_1_explanation: Optional[str] = None
    nbo_2: Optional[str] = None
    nbo_2_explanation: Optional[str] = None
    nbo_3: Optional[str] = None
    nbo_3_explanation: Optional[str] = None


@strawberry.type
class FinancePoint:
    month: str
    date_key: Optional[str] = None
    value: Optional[float] = None


@strawberry.type
class FinanceMetricSeriesResult:
    customer_id: str
    metric: str
    months: int
    points: list[FinancePoint]
    trend_direction: str


@strawberry.type
class CustomerOverview:
    customer: CustomerRef
    customer_info: Optional[CustomerInfo] = None
    finance_latest: Optional[FinanceProfileLatest] = None


# --- Helpers ---

def _derive_age(dob_str: str | None) -> int | None:
    """Derive age from date_of_birth string (DD/MM/YYYY)."""
    if not dob_str:
        return None
    try:
        parts = dob_str.split("/")
        birth = date(int(parts[2]), int(parts[1]), int(parts[0]))
        today = date.today()
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    except (IndexError, ValueError):
        return None


def _map_customer_info(raw: dict) -> CustomerInfo:
    """Map raw customer info dict to GraphQL type."""
    return CustomerInfo(
        customer_id=raw.get("customer_id", ""),
        customer_name=raw.get("customer_name", ""),
        rm_id=raw.get("rm_id"),
        age=_derive_age(raw.get("date_of_birth")),
        age_group=raw.get("age_group"),
        occupation=raw.get("occupation"),
        nationality=raw.get("nationality"),
        gender=raw.get("gender"),
        tier=raw.get("tier"),
        sub_tier=raw.get("sub_tier"),
        program_code=raw.get("program_code"),
        lavender_group=raw.get("lavender_group"),
        risk_appetite=raw.get("risk_appetite"),
        cic_score=raw.get("cic_score"),
        economic_segment=raw.get("economic_segment"),
        marketing_segment=raw.get("marketing_segment"),
        tactical_segment=raw.get("tactical_segment"),
        customer_journey=raw.get("customer_journey"),
        customer_persona=raw.get("customer_persona"),
        investment_needs_persona=raw.get("investment_needs_persona"),
        professional_investor_flag=raw.get("professional_investor_flag"),
        customer_since=raw.get("customer_since"),
        membership_effective_date=raw.get("membership_effective_date"),
        membership_review_date=raw.get("membership_review_date"),
        membership_expiration_date=raw.get("membership_expiration_date"),
        managing_branch=raw.get("managing_branch"),
        family_member_count=raw.get("family_member_count"),
    )


def _map_finance_profile(raw: dict) -> FinanceProfileLatest:
    """Map raw finance profile dict to GraphQL type."""
    return FinanceProfileLatest(
        customer_id=raw.get("customer_id", ""),
        date_key=raw.get("date_key", ""),
        aum_eop_amount=raw.get("aum_eop_amount"),
        aum_avg_last_3m_amount=raw.get("aum_casa_td_cd_bond_fund_avg_last_3m_amount"),
        casa_eop_amount=raw.get("casa_eop_amount"),
        td_eop_amount=raw.get("td_eop_amount"),
        cd_max_eop_amount=raw.get("cd_max_eop_amount"),
        bond_eop_amount=raw.get("bond_eop_amount"),
        fund_eop_amount=raw.get("fund_eop_amount"),
        ape_ytd_amount=raw.get("ape_ytd_amount"),
        total_asset_value_amount=raw.get("total_asset_value_amount"),
        total_liabilities_value_amount=raw.get("total_liabilities_value_amount"),
        net_assets_value_amount=raw.get("net_assets_value_amount"),
        total_casa_at_tcb_eop_amount=raw.get("total_casa_at_tcb_eop_amount"),
        total_liquid_asset_at_tcb_amount=raw.get("total_liquid_asset_at_tcb_amount"),
        total_shared_capital_asset_value_amount=raw.get("total_shared_capital_asset_value_amount"),
        total_fixed_asset_value_amount=raw.get("total_fixed_asset_value_amount"),
        total_mortgage_and_auto_eop_amount=raw.get("total_mortgage_and_auto_eop_amount"),
        total_unsecured_loan_at_tcb_amount=raw.get("total_unsecured_loan_at_tcb_amount"),
        total_secured_loan_amount=raw.get("total_secured_loan_amount"),
        secured_lending_eop_amount=raw.get("secured_lending_eop_amount"),
        unsecured_lending_eop_amount=raw.get("unsecured_lending_eop_amount"),
        lending_credit_card_eop_amount=raw.get("lending_credit_card_eop_amount"),
        mycash_eop_amount=raw.get("mycash_eop_amount"),
        product_used_count=raw.get("product_used_count"),
        total_monthly_salary_income_amount=raw.get("total_monthly_salary_income_amount"),
        total_monthly_real_estate_rental_income_amount=raw.get("total_monthly_real_estate_rental_income_amount"),
        total_monthly_car_rental_income_amount=raw.get("total_monthly_car_rental_income_amount"),
        total_monthly_entrepreneurial_income_amount=raw.get("total_monthly_entrepreneurial_income_amount"),
        total_monthly_other_income_amount=raw.get("total_monthly_other_income_amount"),
        total_monthly_income_amount=raw.get("total_monthly_income_amount"),
        total_monthly_fixed_expense_amount=raw.get("total_monthly_fixed_expense_amount"),
        total_monthly_medical_expense_amount=raw.get("total_monthly_medical_expense_amount"),
        total_monthly_education_expense_amount=raw.get("total_monthly_education_expense_amount"),
        total_monthly_holiday_expense_amount=raw.get("total_monthly_holiday_expense_amount"),
        total_monthly_other_expense_amount=raw.get("total_monthly_other_expense_amount"),
        total_monthly_expense_amount=raw.get("total_monthly_expense_amount"),
        net_monthly_income_amount=raw.get("net_monthly_income_amount"),
        nbo_1=raw.get("nbo_1"),
        nbo_1_explanation=raw.get("nbo_1_explanation"),
        nbo_2=raw.get("nbo_2"),
        nbo_2_explanation=raw.get("nbo_2_explanation"),
        nbo_3=raw.get("nbo_3"),
        nbo_3_explanation=raw.get("nbo_3_explanation"),
    )


METRIC_FIELD_MAP = {
    "AUM_EOP": "aum_eop_amount",
    "AUM_AVG_LAST_3M": "aum_casa_td_cd_bond_fund_avg_last_3m_amount",
    "CASA_EOP": "casa_eop_amount",
    "TD_EOP": "td_eop_amount",
    "TOTAL_ASSETS": "total_asset_value_amount",
    "TOTAL_LIABILITIES": "total_liabilities_value_amount",
    "NET_MONTHLY_INCOME": "net_monthly_income_amount",
}


def _compute_trend(points: list[FinancePoint]) -> str:
    """Compute simple trend direction."""
    if len(points) < 2:
        return "UNKNOWN"
    first = points[0].value
    last = points[-1].value
    if first is None or last is None:
        return "UNKNOWN"
    diff = last - first
    threshold = abs(first) * 0.02 if first != 0 else 0
    if diff > threshold:
        return "UP"
    elif diff < -threshold:
        return "DOWN"
    else:
        return "FLAT"


# --- Resolvers ---

@strawberry.type
class Query:

    @strawberry.field
    def resolve_customer(
        self,
        customer_id: Optional[str] = None,
        customer_name: Optional[str] = None,
    ) -> CustomerResolveResult:
        """Resolve a customer by ID or name."""
        candidates = []

        if customer_id:
            raw = data_loader.get_customer_by_id(customer_id)
            if raw:
                candidates.append(CustomerRef(
                    customer_id=raw["customer_id"],
                    customer_name=raw.get("customer_name", ""),
                    rm_id=raw.get("rm_id"),
                    tier=raw.get("tier"),
                    confidence=1.0,
                ))

        if customer_name and not candidates:
            matches = data_loader.get_customer_by_name(customer_name)
            for raw in matches:
                # Simple confidence scoring
                exact = raw.get("customer_name", "").lower() == customer_name.lower()
                candidates.append(CustomerRef(
                    customer_id=raw["customer_id"],
                    customer_name=raw.get("customer_name", ""),
                    rm_id=raw.get("rm_id"),
                    tier=raw.get("tier"),
                    confidence=1.0 if exact else 0.8,
                ))

        if not candidates:
            return CustomerResolveResult(status="NOT_FOUND", candidates=[])
        elif len(candidates) == 1:
            return CustomerResolveResult(status="RESOLVED", candidates=candidates)
        else:
            return CustomerResolveResult(status="AMBIGUOUS", candidates=candidates)

    @strawberry.field
    def customer_info(self, customer_id: str) -> Optional[CustomerInfo]:
        """Return latest customer demographic profile."""
        raw = data_loader.get_customer_by_id(customer_id)
        if not raw:
            return None
        return _map_customer_info(raw)

    @strawberry.field
    def finance_profile_latest(self, customer_id: str) -> Optional[FinanceProfileLatest]:
        """Return latest finance snapshot."""
        raw = data_loader.get_finance_profile_latest(customer_id)
        if not raw:
            return None
        return _map_finance_profile(raw)

    @strawberry.field
    def finance_metric_series(
        self,
        customer_id: str,
        metric: str,
        months: int = 3,
    ) -> FinanceMetricSeriesResult:
        """Return a time series for a specific finance metric."""
        months = max(1, min(months, 24))
        profiles = data_loader.get_finance_profiles_series(customer_id, months)

        field = METRIC_FIELD_MAP.get(metric, "aum_eop_amount")
        points = []
        for p in profiles:
            dk = p.get("date_key", "")
            val = p.get(field)
            # Extract month label (MM/YYYY)
            parts = dk.split("/")
            month_label = f"{parts[1]}/{parts[2]}" if len(parts) == 3 else dk
            points.append(FinancePoint(month=month_label, date_key=dk, value=val))

        return FinanceMetricSeriesResult(
            customer_id=customer_id,
            metric=metric,
            months=months,
            points=points,
            trend_direction=_compute_trend(points),
        )

    @strawberry.field
    def customer_overview(self, customer_id: str) -> Optional[CustomerOverview]:
        """Return combined customer overview."""
        raw_info = data_loader.get_customer_by_id(customer_id)
        if not raw_info:
            return None

        raw_finance = data_loader.get_finance_profile_latest(customer_id)

        return CustomerOverview(
            customer=CustomerRef(
                customer_id=raw_info["customer_id"],
                customer_name=raw_info.get("customer_name", ""),
                rm_id=raw_info.get("rm_id"),
                tier=raw_info.get("tier"),
            ),
            customer_info=_map_customer_info(raw_info),
            finance_latest=_map_finance_profile(raw_finance) if raw_finance else None,
        )


schema = strawberry.Schema(query=Query)

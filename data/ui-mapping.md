---
title: "Overview Dashboard UI Mapping"
description: "Canonical Markdown export of the overview dashboard field mapping workbook for AI Frontline POC1."
created: 2026-03-12
updated: 2026-03-12
tags: [ui-mapping, dashboard, data-lake, overview, semantic-search]
status: stable
---

# Overview Dashboard UI Mapping

Nguồn canonical được chuyển từ workbook `overview-dashboard-field-map.xlsx` để mô tả field nào từ Data Lake đang được dùng để hiển thị trên dashboard overview của POC.

## Overview

| Metric | Value |
|---|---|
| Source workbook | `overview-dashboard-field-map.xlsx` |
| Sheet count | 1 |
| Mapping row count | 36 |
| Column set | `AI agent`, `Description`, `Data Lake` |

## Mapping Rules

| Rule | Value |
|---|---|
| Snapshot fields | Thường dùng điều kiện `date_key = latest` |
| Time-series field | `Average AUM (24 months)` dùng `group by month` và lấy `latest 24 months` |
| NBO fields | Map trực tiếp từ `nbo_1`, `nbo_2`, `nbo_3` |

## Field Mapping

| Dashboard Field | Description | Data Lake Mapping |
|---|---|---|
| `Customer ID` | Mã khách hàng | `customer_id` |
| `RM ID` | Mã RM | `rm_id` |
| `Customer Name` |  | `customer_name` |
| `Age` |  | `age` |
| `Tier` |  | `tier` |
| `VIP Program` |  | `program_code` |
| `Lavender Group` |  | `lavender_group` |
| `Risk level` |  | `risk_appetite` |
| `CIC Score` |  | `cic_score` |
| `Membership Expiration date` |  | `membership_expiration_date` |
| `Product Holding (Deposit)` | Số dư sản phẩm TD | `td_eop_amount + date_key = latest` |
| `Product Holding (CASA)` | Số dư sản phẩm CASA | `casa_eop_amount + date_key = latest` |
| `Product Holding (Certificates of deposit)` | Số dư sản phẩm CD | `cd_max_eop_amount + date_key = latest` |
| `Product Holding (Bond)` | Số dư Bond | `bond_eop_amount + date_key = latest` |
| `Product Holding (Banca)` | Phí hợp đồng Banca (total APE) | `ape_ytd_amount + date_key = latest` |
| `Assets (CASA at TCB)` |  | `total_casa_at_tcb_eop_amount + date_key = latest` |
| `Assets (Liquid assets at TCB)` |  | `total_liquid_asset_at_tcb_amount + date_key = latest` |
| `Assets (Shared capital asset)` |  | `total_shared_capital_asset_value_amount + date_key = latest` |
| `Assets (Fixed asset value)` |  | `total_fixed_asset_value_amount + date_key = latest` |
| `Assets (Mortgage and auto)` |  | `total_mortgage_and_auto_eop_amount + date_key = latest` |
| `Total Assets Value` |  | `total_asset_value_amount + date_key = latest` |
| `Liabilities (Unsecured loan amount)` |  | `total_unsecured_loan_at_tcb_amount + date_key = latest` |
| `Liabilities (Secured loan amount)` |  | `total_secured_loan_amount + date_key = latest` |
| `Total Liabilities Value` |  | `total_liabilities_value_amount + date_key = latest` |
| `Income (Monthly salary income)` |  | `total_monthly_salary_income_amount + date_key = latest` |
| `Income (Monthly Real estate rental income)` |  | `total_monthly_real_estate_rental_income_amount + date_key = latest` |
| `Income (Monthly Car rental income)` |  | `total_monthly_car_rental_income_amount + date_key = latest` |
| `Income (Monthly Other)` |  | `total_monthly_other_income_amount + date_key = latest` |
| `Expense (Monthly Fixed expense)` |  | `total_monthly_fixed_expense_amount + date_key = latest` |
| `Expense (Monthly Medical expense)` |  | `total_monthly_medical_expense_amount + date_key = latest` |
| `Expense (Monthly Education expense)` |  | `total_monthly_education_expense_amount + date_key = latest` |
| `Expense (Monthly Holiday expense)` |  | `total_monthly_holiday_expense_amount + date_key = latest` |
| `Average AUM (24 months)` |  | `aum_3m_amount + date_key (group by month) = latest 24 months` |
| `NBO 1` |  | `nbo_1` |
| `NBO 2` |  | `nbo_2` |
| `NBO 3` |  | `nbo_3` |

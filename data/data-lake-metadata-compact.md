---
title: "Data Lake Metadata Compact"
description: "Compact metadata summary for AI Frontline POC1 field routing when full pgvector metadata search is disabled."
created: 2026-03-12
updated: 2026-03-12
tags: [data-lake, metadata, compact, semantic-search, field-routing]
status: stable
---

# Data Lake Metadata Compact

Bản rút gọn này dùng cho bước tìm field khi `USE_METADATA_PGVECTOR_SEARCH=false`.
Mục tiêu là giữ ngữ nghĩa đủ dùng cho POC hiện tại nhưng ngắn hơn nhiều so với `data-lake-metadata.md`.

## Scope

- Tập trung vào 2 bảng dữ liệu thật đang nuôi POC:
  - `ai_frontline_customer_info`
  - `ai_frontline_finance_profile`
- Ưu tiên các field đang dùng ở overview dashboard, field drill-down thường gặp và alias business phổ biến.
- Quy ước thời gian:
  - field snapshot trong `finance_profile` thường lấy record mới nhất theo `date_key = latest`
  - field timeseries AUM lấy theo tháng từ `date_key`

## Canonical Keys

| Concept | Canonical Field | Notes |
|---|---|---|
| Customer identifier | `customer_id` | Sample data hiện tại dùng `customer_id`; metadata gốc có nơi dùng `customer_code` |
| RM identifier | `rm_id` | Mã RM phụ trách khách hàng |
| Time key | `date_key` | Dùng để lấy latest record hoặc group by month |

## Demographics

| Field | Meaning | Common Aliases |
|---|---|---|
| `customer_name` | Tên khách hàng | customer name, họ tên KH, tên KH |
| `age` | Tuổi khách hàng | age, tuổi |
| `tier` | Hạng hội viên hiện tại | tier, hạng hội viên, hạng KH |
| `program_code` | Chương trình hội viên/VIP | vip program, membership program, chương trình ưu tiên |
| `lavender_group` | Nhóm khách hàng Lavender | lavender group, nhóm Lavender |
| `risk_appetite` | Khẩu vị rủi ro | risk level, risk appetite, mức rủi ro |
| `cic_score` | Điểm CIC | cic score, điểm tín dụng |
| `membership_expiration_date` | Ngày hết hạn hạng hội viên | membership expiry, expiry date, ngày hết hạn hội viên |
| `economic_segment` | Phân khúc kinh tế | segment, phân khúc KH |

## Product Holdings

Các field này lấy từ `ai_frontline_finance_profile` với `date_key = latest`.

| Field | Meaning | Common Aliases |
|---|---|---|
| `td_eop_amount` | Số dư tiền gửi có kỳ hạn | deposit, TD, term deposit |
| `casa_eop_amount` | Số dư CASA | CASA, current account, tiền gửi không kỳ hạn |
| `cd_max_eop_amount` | Số dư chứng chỉ tiền gửi | CD, certificates of deposit |
| `bond_eop_amount` | Số dư trái phiếu | bond, trái phiếu |
| `fund_eop_amount` | Số dư quỹ | fund, chứng chỉ quỹ |
| `ape_ytd_amount` | Giá trị APE bảo hiểm | banca, total APE, phí bảo hiểm |
| `mycash_eop_amount` | Số dư MyCash | mycash |
| `lending_credit_card_eop_amount` | Dư nợ thẻ tín dụng | credit card balance, dư nợ thẻ |
| `secured_lending_eop_amount` | Tổng dư nợ vay có tài sản đảm bảo | secured lending, secured loan |

## Assets

Các field này lấy từ `ai_frontline_finance_profile` với `date_key = latest`.

| Field | Meaning | Common Aliases |
|---|---|---|
| `total_casa_at_tcb_eop_amount` | Tổng CASA tại Techcombank | casa at tcb |
| `total_liquid_asset_at_tcb_amount` | Tổng tài sản lỏng tại Techcombank | liquid assets at tcb |
| `total_shared_capital_asset_value_amount` | Giá trị shared capital asset | shared capital asset |
| `total_fixed_asset_value_amount` | Tổng tài sản cố định | fixed asset value |
| `total_mortgage_and_auto_eop_amount` | Tổng dư nợ nhà và ô tô | mortgage and auto |
| `total_asset_value_amount` | Tổng tài sản | total assets value, tổng tài sản, TAV |
| `net_assets_value_amount` | Tài sản ròng | net assets, tài sản ròng |

## Liabilities

Các field này lấy từ `ai_frontline_finance_profile` với `date_key = latest`.

| Field | Meaning | Common Aliases |
|---|---|---|
| `total_unsecured_loan_at_tcb_amount` | Vay không tài sản đảm bảo tại TCB | unsecured loan |
| `total_secured_loan_amount` | Tổng vay có tài sản đảm bảo | secured loan |
| `total_liabilities_value_amount` | Tổng dư nợ | total liabilities, liabilities |

## AUM

| Field | Meaning | Common Aliases | Notes |
|---|---|---|---|
| `aum_eop_amount` | AUM hiện tại/cuối kỳ | current AUM, AEM, total AUM | Snapshot tại `date_key = latest` |
| `aum_casa_td_cd_bond_fund_avg_last_3m_amount` | AUM bình quân 3 tháng | average AUM, AUM 3 tháng, AEM 3 tháng | Dùng cho overview chart của POC |

## Income

Các field này lấy từ `ai_frontline_finance_profile` với `date_key = latest`.

| Field | Meaning | Common Aliases |
|---|---|---|
| `total_monthly_salary_income_amount` | Thu nhập lương tháng | monthly salary, lương tháng |
| `total_monthly_real_estate_rental_income_amount` | Thu nhập cho thuê nhà | rental income, real estate rental |
| `total_monthly_car_rental_income_amount` | Thu nhập cho thuê ô tô | car rental income |
| `total_monthly_entrepreneurial_income_amount` | Thu nhập kinh doanh | business income, entrepreneurial income |
| `total_monthly_other_income_amount` | Thu nhập khác | other income |
| `total_monthly_income_amount` | Tổng thu nhập tháng | total monthly income, tổng thu nhập |

## Expenses

Các field này lấy từ `ai_frontline_finance_profile` với `date_key = latest`.

| Field | Meaning | Common Aliases |
|---|---|---|
| `total_monthly_fixed_expense_amount` | Chi phí cố định tháng | fixed expense |
| `total_monthly_medical_expense_amount` | Chi phí y tế tháng | medical expense |
| `total_monthly_education_expense_amount` | Chi phí giáo dục tháng | education expense |
| `total_monthly_holiday_expense_amount` | Chi phí du lịch tháng | holiday expense |
| `total_monthly_other_expense_amount` | Chi phí khác tháng | other expense |
| `total_monthly_expense_amount` | Tổng chi phí tháng | total monthly expense, tổng chi phí |
| `net_monthly_income_amount` | Thu nhập ròng tháng | net monthly income, thu nhập ròng |

## Next Best Offers

| Field | Meaning | Common Aliases |
|---|---|---|
| `nbo_1` | Gợi ý sản phẩm số 1 | nbo 1, offer 1 |
| `nbo_2` | Gợi ý sản phẩm số 2 | nbo 2, offer 2 |
| `nbo_3` | Gợi ý sản phẩm số 3 | nbo 3, offer 3 |

## Overview UI Mapping Summary

| Dashboard Concept | Data Lake Field |
|---|---|
| Customer ID | `customer_id` |
| RM ID | `rm_id` |
| Customer Name | `customer_name` |
| Age | `age` |
| Tier | `tier` |
| VIP Program | `program_code` |
| Lavender Group | `lavender_group` |
| Risk level | `risk_appetite` |
| CIC Score | `cic_score` |
| Membership Expiration date | `membership_expiration_date` |
| Deposit holding | `td_eop_amount` |
| CASA holding | `casa_eop_amount` |
| CD holding | `cd_max_eop_amount` |
| Bond holding | `bond_eop_amount` |
| Banca holding | `ape_ytd_amount` |
| Total Assets Value | `total_asset_value_amount` |
| Total Liabilities Value | `total_liabilities_value_amount` |
| Monthly salary income | `total_monthly_salary_income_amount` |
| Monthly other income | `total_monthly_other_income_amount` |
| Monthly fixed expense | `total_monthly_fixed_expense_amount` |
| Average AUM | `aum_casa_td_cd_bond_fund_avg_last_3m_amount` |
| NBO 1/2/3 | `nbo_1`, `nbo_2`, `nbo_3` |

## Resolution Hints

- Nếu user hỏi `tổng quan`, `overview`, `hồ sơ đầy đủ`:
  - route về `customer-overview`
- Nếu user hỏi một block như `AUM`, `thu nhập`, `tài sản`, `sản phẩm`, `NBO`:
  - route về block/widget tương ứng
- Nếu user hỏi một field cụ thể như `VIP Program`, `tier`, `CIC score`, `tổng tài sản`, `AUM hiện tại`:
  - map về field canonical gần nhất trong bảng trên
- Nếu user hỏi giá trị snapshot:
  - dùng `date_key = latest`
- Nếu user hỏi chuỗi thời gian AUM:
  - dùng `aum_casa_td_cd_bond_fund_avg_last_3m_amount` theo tháng từ `date_key`

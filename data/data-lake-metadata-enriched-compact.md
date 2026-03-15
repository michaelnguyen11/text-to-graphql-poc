---
title: "Data Lake Metadata Enriched Compact"
description: "Compact enriched metadata summary for AI Frontline POC1 field routing when pgvector metadata search is disabled."
created: 2026-03-13
updated: 2026-03-13
tags: [data-lake, metadata, compact, enriched, semantic-search, field-routing]
status: draft
---

# Data Lake Metadata Enriched Compact

Bản rút gọn này lấy từ `data-lake-metadata-enriched.md` để dùng cho bước tìm field khi `USE_METADATA_PGVECTOR_SEARCH=false`.
Mục tiêu là giữ alias banking đủ mạnh cho LLM nhưng ngắn hơn nhiều so với catalog enriched đầy đủ.

## Scope

- Tập trung vào 2 bảng đang nuôi POC:
  - `ai_frontline_customer_info`
  - `ai_frontline_finance_profile`
- Ưu tiên các field overview dashboard, field drill-down thường gặp và business aliases mà RM có thể hỏi bằng tiếng Việt hoặc tiếng Anh.
- Quy ước truy vấn:
  - field snapshot lấy record mới nhất theo `date_key = latest`
  - AUM timeseries dùng `date_key` để sắp xếp theo thời gian

## Canonical Keys

| Concept | Canonical Field | Aliases |
|---|---|---|
| Customer identifier | `customer_id` | customer id, mã KH, CIF, customer code |
| RM identifier | `rm_id` | RM id, mã RM, banker id, chuyên viên phụ trách |
| Time key | `date_key` | ngày dữ liệu, snapshot date, ngày chụp dữ liệu |

## Demographics And Segmentation

| Field | Meaning | Common Aliases |
|---|---|---|
| `customer_name` | Tên khách hàng | tên KH, họ tên, customer name, client name |
| `age` | Tuổi khách hàng | tuổi, age, years old |
| `age_group` | Nhóm tuổi | nhóm tuổi, độ tuổi, age band |
| `occupation` | Nghề nghiệp | nghề nghiệp, công việc, occupation, profession |
| `tier` | Hạng hội viên | tier, hạng KH, hạng hội viên, VIP tier |
| `sub_tier` | Hạng hội viên chi tiết | sub-tier, hạng phụ, tier detail |
| `program_code` | Chương trình hội viên/VIP | VIP program, chương trình ưu tiên, loyalty program |
| `lavender_group` | Nhóm khách hàng Lavender | lavender group, nhóm Lavender |
| `risk_appetite` | Khẩu vị rủi ro | risk appetite, risk level, mức rủi ro |
| `cic_score` | Điểm CIC | CIC, credit score, điểm tín dụng |
| `economic_segment` | Phân khúc kinh tế | segment, economic segment, phân khúc KH |
| `customer_since` | Ngày trở thành khách hàng TCB | customer since, onboarding date, ngày mở tài khoản |
| `membership_effective_date` | Ngày hiệu lực hạng hội viên | ngày lên hạng, membership effective date |
| `membership_review_date` | Ngày review hạng hội viên | ngày review tier, membership review date |
| `membership_expiration_date` | Ngày hết hạn hạng hội viên | expiry date, membership expiry, ngày hết hạn hội viên |

## Product Holdings Snapshot

Các field bên dưới lấy từ `ai_frontline_finance_profile` với `date_key = latest`.

| Field | Meaning | Common Aliases |
|---|---|---|
| `casa_eop_amount` | Số dư CASA | CASA, tiền gửi không kỳ hạn, current account |
| `td_eop_amount` | Số dư tiền gửi có kỳ hạn | TD, term deposit, deposit holding |
| `cd_max_eop_amount` | Số dư chứng chỉ tiền gửi | CD, certificate of deposit |
| `bond_eop_amount` | Số dư trái phiếu | bond, trái phiếu |
| `fund_eop_amount` | Số dư quỹ | fund, chứng chỉ quỹ, mutual fund holding |
| `ape_ytd_amount` | Giá trị APE bảo hiểm | banca, APE, phí bảo hiểm năm nay |
| `mycash_eop_amount` | Số dư MyCash | mycash |
| `lending_credit_card_eop_amount` | Dư nợ thẻ tín dụng | credit card balance, dư nợ thẻ |
| `secured_lending_eop_amount` | Dư nợ vay có tài sản đảm bảo | secured lending, secured loan |
| `unsecured_lending_eop_amount` | Dư nợ vay tín chấp | unsecured lending, unsecured loan |
| `product_used_count` | Số lượng sản phẩm đang dùng | product count, số sản phẩm |

## Assets And Liabilities

Các field bên dưới lấy từ `ai_frontline_finance_profile` với `date_key = latest`.

| Field | Meaning | Common Aliases |
|---|---|---|
| `total_casa_at_tcb_eop_amount` | Tổng CASA tại TCB | CASA at TCB, tổng CASA tại TCB |
| `total_liquid_asset_at_tcb_amount` | Tổng tài sản lỏng tại TCB | liquid assets, tài sản lỏng |
| `total_shared_capital_asset_value_amount` | Giá trị shared capital asset | shared capital asset |
| `total_fixed_asset_value_amount` | Tổng tài sản cố định | fixed assets, tài sản cố định |
| `total_asset_value_amount` | Tổng tài sản | total assets, total asset value, TAV, tổng tài sản |
| `net_assets_value_amount` | Tài sản ròng | net assets, NAV, tài sản ròng |
| `total_mortgage_and_auto_eop_amount` | Tổng dư nợ nhà và ô tô | mortgage and auto, vay nhà xe |
| `total_unsecured_loan_at_tcb_amount` | Tổng vay tín chấp tại TCB | unsecured loan at TCB, vay tín chấp |
| `total_secured_loan_amount` | Tổng vay có tài sản đảm bảo | secured loan, vay thế chấp |
| `total_liabilities_value_amount` | Tổng dư nợ | total liabilities, liabilities, tổng nghĩa vụ nợ |

## AUM

| Field | Meaning | Common Aliases | Notes |
|---|---|---|---|
| `aum_eop_amount` | AUM hiện tại/cuối kỳ | AUM hiện tại, current AUM, total AUM, AEM | Snapshot tại `date_key = latest` |
| `aum_casa_td_cd_bond_fund_avg_last_3m_amount` | AUM bình quân 3 tháng | average AUM, AUM 3 tháng, AEM 3 tháng, average balance | Dùng cho overview và trend 3 tháng |
| `casa_net_change_aum_t30_amount` | Biến động CASA 30 ngày | CASA net change 30d, biến động CASA tháng |
| `td_net_change_aum_t30_amount` | Biến động TD 30 ngày | TD net change 30d, biến động tiền gửi kỳ hạn |
| `fund_net_change_aum_t30_amount` | Biến động Fund 30 ngày | fund net change 30d, biến động quỹ |

## Income And Expenses

Các field bên dưới lấy từ `ai_frontline_finance_profile` với `date_key = latest`.

| Field | Meaning | Common Aliases |
|---|---|---|
| `total_monthly_salary_income_amount` | Thu nhập lương tháng | salary, monthly salary, lương tháng |
| `total_monthly_real_estate_rental_income_amount` | Thu nhập cho thuê bất động sản | rental income, thu nhập cho thuê nhà |
| `total_monthly_car_rental_income_amount` | Thu nhập cho thuê ô tô | car rental income |
| `total_monthly_entrepreneurial_income_amount` | Thu nhập kinh doanh | business income, entrepreneurial income |
| `total_monthly_other_income_amount` | Thu nhập khác | other income |
| `total_monthly_income_amount` | Tổng thu nhập tháng | total monthly income, tổng thu nhập, tổng dòng tiền vào, dòng tiền vào, monthly inflow |
| `total_monthly_fixed_expense_amount` | Chi phí cố định tháng | fixed expense, chi phí cố định |
| `total_monthly_medical_expense_amount` | Chi phí y tế tháng | medical expense |
| `total_monthly_education_expense_amount` | Chi phí giáo dục tháng | education expense |
| `total_monthly_holiday_expense_amount` | Chi phí du lịch tháng | holiday expense, travel expense |
| `total_monthly_other_expense_amount` | Chi phí khác tháng | other expense |
| `total_monthly_expense_amount` | Tổng chi phí tháng | total monthly expense, tổng chi phí, tổng dòng tiền ra, dòng tiền ra, monthly outflow |
| `net_monthly_income_amount` | Thu nhập ròng tháng | net monthly income, thu nhập ròng, dòng tiền ròng, dòng tiền, cash flow, monthly cash flow |

## Next Best Offers

| Field | Meaning | Common Aliases |
|---|---|---|
| `nbo_1` | Gợi ý sản phẩm số 1 | nbo 1, offer 1, next best offer 1 |
| `nbo_2` | Gợi ý sản phẩm số 2 | nbo 2, offer 2, next best offer 2 |
| `nbo_3` | Gợi ý sản phẩm số 3 | nbo 3, offer 3, next best offer 3 |

## Overview UI Mapping Summary

| Dashboard Concept | Canonical Field |
|---|---|
| Customer ID | `customer_id` |
| RM ID | `rm_id` |
| Customer Name | `customer_name` |
| Age | `age` |
| Tier | `tier` |
| VIP Program | `program_code` |
| Lavender Group | `lavender_group` |
| Risk Level | `risk_appetite` |
| CIC Score | `cic_score` |
| Membership Expiration Date | `membership_expiration_date` |
| Deposit Holding | `td_eop_amount` |
| CASA Holding | `casa_eop_amount` |
| CD Holding | `cd_max_eop_amount` |
| Bond Holding | `bond_eop_amount` |
| Fund Holding | `fund_eop_amount` |
| Banca Holding | `ape_ytd_amount` |
| Total Assets Value | `total_asset_value_amount` |
| Total Liabilities Value | `total_liabilities_value_amount` |
| Monthly Salary Income | `total_monthly_salary_income_amount` |
| Monthly Other Income | `total_monthly_other_income_amount` |
| Monthly Fixed Expense | `total_monthly_fixed_expense_amount` |
| Average AUM | `aum_casa_td_cd_bond_fund_avg_last_3m_amount` |
| NBO 1/2/3 | `nbo_1`, `nbo_2`, `nbo_3` |

## Resolution Hints

- Nếu RM hỏi `tổng quan`, `overview`, `hồ sơ đầy đủ`:
  - route về `customer-overview`
- Nếu RM hỏi theo block như `AUM`, `thu nhập`, `chi phí`, `dòng tiền`, `cash flow`, `thu chi`, `tài sản`, `sản phẩm`, `NBO`:
  - route về widget tương ứng
- Nếu RM hỏi `liệt kê các dòng tiền`, `dòng tiền vào/ra`, `cash flow của KH`:
  - ưu tiên route về `income-expenses`
  - hiển thị danh sách các khoản thu, các khoản chi và `net_monthly_income_amount`
- Nếu RM hỏi field cụ thể như `VIP Program`, `tier`, `CIC`, `tổng tài sản`, `CASA`, `AUM hiện tại`:
  - map về canonical field gần nhất trong bảng trên
- Nếu hỏi snapshot hay giá trị hiện tại:
  - dùng `date_key = latest`
- Nếu hỏi xu hướng AUM:
  - dùng `aum_casa_td_cd_bond_fund_avg_last_3m_amount`

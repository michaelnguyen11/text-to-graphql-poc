---
title: "Data Lake Metadata"
description: "Canonical Markdown export of the real Data Lake metadata workbook for AI Frontline POC1 semantic search and reference."
created: 2026-03-12
updated: 2026-03-12
tags: [data-lake, metadata, schema, vectordb, semantic-search]
status: stable
---

# Data Lake Metadata

Nguồn canonical được chuyển từ workbook `data-lake-metadata.xlsx` để dễ đọc, review và đưa vào vector DB cho semantic search.

File này hiện giữ 2 lớp thông tin:
- `Field Catalog`: metadata gốc được export gần như nguyên trạng từ workbook.
- `Field Alias Enrichment Preview`: alias business để preview cách enrich metadata trước khi ingest vào vector DB.

## Overview

| Metric | Value |
|---|---|
| Source workbook | `data-lake-metadata.xlsx` |
| Sheet count | 1 |
| Metadata row count | 194 |
| Distinct source tables | 5 |
| Alias enrichment preview rows | 16 |

## Source Tables

| Source Table | Field Count |
|---|---:|
| `?` (source workbook chưa xác định rõ table) | 4 |
| `ai_frontline_customer_event` | 1 |
| `ai_frontline_customer_info` | 55 |
| `ai_frontline_customer_statistic` | 36 |
| `ai_frontline_finance_profile` | 99 |

## Field Alias Enrichment Preview

Preview này dùng để chuẩn hóa cách lưu synonym ngay trong `data-lake-metadata.md`, thay vì tách thêm file alias riêng. Mục tiêu là để ingestion sau này chỉ cần 2 nguồn canonical:
- `data-lake-metadata.md`
- `ui-mapping.md`

| Field Name | Business Aliases | Vietnamese Aliases | English Aliases | Abbreviations | Sample Queries |
|---|---|---|---|---|---|
| `customer_code` | mã khách hàng lõi, mã CIF | mã khách hàng, mã KH, CIF khách hàng | customer code, customer identifier, CIF | `CIF` | `Mã khách hàng của KH là gì?`; `Cho tôi CIF của khách hàng` |
| `rm_id` | mã RM phụ trách, mã chuyên viên quan hệ | mã RM, RM phụ trách, chuyên viên chăm sóc | relationship manager id, RM id | `RM` | `RM nào đang phụ trách KH này?`; `Cho tôi mã RM` |
| `customer_name` | tên khách hàng hiển thị | tên khách hàng, họ tên KH | customer name, full name |  | `Tên khách hàng là gì?`; `Cho tôi họ tên của KH` |
| `tier` | hạng hội viên hiện tại | hạng hội viên, tier khách hàng, hạng KH | membership tier, customer tier |  | `KH đang ở hạng nào?`; `Tier hiện tại của KH là gì?` |
| `program_code` | chương trình VIP áp dụng | chương trình hội viên, chương trình ưu tiên, VIP program | program code, VIP program, membership program | `VIP` | `KH thuộc chương trình VIP nào?`; `Program code của KH là gì?` |
| `lavender_group` | nhóm Lavender | nhóm Lavender, lavender group | lavender group |  | `KH thuộc nhóm Lavender nào?` |
| `risk_appetite` | mức chấp nhận rủi ro | khẩu vị rủi ro, mức rủi ro, risk level | risk appetite, risk level |  | `Khẩu vị rủi ro của KH là gì?`; `Risk level của KH thế nào?` |
| `membership_expiration_date` | ngày hết hạn hạng hội viên | ngày hết hạn hội viên, ngày hết hạn tier | membership expiration date, tier expiry date |  | `Khi nào hạng hội viên của KH hết hạn?` |
| `aum_casa_td_cd_bond_fund_avg_last_3m_amount` | AUM bình quân 3 tháng | AUM bình quân 3 tháng, bình quân tài sản 90 ngày, AUM trung bình 3 tháng | average AUM last 3 months, 3-month average AUM | `AUM`, `AEM` | `AUM bình quân 3 tháng gần đây là bao nhiêu?`; `Cho tôi average AUM 3 tháng` |
| `aum_eop_amount` | AUM hiện tại, tổng tài sản cuối kỳ | AUM hiện tại, tổng tài sản cuối kỳ | current AUM, end-of-period AUM, assets under management | `AUM`, `AEM`, `EOP` | `AUM hiện tại của KH là bao nhiêu?`; `Tổng tài sản cuối kỳ hiện tại là bao nhiêu?` |
| `td_eop_amount` | số dư tiền gửi có kỳ hạn cuối kỳ | số dư TD, tiền gửi kỳ hạn, tiền gửi có kỳ hạn | term deposit balance, TD balance | `TD`, `EOP` | `Số dư TD hiện tại là bao nhiêu?`; `KH đang có bao nhiêu tiền gửi kỳ hạn?` |
| `casa_eop_amount` | số dư CASA cuối kỳ | số dư CASA, tiền gửi không kỳ hạn, tài khoản thanh toán | CASA balance, current account balance | `CASA`, `EOP` | `Số dư CASA hiện tại là bao nhiêu?`; `KH có bao nhiêu tiền gửi không kỳ hạn?` |
| `cd_max_eop_amount` | số dư chứng chỉ tiền gửi cuối kỳ | số dư CD, số dư chứng chỉ tiền gửi | certificate of deposit balance, CD balance | `CD`, `EOP` | `Số dư chứng chỉ tiền gửi của KH là bao nhiêu?` |
| `total_asset_value_amount` | tổng tài sản của khách hàng | tổng tài sản, tổng giá trị tài sản | total assets value, total asset value | `TAV` | `Tổng tài sản của KH là bao nhiêu?`; `Total assets value hiện tại là gì?` |
| `total_liabilities_value_amount` | tổng dư nợ, tổng nghĩa vụ nợ | tổng nợ, tổng dư nợ, liabilities | total liabilities value, total liabilities |  | `Tổng dư nợ hiện tại của KH là bao nhiêu?`; `Liabilities hiện tại là gì?` |
| `total_monthly_income_amount` | tổng thu nhập hàng tháng | tổng thu nhập tháng, thu nhập hàng tháng | total monthly income, monthly income |  | `Thu nhập hàng tháng của KH là bao nhiêu?`; `Tổng income mỗi tháng là gì?` |
| `total_monthly_expense_amount` | tổng chi phí hàng tháng | tổng chi tiêu tháng, tổng chi phí tháng | total monthly expense, monthly expense |  | `Chi phí hàng tháng của KH là bao nhiêu?`; `Tổng expense mỗi tháng là gì?` |

## Field Catalog

| Field Name | Meaning | Source Tables |
|---|---|---|
| `customer_code` | ID khách hàng tại Techcombank | ai_frontline_customer_info, ai_frontline_customer_event, ai_frontline_customer_statistic, ai_frontline_finance_profile |
| `rm_id` | ID của Chuyên viên đang chăm sóc khách hàng | ai_frontline_customer_info |
| `customer_name` | Họ tên của khách hàng | ai_frontline_customer_info |
| `managing_branch` | Mã chi nhánh đang quản lý khách hàng | ai_frontline_customer_info |
| `nationality` | Quốc tịch | ai_frontline_customer_info |
| `gender` | Giới tính | ai_frontline_customer_info |
| `date_of_birth` | Ngày sinh nhật | ai_frontline_customer_info |
| `age` | Tuổi -  viết bằng chữ số | ? |
| `age_group` | Nhóm tuổi | ai_frontline_customer_info |
| `occupation` | Nghề nghiệp | ai_frontline_customer_info |
| `married_status` | Tình trạng hôn nhân | ? |
| `tier` | Hạng hội viên của khách hàng hiện tại tại Techcombank | ai_frontline_customer_info |
| `sub_tier` | Hạng hội viên mức độ chi tiết | ai_frontline_customer_info |
| `program_code` | Mã chương trình để khách hàng đạt hạng hội viên | ai_frontline_customer_info |
| `membership_effective_date` | Ngày hiệu lực của hạng hội viên của khách hàng | ai_frontline_customer_info |
| `membership_review_date` | Ngày đánh giá lại hạng hội viên | ai_frontline_customer_info |
| `membership_expiration_date` | Ngày hết hạn của hạng hội viên | ai_frontline_customer_info |
| `family_member_count` | Số thành viên trong gia đình | ai_frontline_customer_info |
| `ae_2_0_enabled_flag` | Khách hàng có đang sử dụng sản phẩm Auto Earning không? | ai_frontline_customer_info |
| `economic_segment` | Phân khúc kinh tế | ai_frontline_customer_info |
| `marketing_segment` | Phân khúc Marketing | ai_frontline_customer_info |
| `tactical_segment` | Phân khúc chiến thuật | ai_frontline_customer_info |
| `lavender_group` | Phân khúc nhóm khách hàng theo Lavender | ai_frontline_customer_info |
| `engagement_level` | Mức độ gắn kết của khách hàng với Techcombank | ai_frontline_customer_info |
| `bcg_persona` | Phân khúc khách hàng theo BCG | ai_frontline_customer_info |
| `investment_needs_persona` | Nhu cầu đầu tư của khách hàng | ai_frontline_customer_info |
| `customer_journey` | Hành trình khách hàng | ai_frontline_customer_info |
| `professional_investor_flag` | Khách hàng có phải là nhà đầu tư chuyên nghiệp không? | ai_frontline_customer_info |
| `customer_persona` |  | ai_frontline_customer_info |
| `customer_since` | Ngày khách hàng mở tài khoản tại Techcombank | ai_frontline_customer_info |
| `aum_casa_td_cd_bond_fund_avg_last_3m_amount` | Bình quân tài sản của khách trong vòng 90 ngày gần nhất (Only casa, td, cd, bond, fund) | ai_frontline_finance_profile |
| `casa_avg_last_3m_amount` | Bình quân tài sản CASA của khách hàng trong vòng 90 ngày gần nhất ( casa : Current savings accounts - tiền gửi không kì hạn ) | ai_frontline_finance_profile |
| `bond_avg_last_3m_amount` | Bình quân tài sản Bond của khách hàng trong vòng 90 ngày | ai_frontline_finance_profile |
| `fund_avg_last_3m_amount` | Bình quân tài sản Fund của khách hàng trong vòng 90 ngày | ai_frontline_finance_profile |
| `aum_eop_amount` | Tổng tài sản của khách hàng (AUM : Assets Under Management - Tài sản được quản lý) | ai_frontline_finance_profile |
| `casa_eop_amount` | Số dư CASA của khách hàng ( casa : Current savings accounts - tiền gửi không kì hạn ) | ai_frontline_finance_profile |
| `td_eop_amount` | Số dư TD của khách hàng (TD: Term deposit) | ai_frontline_finance_profile |
| `td_1m_to_3m_eop_amount` | Số dư TD có kì hạn từ 1 đến 3 tháng của khách hàng (TD: Term deposit) | ai_frontline_finance_profile |
| `td_4m_to_6m_eop_amount` | Số dư TD có kì hạn từ 4 đến 6 tháng của khách hàng (TD: Term deposit) | ai_frontline_finance_profile |
| `td_7m_to_12m_eop_amount` | Số dư TD có kì hạn từ 7 đến 12 tháng của khách hàng (TD: Term deposit) | ai_frontline_finance_profile |
| `td_over_12m_eop_amount` | Số dư TD có kì hạn trên 12 tháng của khách hàng (TD: Term deposit) | ai_frontline_finance_profile |
| `td_maturing_this_week_balance_amount` | Số dư TD đáo đạn trong tuần này của khách hàng (TD: Term deposit) | ? |
| `td_maturing_this_month_balance_amount` | Số dư TD đáo hạn trong tháng này của khách hàng (TD: Term deposit) | ? |
| `td_fcy_eop_amount` | Số dư TD ngoại tệ của khách hàng (TD: Term deposit) | ai_frontline_finance_profile |
| `cd_max_eop_amount` | Số dư chứng chỉ tiền gửi bảo lộc của khách hàng | ai_frontline_finance_profile |
| `bond_eop_amount` | Số dư Bond của khách hàng | ai_frontline_finance_profile |
| `fund_eop_amount` | Số dư Fund của khách hàng | ai_frontline_finance_profile |
| `lending_all_product_eop_amount` | Tổng số dư Lending (Vay nợ) của khách hàng | ai_frontline_finance_profile |
| `mycash_eop_amount` | Số dư MyCash của khách hàng | ai_frontline_finance_profile |
| `pil_eop_amount` | Số dư PIL (Personal Installment Loan - Khoản vay trả góp cá nhân) vay trả góp tiêu dùng của khách hàng | ai_frontline_finance_profile |
| `trv_by_identification_method_eop_amount` | Tổng giá trị quan hệ của khách hàng tại Techcombank bao gồm các tài sản và các khoản vay | ai_frontline_finance_profile |
| `secured_lending_eop_amount` | Tổng số dư vay có tài sản đảm bảo của khách hàng | ai_frontline_finance_profile |
| `lending_auto_eop_amount` | Số dư vay mua ô tô | ai_frontline_finance_profile |
| `lending_morgage_primary_eop_amount` | Số dư vay mua bất động sản sơ cấp | ai_frontline_finance_profile |
| `lending_topup_loan_eop_amount` | Tổng số dư vay topup | ai_frontline_finance_profile |
| `lending_mortgage_normal_eop_amount` | Số dư vay mua bất động sản thông thường- nhà đất | ai_frontline_finance_profile |
| `lending_mortgage_secondary_non_book_eop_amount` | Số dư vay mua bất động sản thứ cấp ( non-book : không có sổ đỏ) | ai_frontline_finance_profile |
| `lending_mortgage_secondary_red_book_eop_amount` | Số dư vay mua bất động sản thứ cấp ( red-book: có sổ đỏ) | ai_frontline_finance_profile |
| `lending_house_construction_renovation_eop_amount` | Số dư vay mua sửa chữa nhà | ai_frontline_finance_profile |
| `lending_refinancing_eop_amount` | Số dư vay refinancing | ai_frontline_finance_profile |
| `lending_household_by_credit_limit_eop_amount` | Số dư vay credit của hộ kinh doanh | ai_frontline_finance_profile |
| `lending_household_installment_eop_amount` | Số dư vay Installment (vay trả góp) của hộ kinh doanh | ai_frontline_finance_profile |
| `lending_securities_eop_amount` | Số dư vay có tài sản thế chấp là chứng khoán | ai_frontline_finance_profile |
| `lending_savings_pledge_eop_amount` | Số dư vay có tài sản thế chấp là tiền gửi | ai_frontline_finance_profile |
| `lending_credit_card_eop_amount` | Tổng dư nợ thẻ tín dụng của khách hàng | ai_frontline_finance_profile |
| `other_loans_eop_amount` | Tổng dư nợ các khoản vay khác (không thuộc các khoản vay đã liệt kê) | ai_frontline_finance_profile |
| `total_ape_amount` | Tổng giá trị APE ( Annualized Premium Equivalent - tổng phí quy năm của bảo hiểm) | ai_frontline_finance_profile |
| `net_change_aum_t1_amount` | Tổng giá trị biến động tất cả tài sản của khách hàng tại ngày gần nhất | ai_frontline_finance_profile |
| `casa_net_change_aum_t1_amount` | Giá  trị biến động CASA của khách hàng tại ngày gần nhất  ( casa : Current savings accounts - tiền gửi không kì hạn ) | ai_frontline_finance_profile |
| `td_net_change_aum_t1_amount` | Giá trị biến động TD của khách hàng tại ngày gần nhất (Term Deposit - Tiền gửi có kỳ hạn) | ai_frontline_finance_profile |
| `cd_net_change_aum_t1_amount` | Giá trị biến động CD của khách hàng tại ngày gần nhất (Certificate of Deposit - Chứng chỉ tiền gửi) | ai_frontline_finance_profile |
| `bond_net_change_aum_t1_amount` | Giá trị biến động bond của khách hàng tại ngày gần nhất | ai_frontline_finance_profile |
| `fund_net_change_aum_t1_amount` | Giá  trị biến động fund của khách hàng tại ngày gần nhất | ai_frontline_finance_profile |
| `casa_largest_net_change_in_t1_amount` | Biến động lớn nhất giá trị tiền vào CASA của khách hàng tại ngày gần nhất ( casa : Current savings accounts - tiền gửi không kì hạn ) | ai_frontline_finance_profile |
| `td_largest_net_change_in_t1_amount` | Biến động lớn nhất giá trị tiền vào td của khách hàng tại ngày gần nhất (td: Term Deposit - Tiền gửi có kỳ hạn) | ai_frontline_finance_profile |
| `cd_largest_net_change_in_t1_amount` | Biến động lớn nhất giá trị tiền vào chứng chỉ tiền gửi (CD) của khách hàng tại ngày gần nhất | ai_frontline_finance_profile |
| `bond_largest_net_change_in_t1_amount` | Biến động lớn nhất giá trị tiền vào trái phiếu của khách hàng tại ngày gần nhất | ai_frontline_customer_statistic |
| `fund_largest_net_change_in_t1_amount` | Biến động lớn nhất giá trị tiền vào fund của khách hàng tại ngày gần nhất | ai_frontline_customer_statistic |
| `casa_largest_net_change_out_t1_amount` | Biến động lớn nhất giá trị tiền ra casa của khách hàng tại ngày gần nhất ( casa : Current savings accounts - tiền gửi không kì hạn ) | ai_frontline_customer_statistic |
| `td_largest_net_change_out_t1_amount` | Biến động lớn nhất giá trị tiền ra td của khách hàng tại ngày gần nhất (td: Term Deposit - Tiền gửi có kỳ hạn) | ai_frontline_customer_statistic |
| `cd_largest_net_change_out_t1_amount` | Biến động lớn nhất giá trị tiền ra chứng chỉ tiền gửi của khách hàng tại ngày gần nhất | ai_frontline_customer_statistic |
| `bond_largest_net_change_out_t1_amount` | Biến động lớn nhất giá trị tiền ra trái phiếu của khách hàng tại ngày gần nhất | ai_frontline_customer_statistic |
| `fund_largest_net_change_out_t1_amount` | Biến động lớn nhất giá trị tiền ra chứng chỉ tiền gửi của khách hàng tại ngày gần nhất | ai_frontline_customer_statistic |
| `casa_net_change_aum_t30_amount` | Giá  trị biến động casa của khách hàng trong 30 ngày gần nhất ( casa : Current savings accounts - tiền gửi không kì hạn ) | ai_frontline_customer_statistic |
| `td_net_change_aum_t30_amount` | Giá  trị biến động td của khách hàng trong 30 ngày gần nhất (td: Term Deposit - Tiền gửi có kỳ hạn) | ai_frontline_customer_statistic |
| `cd_net_change_aum_t30_amount` | Giá  trị biến động chứng chỉ tiền gửi của khách hàng trong 30 ngày gần nhất | ai_frontline_customer_statistic |
| `bond_net_change_aum_t30_amount` | Giá  trị biến động trái phiếu của khách hàng trong 30 ngày gần nhất | ai_frontline_customer_statistic |
| `fund_net_change_aum_t30_amount` | Giá  trị biến động chứng chỉ quỹ của khách hàng trong 30 ngày gần nhất | ai_frontline_customer_statistic |
| `largest_net_change_in_t30_casa_amount` | Biến động lớn nhất giá trị tiền vào của khách hàng trong 30 ngày gần nhất | ai_frontline_customer_statistic |
| `largest_net_change_in_t30_td_amount` | Biến động lớn nhất giá trị tiền vào sản phẩm TD của khách hàng trong 30 ngày gần nhất (td: Term Deposit - Tiền gửi có kỳ hạn) | ai_frontline_customer_statistic |
| `largest_net_change_in_t30_cd_amount` | Biến động lớn nhất giá trị tiền vào sản phẩm chứng chỉ tiền gửi của khách hàng trong 30 ngày gần nhất | ai_frontline_customer_statistic |
| `largest_net_change_in_t30_bond_amount` | Biến động lớn nhất giá trị tiền vào sản phẩm trái phiếu của khách hàng trong 30 ngày gần nhất | ai_frontline_customer_statistic |
| `largest_net_change_in_t30_fund_amount` | Biến động lớn nhất giá trị tiền vào sản phẩm chứng chỉ quỹ của khách hàng trong 30 ngày gần nhất | ai_frontline_customer_statistic |
| `largest_net_change_out_t30_casa_amount` | Biến động lớn nhất giá trị tiền ra của khách hàng trong 30 ngày gần nhất | ai_frontline_customer_statistic |
| `largest_net_change_out_t30_td_amount` | Biến động lớn nhất giá trị tiền ra sản phẩm TD của khách hàng trong 30 ngày gần nhất (td: Term Deposit - Tiền gửi có kỳ hạn) | ai_frontline_customer_statistic |
| `largest_net_change_out_t30_cd_amount` | Biến động lớn nhất giá trị tiền ra sản phẩm chứng chỉ tiền gửi của khách hàng trong 30 ngày gần nhất | ai_frontline_customer_statistic |
| `largest_net_change_out_t30_bond_amount` | Biến động lớn nhất giá trị tiền ra sản phẩm trái phiếu của khách hàng trong 30 ngày gần nhất | ai_frontline_customer_statistic |
| `largest_net_change_out_t30_fund_amount` | Biến động lớn nhất giá trị tiền ra sản phẩm chứng chỉ quỹ của khách hàng trong 30 ngày gần nhất | ai_frontline_customer_statistic |
| `total_casa_at_tcb_eop_amount` | Tổng giá trị Casa của khách hàng tại Techcombank | ai_frontline_finance_profile |
| `total_casa_at_other_fi_eop_amount` | Tổng giá trị Casa của khách hàng tại các tổ chức tín dụng khác | ai_frontline_finance_profile |
| `total_liquid_asset_at_tcb_amount` | Tổng giá trị tài sản lỏng của khách hàng tại Techcombank | ai_frontline_finance_profile |
| `total_liquid_asset_at_other_fi_amount` | Tổng giá trị tài sản lỏng của khách hàng tại tổ chức tín dụng khác | ai_frontline_finance_profile |
| `total_shared_capital_asset_value_amount` | Giá trị walletshare của khách hàng tại Techcombank | ai_frontline_finance_profile |
| `total_fixed_asset_value_amount` | Tổng giá trị tài sản cố định của khách hàng tại Techcombank và ngoài Techcombank | ai_frontline_finance_profile |
| `total_non_fixed_asset_value_amount` | Tổng giá trị tài sản không cố định của khách hàng tại Techcombank và ngoài Techcombank | ai_frontline_finance_profile |
| `total_asset_value_amount` | Tổng giá trị tài sản của khách hàng tại Techcombank và ngoài Techcombank | ai_frontline_finance_profile |
| `total_mortgage_and_auto_eop_amount` | Tổng giá trị vay mua nhà và ô tô của khách hàng tại Techcombank và ngoài Techcombank | ai_frontline_finance_profile |
| `total_secured_loan_amount` | Tổng giá trị vay của khách hàng có tài sản đảm bảo tại Techcombank và ngoài Techcombank | ai_frontline_finance_profile |
| `total_secured_loan_at_other_fi_amount` | Tổng giá trị vay của khách hàng có tài sản đảm bảo ngoài Techcombank | ai_frontline_finance_profile |
| `total_unsecured_loan_at_tcb_amount` | Tổng giá trị vay của khách hàng không có tài sản đảm bảo tại Techcombank | ai_frontline_finance_profile |
| `total_unsecured_loan_at_other_fi_amount` | Tổng giá trị vay của khách hàng không có tài sản đảm bảo ngoài Techcombank | ai_frontline_finance_profile |
| `total_liabilities_value_amount` | Tổng dư nợ của khách hàng tại Techcombank và ngoài Techcombank | ai_frontline_finance_profile |
| `net_assets_value_amount` | Chênh lệnh tài sản của KH tại Techcombank & ngoài Techcombank với dư nợ của khách hàng tại Techcombank & ngoài Techcombank | ai_frontline_finance_profile |
| `total_monthly_salary_income_amount` | Thu nhập hàng tháng từ tiền công tiền lương của khách hàng | ai_frontline_finance_profile |
| `total_monthly_real_estate_rental_income_amount` | Thu nhập từ cho thuê nhà | ai_frontline_finance_profile |
| `total_monthly_car_rental_income_amount` | Thu nhập từ cho thuê ô tô | ai_frontline_finance_profile |
| `total_monthly_entrepreneurial_income_amount` | Thu nhập từ hoạt động kinh doanh của khách hàng | ai_frontline_finance_profile |
| `total_monthly_other_income_amount` | Thu nhập khác | ai_frontline_finance_profile |
| `total_monthly_income_amount` | Tổng thu nhập hàng tháng của khách hàng | ai_frontline_finance_profile |
| `total_monthly_fixed_expense_amount` | Chi phí cố định hàng tháng của khách hàng | ai_frontline_finance_profile |
| `total_monthly_medical_expense_amount` | Chi phí cho y tế hàng tháng | ai_frontline_finance_profile |
| `total_monthly_education_expense_amount` | Chi phí cho giáo dục hàng tháng | ai_frontline_finance_profile |
| `total_monthly_holiday_expense_amount` | Chi phí cho du lịch hàng tháng | ai_frontline_finance_profile |
| `total_monthly_other_expense_amount` | Các chi phí khác | ai_frontline_finance_profile |
| `total_monthly_expense_amount` | Tổng chi phí hàng tháng của khách hàng | ai_frontline_finance_profile |
| `net_monthly_income_amount` | Chênh lệch giữa thu nhập và chi phí của khách hàng | ai_frontline_finance_profile |
| `pre_approval_unsecured_bundle_limit_amount` | Hạn mức phê duyệt trước của sản phẩm cho vay không tài sản đảm bảo | ai_frontline_customer_info |
| `pre_approval_shopcash_amount` | Hạm mức phê duyệt trước của Shopcash | ai_frontline_customer_info |
| `pre_approval_mycash_amount` | Hạn mức phê duyệt trước của Mycash | ai_frontline_customer_info |
| `pre_approval_credit_card_amount` | Hạn mức phê duyệt trước của thẻ tín dụng | ai_frontline_customer_info |
| `pre_approval_shopcredit_amount` | Hạn mức phê duyệt trước của Shopcredit | ai_frontline_customer_info |
| `pre_approval_bundle_limit_shopcredit_plus_shopcash_amount` | Hạn mức phê duyệt trước của Shopcredit + shopscash | ai_frontline_customer_info |
| `pre_approval_unsecured_bundle_limit_expiration_date_amount` | Ngày hết hiệu lực hạn mức phê duyệt trước của cho vay không tài sản đảm bảo | ai_frontline_customer_info |
| `pre_approval_shopcash_expiration_date` | Ngày hết hiệu lực hạn mức phê duyệt trước cho vay shopcash | ai_frontline_customer_info |
| `pre_approval_mycash_expiration_date` | Ngày hết hiệu lực hạn mức phê duyệt trước cho mycash | ai_frontline_customer_info |
| `pre_approval_ccb_expiration_date` | Ngày hết hiệu lực hạn mức phê duyệt trước thẻ tín dụng | ai_frontline_customer_info |
| `pre_approval_shopcredit_expiration_date` | Ngày hết hiệu lực hạn mức phê duyệt trước của shopcredit | ai_frontline_customer_info |
| `pre_approval_bundle_limit_shopcredit_plus_shopcash_expiration_date` | Ngày hết hiệu lực hạn mức phê duyệt trước của shopcredit + shopcash | ai_frontline_customer_info |
| `product_holding` | Số sản phẩm khách hàng đang sử dụng tại Techcombank | ai_frontline_customer_info |
| `eb_fmb_registration_status` | Khách hàng có đang sử dụng app TCBM (techcombank mobile) không? | ai_frontline_customer_info |
| `securities_account_at_tcbs_status` | KH có tài khoản chứng khoán tại TCBS (techcombank securities) không? | ai_frontline_customer_info |
| `lucky_account_status` | KH có tài khoản techcombank reward | ai_frontline_customer_info |
| `cd_max_registration_status` | KH có đăng kí CD max không (CD: Certificates of deposit) | ai_frontline_customer_info |
| `cd_max_active_status` | Tài khoản CD max đang active không (CD: Certificates of deposit) | ai_frontline_customer_info |
| `debit_card_type` | Loại thẻ ghi nợ | ai_frontline_finance_profile |
| `debit_card_transaction_last_3m_count` | Số lượng giao dịch trong 3 tháng gần nhất của thẻ ghi nợ | ai_frontline_finance_profile |
| `debit_card_transaction_last_3m_amount` | Tổng giá trị giao dịch trong 3 tháng gần nhất của thẻ ghi nợ | ai_frontline_finance_profile |
| `credit_card_count` | Số lượng thẻ tín dụng khách hàng sử dụng | ai_frontline_finance_profile |
| `supplementary_credit_card_count` | Số lượng thẻ phụ của khách hàng | ai_frontline_finance_profile |
| `credit_card_type` | Loại thẻ tín dụng của khách hàng | ai_frontline_finance_profile |
| `credit_card_transaction_last_3m_count` | Số lượng giao dịch trong 3 tháng gần nhất của thẻ tín dụng | ai_frontline_finance_profile |
| `credit_card_transaction_last_3m_amount` | Tổng giá trị giao dịch trong 3 tháng gần nhất của thẻ tín dụng | ai_frontline_finance_profile |
| `apple_pay_registration_status` | Khách hàng có đăng kí thanh toán qua apple pay không? | ai_frontline_customer_info |
| `fx_usage_status` | Khách hàng có giao dịch mua bán ngoại tệ không? | ai_frontline_customer_info |
| `td_product_held_flag` | KH đã từng sử dụng TD chưa? (td: Term Deposit - Tiền gửi có kỳ hạn) | ai_frontline_customer_info |
| `cd_product_held_flag` | KH đã từng sử dụng chứng chỉ tiền gửi chưa? | ai_frontline_customer_info |
| `bond_product_held_flag` | KH đã từng sử dụng trái phiếu chưa? | ai_frontline_customer_info |
| `fund_product_held_flag` | KH đã từng sử dụng chứng chỉ tiền gửi chưa? | ai_frontline_customer_info |
| `lending_product_count` | Tổng số sản phẩm vay khách hàng đang sử dụng | ai_frontline_finance_profile |
| `lending_outstanding_amount` | Tổng số dư sản phẩm vay của khách hàng | ai_frontline_finance_profile |
| `insurance_contract_ytd_count` | Tổng số hợp đồng bảo hiểm tính lũy kế từ đầu năm | ai_frontline_finance_profile |
| `ape_ytd_amount` | Tổng phí bảo hiểm lũy kế từ đầu năm của khách hàng | ai_frontline_finance_profile |
| `nearest_birth_date` | Ngày sinh nhật sắp tới của khách hàng | ai_frontline_customer_statistic |
| `nearest_debit_card_expiration_date` | Ngày hết hạn thẻ ghi nợ gần nhất sắp tới của khách hàng | ai_frontline_customer_statistic |
| `nearest_credit_card_expiration_date` | Ngày hết hạn thẻ tín dụng gần nhất sắp tới của khách hàng | ai_frontline_customer_statistic |
| `nearest_credit_card_due_date` | Ngày hết hạn thanh toán dư nợ của thẻ tín dụng gần nhất sắp tới của khách hàng | ai_frontline_customer_statistic |
| `trigger_credit_card_expiry_han_2thangsau_date` |  | N/A |
| `nearest_td_maturity_date` | Ngày đáo hạn hợp đồng tiền gửi sắp tới gần nhất | ai_frontline_customer_statistic |
| `nearest_cd_maturity_date` | Ngày đáo hạn hợp đồng chứng chỉ tiền gửi sắp tới gần nhất | ai_frontline_customer_statistic |
| `nearest_coupon_bond_maturity_date` | Ngày đáp hạn trái phiếu/ nhận lãi trái phiếu sắp tới gần nhất | ai_frontline_customer_statistic |
| `nearest_secured_loan_due_date` | Ngày đến hạn thanh toán nợ có tài sản đảm bảo sắp tới gần nhất | ai_frontline_customer_statistic |
| `nearest_f1_due_date` | Ngày đến hạn thanh toán nợ F1 sắp tới gần nhất | ai_frontline_customer_statistic |
| `nearest_f2_due_date` | Ngày đến hạn thanh toán nợ  F2 sắp tới gần nhất | ai_frontline_customer_statistic |
| `nearest_mycash_due_date` | Ngày đến hạn thanh toán dư nợ mycash sắp tới gần nhất | ai_frontline_customer_statistic |
| `nearest_other_product_due_date` | Ngày đến hạn khác | ai_frontline_customer_statistic |
| `nearest_insurance_contract_anniversary_date` | Ngày kỷ niệm hợp đồng bảo hiểm gần nhất | ai_frontline_customer_statistic |
| `content_com_interest_level` | Mức độ quan tâm về nội dung truyền thông | ai_frontline_customer_info |
| `eb_fmb_registration_status` | Trạng thái đăng ký e-banking | ai_frontline_customer_info |
| `product_com_interested_last_3m` |  | ai_frontline_finance_profile |
| `risk_appetite` | khẩu vị rủi ro của khách hàng | ai_frontline_customer_info |
| `last_done_deal_date` | Ngày done deal với khách hàng gần nhất | ai_frontline_finance_profile |
| `last_done_deal_product` | Lần gần nhất khách hàng sử dụng sản phẩm của Techcombank | ai_frontline_finance_profile |
| `last_close_lost_date` | Ngày khách hàng từ chối sử dụng sản phẩm của Techcombank gần nhất | ai_frontline_finance_profile |
| `last_close_lost_product` | Lần gần nhất khách hàng từ chối sử dụng sản phẩm của Techcombank | ai_frontline_finance_profile |
| `nbo_1` | Sản phẩm tiềm năng nhất cho khách hàng tại thời điểm (NBO : Next best offers - Product level 1) | ai_frontline_finance_profile |
| `nbo_2` | Sản phẩm tiềm năng thứ 2 cho khách hàng tại thời điểm (NBO : Next best offers - Product level 1) | ai_frontline_finance_profile |
| `nbo_3` | Sản phẩm tiềm năng thứ 3 cho khách hàng tại thời điểm (NBO : Next best offers - Product level 1) | ai_frontline_finance_profile |
| `buying_signal_nbo_1` | Tín hiệu mua của sản phẩm tiềm năng nhất cho khách hàng | ai_frontline_finance_profile |
| `buying_signal_nbo_2` | Tín hiệu mua của sản phẩm tiềm năng thứ 2 cho khách hàng | ai_frontline_finance_profile |
| `buying_signal_nbo_3` | Tín hiệu mua của sản phẩm tiềm năng thứ 3 cho khách hàng | ai_frontline_finance_profile |
| `nbo_1_explanation` | Giải thích vì sao sản phẩm này là sản phẩm tiềm năng nhất cho khách hàng tại thời điểm | ai_frontline_finance_profile |
| `nbo_2_explanation` | Giải thích vì sao sản phẩm này là sản phẩm tiềm năng thứ 2 cho khách hàng tại thời điểm | ai_frontline_finance_profile |
| `nbo_3_explanation` | Giải thích vì sao sản phẩm này là sản phẩm tiềm năng thứ 3 cho khách hàng tại thời điểm | ai_frontline_finance_profile |
| `nba` | Gợi ý next action với khách hàng | N/A |

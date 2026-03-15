---
title: "Customer Overview Dashboard Schema"
description: "Contract adapter cho Customer Overview Dashboard, chuẩn hóa từ field thật trong Data Lake sample sang payload FE hiện tại."
created: 2026-03-05
updated: 2026-03-12
tags: [ai-frontline-poc, dashboard, schema, customer-360, urd]
status: draft
---
# Customer Overview Dashboard Schema

## Scope

Tài liệu này chuẩn hóa contract dữ liệu cho dashboard overview mà FE đang render.

Nguồn canonical của field thật nằm ở:
- `ui-mapping.md`
- `data-lake-metadata.md`
- `ai_frontline_customer_info.json`
- `ai_frontline_finance_profile.json`

Tài liệu này không còn là mock payload độc lập; nó mô tả shape adapter mà backend build ra từ dữ liệu thật.

## Block Inventory


| Block Key          | Block Name (VI)                      | Block Name (UI)        | Type   |
| -------------------- | -------------------------------------- | ------------------------ | -------- |
| `demographics`     | Nhân khẩu học khách hàng        | Header                 | object |
| `product_holdings` | Danh mục sản phẩm đang nắm giữ | Product holdings       | object |
| `assets`           | Cơ cấu tài sản                   | Assets                 | object |
| `liabilities`      | Cơ cấu nợ                         | Liabilities            | object |
| `average_aum`      | Xu hướng AUM trung bình 24 tháng | Average AUM            | object |
| `income_expenses`  | Thu nhập và chi tiêu              | Income / Expenses      | object |
| `next_best_offers` | Top đề xuất sản phẩm tiếp theo | Top 3 next best offers | array  |

## 1) Demographics (Ô đầu tiên: Nhân khẩu học)


| Field Key                | UI Label                   | Data Type | Format       | Required | Example        |
| -------------------------- | ---------------------------- | ----------- | -------------- | ---------- | ---------------- |
| `customer_name`          | (header line)              | string    | text         | yes      | `Nguyen van A` |
| `cif`                    | (header line)              | string    | customer id  | yes      | `Cus1`         |
| `age`                    | tuổi, tuoi...             | integer   | years        | yes      | `34`           |
| `segment`                | `Segment`                  | string    | enum         | yes      | `Mass Affluent` |
| `tier`                   | `Tier`                     | string    | enum         | yes      | `Gold`         |
| `membership_expiry_date` | `Membership expiry date`   | string    | `DD/MM/YYYY` | yes      | `31/12/2026`   |
| `vip_program`            | `VIP program`              | string    | code         | yes      | `PRG2026A`     |
| `customer_group`         | `Lavender group`           | string    | enum         | no       | `Group-2`      |
| `risk_level`             | `Risk level`               | string    | enum         | yes      | `Medium`       |
| `cic_score`              | `CIC score`                | integer   | `0..900`     | yes      | `710`          |
| `cic_score_max`          | `CIC score`                | integer   | constant     | yes      | `900`          |

## 2) Product Holdings


| Field Key                 | UI Label    | Data Type     | Format     | Required | Example         |
| --------------------------- | ------------- | --------------- | ------------ | ---------- | ----------------- |
| `products`                | `Products`  | array<object> | list       | yes      | xem bên dưới |
| `products[].product_name` | product row | string        | text       | yes      | `Deposit`       |
| `products[].balance_vnd`  | `Balance`   | integer       | VND amount | yes      | `11580313531`   |
| `pagination.page_size`    | pager       | integer       | `>=1`      | no       | `5`             |
| `pagination.current_page` | pager       | integer       | `>=1`      | no       | `1`             |
| `pagination.total_items`  | pager       | integer       | `>=0`      | no       | `15`            |

## 3) Assets


| Field Key                   | UI Label    | Data Type     | Format       | Required | Example         |
| ----------------------------- | ------------- | --------------- | -------------- | ---------- | ----------------- |
| `distribution`              | pie legend  | array<object> | percent list | yes      | xem bên dưới |
| `distribution[].category`   | legend item | string        | enum         | yes      | `CASA at TCB`   |
| `distribution[].percentage` | legend item | number        | `0..100`     | yes      | `31.6`          |

## 4) Liabilities


| Field Key                   | UI Label    | Data Type     | Format       | Required | Example         |
| ----------------------------- | ------------- | --------------- | -------------- | ---------- | ----------------- |
| `distribution`              | pie legend  | array<object> | percent list | yes      | xem bên dưới |
| `distribution[].category`   | legend item | string        | enum         | yes      | `Unsecured loan` |
| `distribution[].percentage` | legend item | number        | `0..100`     | yes      | `80.0`          |

## 5) Average AUM (24 months)


| Field Key          | UI Label    | Data Type     | Format                   | Required | Example         |
| -------------------- | ------------- | --------------- | -------------------------- | ---------- | ----------------- |
| `period_months`    | `24 months` | integer       | available month window   | yes      | `1`             |
| `series`           | line chart  | array<object> | time series              | yes      | xem bên dưới |
| `series[].month`   | x-axis      | string        | `MM/YYYY`                | yes      | `03/2026`       |
| `series[].aum_vnd` | y-axis      | integer       | VND amount               | yes      | `44406231997`   |
| `trend_direction`  | derived     | string        | enum(`up`,`down`,`flat`) | no       | `up`            |

## 6) Income / Expenses


| Field Key                    | UI Label    | Data Type     | Format     | Required | Example                   |
| ------------------------------ | ------------- | --------------- | ------------ | ---------- | --------------------------- |
| `income_items`               | `Income`    | array<object> | list       | yes      | xem bên dưới           |
| `income_items[].name`        | income row  | string        | text       | yes      | `Monthly salary`          |
| `income_items[].amount_vnd`  | income row  | integer       | VND amount | yes      | `5761741660`              |
| `expense_items`              | `Expenses`  | array<object> | list       | yes      | xem bên dưới           |
| `expense_items[].name`       | expense row | string        | text       | yes      | `Fixed expense`           |
| `expense_items[].amount_vnd` | expense row | integer       | VND amount | yes      | `3045330169`              |

## 7) Top 3 Next Best Offers


| Field Key                    | UI Label                 | Data Type     | Format                                       | Required | Example                       |
| ------------------------------ | -------------------------- | --------------- | ---------------------------------------------- | ---------- | ------------------------------- |
| `offers`                     | `Top 3 next best offers` | array<object> | max length = 3                               | yes      | xem bên dưới               |
| `offers[].rank`              | index badge              | integer       | `1..3`                                       | yes      | `1`                           |
| `offers[].offer_type`        | card title               | string        | enum/text                                    | yes      | `Fund`                        |
| `offers[].summary`           | card body                | string        | text                                         | yes      | `High inflow to mutual funds in last quarter.` |
| `offers[].value_proposition` | card body                | string        | text                                         | no       | `Buying signal score: 0.62`   |
| `offers[].cta_text`          | link/button              | string        | text                                         | yes      | `View sale scripts`           |
| `offers[].cta_action`        | action                   | string        | enum(`open_sale_script`,`open_offer_detail`) | yes      | `open_sale_script`            |

## Canonical Output Shape (JSON)

```json
{
  "demographics": {},
  "product_holdings": {
    "products": [],
    "pagination": {}
  },
  "assets": {
    "distribution": []
  },
  "liabilities": {
    "distribution": []
  },
  "average_aum": {
    "period_months": 1,
    "series": []
  },
  "income_expenses": {
    "income_items": [],
    "expense_items": []
  },
  "next_best_offers": {
    "offers": []
  }
}
```

## Notes

- Đây là adapter contract cho FE; source field thật phải đối chiếu ở `ui-mapping.md` và `data-lake-metadata.md`.
- `cif` đang được backend map từ `customer_id` của sample Data Lake hiện tại.
- `period_months` không còn mặc định cố định 24; nó phản ánh số tháng thực có trong sample source sau khi group theo tháng.

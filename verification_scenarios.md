# 🧪 Test Scenarios & Ground Truth (PoC)

This document contains 10 Q&A pairs designed to verify the Text-to-GraphQL agent system. These scenarios cover identity resolution, multi-field retrieval, and business logic mapping.

## 📊 Customer Data Summary (Reference)

- **Cus1: Pham Quang Minh**
  - CASA Balance: 125,000,000 VND
  - Monthly Income: 50,000,000 VND
  - Monthly Expense: 30,000,000 VND
  - Top NBOs: Credit Card, Insurance, Savings
- **Cus2: Chan Thi B**
  - CASA Balance: 45,000,000 VND
  - Total Assets: 2,500,000,000 VND
  - NBO: Mortgage Loan
- **Cus3: Nguyen Van C**
  - CASA Balance: 15,000,000 VND
  - Occupation: Engineer

---

## 🧪 Test Cases

### 1. Identity Resolution & Basic Overview

- **Question**: "Cho tôi thông tin tổng quan về khách hàng Pham Quang Minh"
- **Expected Data**: Name, ID, Occupation, Segment.
- **Ground Truth Answer**: Khách hàng **Phạm Quang Minh** (ID: Cus1) thuộc phân khúc **Private**. Anh là **Giám đốc điều hành** (CEO), hiện đang sinh sống tại Hà Nội.

### 2. Specific Balance Inquiry

- **Question**: "Số dư tài khoản CASA hiện tại của khách hàng Minh là bao nhiêu?"
- **Expected Data**: `casaAccount.availableBalance`
- **Ground Truth Answer**: Số dư tài khoản CASA hiện tại của khách hàng **Phạm Quang Minh** là **125.000.000 VND**.

### 3. Financial Health (Income vs Expense)

- **Question**: "Thu nhập và chi phí hàng tháng của khách hàng có mã Cus1?"
- **Expected Data**: `monthlyIncome`, `monthlyExpense`
- **Ground Truth Answer**: Khách hàng **Phạm Quang Minh** (Cus1) có thu nhập hàng tháng là **50.000.000 VND** và chi phí hàng tháng là **30.000.000 VND**.

### 4. Next Best Offers (NBO)

- **Question**: "Top 3 sản phẩm gợi ý (NBO) cho khách hàng Pham Quang Minh là gì?"
- **Expected Data**: `nboList` (Top 3)
- **Ground Truth Answer**: 3 sản phẩm gợi ý hàng đầu cho khách hàng **Phạm Quang Minh** bao gồm:
  1. Thẻ tín dụng (Credit Card)
  2. Bảo hiểm nhân thọ (Insurance)
  3. Tiền gửi tiết kiệm (Savings)

### 5. Multi-Point Inquiry (AUM & NBO)

- **Question**: "Top NBO và số dư AUM 3 tháng của khách hàng Minh?"
- **Expected Data**: `nboList`, `aum3Month`
- **Ground Truth Answer**: Khách hàng **Phạm Quang Minh** có số dư AUM trung bình 3 tháng là **1.500.000.000 VND**. Các sản phẩm gợi ý (NBO) bao gồm: Thẻ tín dụng, Bảo hiểm và Tiền gửi.

### 6. Search by Full Name (Cus2)

- **Question**: "Khách hàng Chan Thi B có tổng tài sản là bao nhiêu?"
- **Expected Data**: `totalAssets`
- **Ground Truth Answer**: Tổng tài sản (Total Assets) của khách hàng **Chan Thi B** là **2.500.000.000 VND**.

### 7. Product List Inquiry

- **Question**: "Khách hàng Tran Thi B đang sử dụng những sản phẩm nào?"
- **Expected Data**: `productList`
- **Ground Truth Answer**: Khách hàng **Chan Thi B** hiện đang sử dụng các dịch vụ: **Tài khoản thanh toán (CASA)** và **Tiền gửi có kỳ hạn (Term Deposit)**.

### 8. Segment & Occupation (Cus3)

- **Question**: "Thông tin nghề nghiệp và phân khúc của khách hàng Nguyen Van C?"
- **Expected Data**: `occupation`, `customerSegment`
- **Ground Truth Answer**: Khách hàng **Nguyễn Văn C** (Cus3) hiện là **Kỹ sư** (Engineer) và thuộc phân khúc khách hàng **Mass**.

### 9. Liability Inquiry

- **Question**: "Tổng dư nợ hiện tại của khách hàng Minh là bao nhiêu?"
- **Expected Data**: `totalLiabilities`
- **Ground Truth Answer**: Tổng dư nợ hiện tại của khách hàng **Phạm Quang Minh** là **500.000.000 VND**.

### 10. Complex Combined Query

- **Question**: "Cho tôi biết số dư CASA, AUM 3 tháng và sản phẩm gợi ý của khách hàng Tran Thi B"
- **Expected Data**: `casaAccount.availableBalance`, `aum3Month`, `nboList`
- **Ground Truth Answer**: Khách hàng **Chan Thi B** có:
  - Số dư CASA: **45.000.000 VND**
  - AUM trung bình 3 tháng: **2.000.000.000 VND**
  - Sản phẩm gợi ý: **Vay mua nhà (Mortgage Loan)**

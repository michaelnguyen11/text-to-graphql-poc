# 🧪 Comprehensive Verification Scenarios (20 Q&A Pairs)

This document contains 20 Q&A pairs designed to verify the Text-to-GraphQL agent system against the **Data Lake export**. These scenarios cover identity resolution, multi-field retrieval, business logic mapping, and cross-customer verification.

---

## 📊 Reference Data (Data Lake Source of Truth)

### **Cus1: Nguyen van A**

- **Segment**: Mass Affluent | **Tier**: Gold | **Occupation**: CHUYEN
- **Onboarding**: 20/03/2018
- **CASA Balance**: 7,799,609,594 VND
- **Total AUM (Latest)**: 43,074,045,037 VND
- **AUM 3M Average**: 11,089,728,766 VND

### **Cus2: Pham Quang Minh**

- **Segment**: HNW | **Tier**: Diamond | **Persona**: Wealth Builder
- **Occupation**: CHUYEN | **Risk Appetite**: Low
- **Onboarding**: 17/09/2012
- **CASA Balance**: 3,411,502,906 VND
- **AUM (Latest)**: 29,518,668,980 VND | **AUM 3M Average**: 16,726,034,693 VND
- **Bond**: 1,752,169,502 VND | **CD Max**: 7,247,605,953 VND
- **Monthly Income**: 9,946,601,909 VND | **Monthly Expense**: 1,170,840,683 VND
- **Total Liabilities (Lending)**: 62,225,166,216 VND
- **NBOs**: Bond, Fund, Credit Card

### **Cus3: Chan Thi B**

- **Segment**: Affluent | **Tier**: Platinum | **Persona**: Lifestyle Optimizer
- **Onboarding**: 05/07/2021
- **CASA Balance**: 3,573,567,564 VND
- **AUM 3M Average**: 15,805,684,817 VND
- **Monthly Income**: 7,402,623,730 VND
- **NBOs**: Fund, Credit Card, Bond

---

## 🧪 Verification Test Cases

### 1. Identity & Profile (Cus2)

- **Question**: "Cho tôi thông tin tổng quan về khách hàng Pham Quang Minh"
- **Ground Truth**: Khách hàng **Phạm Quang Minh** (ID: Cus2) thuộc phân khúc **HNW**. Anh có persona là **Wealth Builder**, thuộc hạng **Diamond** và đã là khách hàng từ năm 2012.

### 2. Specific Balance (Cus2)

- **Question**: "Số dư tài khoản CASA hiện tại của khách hàng Minh là bao nhiêu?"
- **Ground Truth**: Số dư tài khoản CASA hiện tại của khách hàng **Phạm Quang Minh** là **3.411.502.906 VND**.

### 3. Financial Wellness (Cus2)

- **Question**: "Thu nhập và chi phí hàng tháng của khách hàng Minh?"
- **Ground Truth**: Khách hàng **Phạm Quang Minh** có tổng thu nhập hàng tháng là **9.946.601.909 VND** và tổng chi phí hàng tháng là **1.170.840.683 VND**.

### 4. Direct NBO Inquiry (Cus2)

- **Question**: "Top 3 sản phẩm gợi ý (NBO) cho khách hàng Pham Quang Minh là gì?"
- **Ground Truth**: 3 sản phẩm gợi ý hàng đầu cho anh Minh là: **Trái phiếu (Bond)**, **Quỹ đầu tư (Fund)**, và **Thẻ tín dụng (Credit Card)**.

### 5. Multi-metric Inquiry (Cus2)

- **Question**: "Top NBO và số dư AUM 3 tháng của khách hàng Minh?"
- **Ground Truth**: Anh Minh có số dư AUM trung bình 3 tháng là **16.726.034,693 VND**. Các sản phẩm gợi ý bao gồm Trái phiếu, Quỹ đầu tư và Thẻ tín dụng.

### 6. Tier Search by Name (Cus3)

- **Question**: "Khách hàng Chan Thi B có hạng hội viên là gì?"
- **Ground Truth**: Khách hàng **Chan Thi B** hiện có hạng hội viên là **Platinum**.

### 7. Full Product List (Cus2)

- **Question**: "Khách hàng Pham Quang Minh đang sử dụng những sản phẩm nào?"
- **Ground Truth**: Anh Minh hiện đang sử dụng **8 loại sản phẩm**, bao gồm CASA, Trái phiếu, CD, Thẻ tín dụng, Thẻ ghi nợ và nhiều loại hình vay vốn khác.

### 8. Segment & Job (Cus1)

- **Question**: "Thông tin nghề nghiệp và phân khúc của khách hàng Nguyen van A?"
- **Ground Truth**: Khách hàng **Nguyen van A** (Cus1) có nghề nghiệp là chuyên viên (CHUYEN) và thuộc phân khúc **Mass Affluent**.

### 9. Total Debt Inquiry (Cus2)

- **Question**: "Tổng dư nợ hiện tại của khách hàng Minh là bao nhiêu?"
- **Ground Truth**: Tổng dư nợ Lending của khách hàng **Phạm Quang Minh** là **62.225.166.216 VND**.

### 10. Complex Combined (Cus3)

- **Question**: "Cho tôi biết số dư CASA, AUM 3 tháng và sản phẩm gợi ý của khách hàng Chan Thi B"
- **Ground Truth**: Khách hàng **Chan Thi B** có số dư CASA là **3.573.567.564 VND**, AUM trung bình 3 tháng là **15.805.684.817 VND** và sản phẩm gợi ý hàng đầu là **Quỹ đầu tư (Fund)**.

### 11. Demographics Detail (Cus2)

- **Question**: "Khách hàng Pham Quang Minh bao nhiêu tuổi và làm nghề gì?"
- **Ground Truth**: Anh Minh thuộc nhóm tuổi **45-54** và nghề nghiệp là chuyên viên (CHUYEN).

### 12. Risk & Tier (Cus2)

- **Question**: "Khẩu vị rủi ro và hạng hội viên của anh Minh như thế nào?"
- **Ground Truth**: Khẩu vị rủi ro của anh Minh là **Thấp (Low)** và anh thuộc hạng hội viên **Diamond**.

### 13. Specific Lending (Cus2)

- **Question**: "Anh Minh có khoản vay mua ô tô hay nhà không?"
- **Ground Truth**: Anh Minh có dư nợ vay mua ô tô là **385.314.908 VND** và dư nợ vay mua bất động sản sơ cấp là **8.444.017.101 VND**.

### 14. Total Asset (Cus1)

- **Question**: "Tổng tài sản (AUM) của Nguyen van A là bao nhiêu?"
- **Ground Truth**: Tổng tài sản quản lý (AUM) hiện tại của khách hàng **Nguyen van A** là **43.074.045.037 VND**.

### 15. Relationship Tenure (Cus3)

- **Question**: "Khách hàng Chan Thi B đã giao dịch với ngân hàng từ khi nào?"
- **Ground Truth**: Khách hàng **Chan Thi B** đã gắn bó với ngân hàng từ ngày **05/07/2021**.

### 16. Specific Investment (Cus2)

- **Question**: "Cho tôi biết số dư trái phiếu và chứng chỉ tiền gửi của khách hàng Minh?"
- **Ground Truth**: Anh Minh đang có **1.752.169.502 VND** tiền trái phiếu và **7.247.605.953 VND** tại chứng chỉ tiền gửi CD Max.

### 17. Credit Card Transaction (Cus2)

- **Question**: "Anh Minh có bao nhiêu thẻ tín dụng và tổng chi tiêu thẻ 3 tháng qua là bao nhiêu?"
- **Ground Truth**: Anh Minh có **3 thẻ tín dụng** và tổng giá trị giao dịch thẻ trong 3 tháng gần nhất là **769.510.850 VND**.

### 18. Pre-approval Limits (Cus2)

- **Question**: "Hạn mức phê duyệt trước (pre-approval) MyCash và Shopcash của anh Minh là bao nhiêu?"
- **Ground Truth**: Khách hàng Minh có hạn mức phê duyệt trước MyCash là **9.273.768.782 VND** và Shopcash là **1.324.545 VND**.

### 19. Monthly Inflow (Cus3)

- **Question**: "Tổng thu nhập hàng tháng của khách hàng Chan Thi B là bao nhiêu?"
- **Ground Truth**: Tổng thu nhập hàng tháng của khách hàng **Chan Thi B** là **7.402.623.730 VND**.

### 20. RM & Branch context (Cus2)

- **Question**: "Ai là RM phụ trách khách hàng Pham Quang Minh và thuộc chi nhánh nào?"
- **Ground Truth**: Chuyên viên quan hệ khách hàng phụ trách anh Minh là **RM003** tại chi nhánh **Hà Nội**.

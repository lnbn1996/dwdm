# Thông tin chung

Yêu cầu của bài: xem `requirement.txt` (tìm và xử lý dataset, 2–3 mô hình để so sánh, web dự đoán hoặc gợi ý, báo cáo).

## Đề tài
**Hệ thống dự đoán lựa chọn phương tiện di chuyển của người dân đô thị dựa vào kỹ thuật phân lớp**

- **Hướng nghiên cứu:** từ thông tin về người đi, hộ gia đình và chuyến đi, phân lớp phương tiện thành 5 lớp: xe máy, ô tô, xe đạp/xe điện, đi bộ, công cộng + taxi (chốt 14/11/2026).
- **Giải thuật (chốt 13/11/2026):** k-Nearest Neighbors (kNN), Decision Tree, Random Forest.
- **Feature (chốt 14/11/2026):** 12 feature dùng chung cho cả 3 giải thuật (tuổi, giới tính, nghề nghiệp, mục đích chuyến đi, quãng đường, số chuyến mỗi tuần, số ô tô / xe máy / xe đạp + xe điện của hộ, loại nhà, tình trạng cư trú, hình thức sở hữu nhà). kNN: `weights="distance"`, k=5.
- **Dữ liệu thực nghiệm:** khảo sát người dân Hà Nội năm 2021 (dự án UTM-Hanoi), 26.106 dòng × 56 cột, CC BY 4.0.
    - Kết quả phản ánh bối cảnh nội đô Hà Nội. Đô thị khác cần huấn luyện lại bằng dữ liệu địa phương.
    - Không diễn đạt là "dự đoán của người Hà Nội".
- **Dùng bản gốc OSF**, không dùng bản Kaggle: https://doi.org/10.17605/OSF.IO/497US
- **Trích dẫn đầy đủ:**
    1. Kieu, M., Comber, A., Nguyen Thi Thuy, H., Bui Quang, T., Phe Hoang Huu, & Malleson, N. (2024). An open dataset on individual perceptions of transport policies. *Scientific Data*, 11, 104. https://doi.org/10.1038/s41597-024-02950-9
    2. Dự án UTM-Hanoi (2023). *UTM-Hanoi* [bộ dữ liệu, file `hn_survey_26k.csv`]. Open Science Framework. https://doi.org/10.17605/OSF.IO/497US. CC BY 4.0.

## Nội dung thư mục

| Đường dẫn | Vai trò |
| --- | --- |
| `AI-LOG.md` | Nhật ký: đã làm gì, đang vướng gì, cần xác nhận gì, việc tiếp theo. **Đọc trước tiên.** |
| `requirement.txt` | Yêu cầu bài tập nhóm (bản sao từ w0) |
| `demo/` | Web demo Streamlit + script huấn luyện của AI (chỉ để hình dung, không phải sản phẩm cuối) |
| `ai_notes/` | Script khảo sát UTM-Hanoi của AI (bản sao từ w0) |

Còn ở `w0/` (không chuyển): `ai_notes/` đầy đủ (lịch sử khảo sát các dataset đã loại), `demo_luong/`, `demo_coupon/`, `docs/` (slide, giáo trình).
Tài liệu các vòng chọn đề tài: https://claude.ai/artifact/KBfmBUh2BDnAqhATrqQrzw (tab "Đề tài đã chốt: Phương tiện di chuyển đô thị").

## Chạy demo

Từ thư mục gốc `D:\CaoHoc\DWDM`:

```powershell
$env:PYTHONIOENCODING = "utf-8"
.venv\Scripts\python.exe assignment\w1\demo\train.py
.venv\Scripts\streamlit.exe run assignment\w1\demo\app.py
```

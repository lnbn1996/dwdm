# Demo web – Hệ thống dự đoán lựa chọn phương tiện di chuyển của người dân đô thị dựa vào kỹ thuật phân lớp

> **Bản demo chính thức của nhóm** dùng để báo cáo (từ 14/11/2026).
>
> Giao diện: thanh tiêu đề cố định; thanh tab dính ngay dưới (bấm tab nào hiện tab đó, tab đang chọn tô màu teal); thứ tự tab: Dự đoán phương tiện · So sánh mô hình · Dữ liệu gốc · Làm sạch & chọn cột · Khám phá dữ liệu · Phương tiện thay thế khi cấm xe máy; footer gọn ghi môn học, lớp, nhóm, danh sách thành viên và nguồn dữ liệu. Tông màu xanh lục đậm (teal), đặt ở `D:\CaoHoc\DWDM\.streamlit\config.toml` và trong CSS đầu `app.py` (`PRIMARY`, `PRIMARY_DARK`). Thông tin nhóm khai báo trong `common.py` (`COURSE`, `CLASS_NAME`, `GROUP_NAME`, `MEMBERS`).

## Hướng nghiên cứu và phạm vi dữ liệu

- **Hướng nghiên cứu:** dự đoán lựa chọn phương tiện di chuyển của người đô thị bằng các kỹ thuật phân lớp.
- **Dữ liệu thực nghiệm:** khảo sát người dân Hà Nội năm 2021 (dự án UTM-Hanoi).
    - 26.106 người trả lời, do Tổng cục Thống kê thực hiện qua điện thoại.
    - Theo bài báo, mẫu lấy ngẫu nhiên 2,5% số hộ ở 4 quận trung tâm: Hoàn Kiếm, Ba Đình, Hai Bà Trưng, Đống Đa.
    - Kết quả mô hình vì vậy phản ánh bối cảnh nội đô Hà Nội. Muốn áp dụng cho đô thị khác thì giữ nguyên quy trình nhưng phải huấn luyện lại bằng dữ liệu địa phương.
- **File:** `data/hn_survey_26k.csv`, bản gốc tải từ OSF, gồm 26.106 dòng × 56 cột.

## Nguồn dữ liệu (trích dẫn)

1. Kieu, M., Comber, A., Nguyen Thi Thuy, H., Bui Quang, T., Phe Hoang Huu, & Malleson, N. (2024). An open dataset on individual perceptions of transport policies. *Scientific Data*, 11, 104. https://doi.org/10.1038/s41597-024-02950-9
2. Dự án UTM-Hanoi (2023). *UTM-Hanoi* [bộ dữ liệu, file `hn_survey_26k.csv`]. Open Science Framework. https://doi.org/10.17605/OSF.IO/497US. Giấy phép CC BY 4.0, truy cập ngày 01/11/2026.

Nội dung nguồn ở trên được khai báo một lần trong `common.py` (`DATA_SCOPE`, `CITATIONS`, `SOURCE_SHORT`) và hiển thị ở tab "Dữ liệu gốc" cùng chân trang của demo.

**Không dùng bản Kaggle "Vehicle at Ha Noi"**, vì bản đó:
- thiếu 516 dòng;
- có thêm một dòng tổng ở cuối file;
- có cột `OD_dist_km` bị nhân nhầm 1,609. Thực ra `OD_dist` ở bản gốc đã là km đường chim bay.

## Bài toán

- **Nhãn:** phương tiện của chuyến đi chính, gộp thành 5 lớp: Xe máy / Ô tô / Xe đạp hoặc xe điện / Đi bộ / Công cộng + taxi (bus, taxi, tàu điện).
- **12 feature:** tuổi, giới tính, nghề nghiệp, mục đích chuyến đi, quãng đường (chia 5 mức), số chuyến mỗi tuần, số ô tô / xe máy / xe đạp + xe điện của hộ, loại nhà ở, tình trạng cư trú, hình thức sở hữu nhà. Nhãn tiếng Việt của 3 cột nhà ở là diễn giải tạm, cần đối chiếu từ điển dữ liệu.
- **kNN:** `weights="distance"`, k=5 (chốt 14/11/2026). Decision Tree và Random Forest dùng tham số mặc định của demo.

## Chạy

Từ thư mục gốc `D:\CaoHoc\DWDM` (bắt buộc chạy từ đây để Streamlit đọc được theme trong `.streamlit/config.toml`):

```powershell
$env:PYTHONIOENCODING = "utf-8"
.venv\Scripts\python.exe assignment\w1\demo\train.py          # ~1 phút, tạo artifacts/
.venv\Scripts\streamlit.exe run assignment\w1\demo\app.py      # mở http://localhost:8501
```

## Cấu trúc

| File | Vai trò |
| --- | --- |
| `common.py` | Tên đề tài, phạm vi dữ liệu và trích dẫn; bảng Việt hoá giá trị; nhóm nhãn (`GROUP`); danh sách cột lộ nhãn (`LEAK`); hàm `clean()` (bỏ trùng, bỏ quãng đường bất thường, tạo feature) và hai bộ tiền xử lý (`make_preprocessor` cho cây, `make_knn_preprocessor` có chuẩn hóa MinMax cho kNN) |
| `train.py` | EDA dữ liệu gốc → làm sạch → chia train/test 80/20 → kNN (k=5, weights="distance"), Decision Tree, Random Forest → chọn bằng CV macro-F1 trên train → đánh giá trên test → thí nghiệm rò rỉ nhãn → lưu `artifacts/` |
| `app.py` | Streamlit, 6 tab (xem thứ tự ở đầu file này); nội dung các tab: Dữ liệu gốc (kèm nguồn) · Làm sạch & chọn cột · Khám phá · So sánh mô hình · Dự đoán phương tiện · Nếu cấm xe máy |

## Kết quả lần chạy 14/11/2026

5 nhãn, 12 feature; tập test gồm 4.860 chuyến.

| Mô hình | CV macro-F1 (train) | Accuracy | Macro-F1 |
| --- | --- | --- | --- |
| Random Forest | 0,591 | 0,838 | 0,612 |
| kNN (`distance`, k=5) | 0,582 | 0,804 | 0,594 |
| Decision Tree | 0,567 | 0,801 | 0,590 |
| Luôn đoán xe máy | — | 0,570 | 0,145 |

Các lần chạy cũ (4 nhãn, 9 feature) không so trực tiếp được vì khác số nhãn. Nếu thêm các cột lộ nhãn (thời gian/tốc độ, lý do chọn, tần suất dùng xe), accuracy tăng giả lên 0,860–0,874.

Số đo thử với 9 / 12 / 13 feature và nhiều giá trị k nằm ở `../ai_notes/` (`so_sanh_5nhan_ketqua.json`, `chon_k_ketqua.json`).

## Các demo cũ

- `../../w0/demo_luong/`: đề tài mức lương.
- `../../w0/demo_coupon/`: đề tài Coupon.

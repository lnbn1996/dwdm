# Báo cáo (bản nháp) – Hệ thống dự đoán lựa chọn phương tiện di chuyển của người dân đô thị dựa vào kỹ thuật phân lớp

> Bản nháp do AI soạn sẵn ngày 14/11/2026 để người dùng bổ sung khi tới bước viết báo cáo. Các số liệu là của lần chạy 14/11 (5 nhãn, 12 feature) và phải cập nhật nếu huấn luyện lại. Mục nào ghi "(chờ bổ sung)" là chưa có nội dung.

## 1. Giới thiệu bài toán (chờ bổ sung)

## 2. Dữ liệu (chờ bổ sung)

Nguồn và trích dẫn xem `demo/common.py` (`DATA_SCOPE`, `CITATIONS`).

## 3. Tiền xử lý và chọn đặc trưng (chờ bổ sung)

## 4. Các mô hình (chờ bổ sung)

kNN (`weights="distance"`, k=5), Decision Tree, Random Forest. Số đo thử với 9 / 12 / 13 feature và nhiều giá trị k: `ai_notes/so_sanh_5nhan_ketqua.json`, `ai_notes/chon_k_ketqua.json`.

## 5. Độ đo đánh giá

Bài toán của đề tài là **phân lớp**: với mỗi chuyến đi, mô hình dự đoán một trong 5 nhãn (xe máy, ô tô, xe đạp / xe điện, đi bộ, công cộng + taxi). Vì vậy nhóm đánh giá bằng các độ đo của bài toán phân lớp: accuracy, precision, recall, F1 (trung bình macro) và ma trận nhầm lẫn. Nhóm không dùng RMSE và MAE.

**Vì sao không dùng RMSE và MAE.** Hai độ đo này đo độ lệch giữa giá trị dự đoán và giá trị thật của một đại lượng số, nên chỉ phù hợp khi đầu ra là một con số. Trong tài liệu môn học, chúng xuất hiện ở bài dự báo (chương Forecasting: sai số của dự báo doanh số) và ở hệ gợi ý khi dự đoán điểm đánh giá (rating prediction). Nhãn phương tiện không có thứ tự và không có khoảng cách: nhầm xe máy thành ô tô hay thành đi bộ đều chỉ là một lần dự đoán sai. Nếu mã hóa nhãn thành các số 0–4 rồi tính RMSE hoặc MAE thì kết quả phụ thuộc vào thứ tự mã hóa tùy ý và không phản ánh chất lượng dự đoán.

**Vì sao không chỉ dùng accuracy.** Dữ liệu mất cân bằng: sau làm sạch có 24.296 chuyến, trong đó xe máy chiếm 13.856 chuyến (57%), còn đi bộ chỉ 473 và công cộng + taxi 735. Một mô hình luôn đoán "xe máy" đã đạt accuracy 0,570 nhưng macro-F1 chỉ 0,145 (lần chạy 14/11). Đây đúng là hạn chế của accuracy với dữ liệu mất cân bằng mà tài liệu môn học nêu ở chương đánh giá mô hình (ví dụ 9.990 mẫu lớp 0 và 10 mẫu lớp 1). Vì vậy nhóm báo cáo thêm **macro-F1**: tính F1 cho từng lớp rồi lấy trung bình, mỗi lớp có trọng số bằng nhau, nên lớp nhỏ bị đoán sai sẽ kéo điểm xuống. Ma trận nhầm lẫn và F1 từng lớp cho thấy mô hình nhầm giữa những nhãn nào.

**Quy tắc dùng độ đo.** Chọn tham số và chọn mô hình bằng macro-F1 qua kiểm định chéo (cross-validation) chỉ trên tập train; tập test (20%, phân tầng theo nhãn) chỉ dùng để báo cáo kết quả cuối.

## 6. Kết quả và thảo luận (chờ bổ sung)

Kết quả lần chạy 14/11 (tập test 4.860 chuyến):

| Mô hình | CV macro-F1 (train) | Accuracy | Macro-F1 |
| --- | --- | --- | --- |
| Random Forest | 0,591 | 0,838 | 0,612 |
| kNN (`distance`, k=5) | 0,582 | 0,804 | 0,594 |
| Decision Tree | 0,567 | 0,801 | 0,590 |
| Luôn đoán xe máy | — | 0,570 | 0,145 |

## 7. Hệ thống web demo (chờ bổ sung)

## 8. Kết luận và hạn chế (chờ bổ sung)

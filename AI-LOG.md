# AI-LOG – nhật ký làm việc của AI (w1)

> Mọi thứ trong file này là **ghi chú của AI**, không phải kết quả chính thức của nhóm.
> Cập nhật cuối: 15/11/2026 (01:15). **Session mới: đọc mục 0 trước**, rồi mục 2 (vướng) và mục 4 (việc tiếp theo).

## 0. Hiện trạng (15/11/2026) – đọc trước khi tiếp tục

**Ưu tiên hiện tại: bài nhóm.** Bài cá nhân (`baitapcanhan/`) tạm gác; người dùng sẽ tự yêu cầu khi cần (còn thiếu lời giải Bài 6, 7, 8, 11, 12, 13, 19 trong `giaibaitap.docx`).

**Đề tài:** "Hệ thống dự đoán lựa chọn phương tiện di chuyển của người dân đô thị dựa vào kỹ thuật phân lớp". Dữ liệu UTM-Hanoi 2021 (bản gốc OSF, `demo/data/hn_survey_26k.csv`).

**Cấu hình đã chốt (14/11):** 5 nhãn (xe máy / ô tô / xe đạp + xe điện / đi bộ / công cộng + taxi); 12 thuộc tính (9 cũ + loại nhà, tình trạng cư trú, sở hữu nhà); 3 giải thuật kNN (`distance`, k=5), Decision Tree (max_depth 10, min_samples_leaf 20), Random Forest (200 cây, min_samples_leaf 5). Kết quả test (4.860 chuyến): RF 0,838 / 0,612; kNN 0,804 / 0,594; DT 0,801 / 0,590 (accuracy / macro-F1). RF là mô hình mặc định.

**Đã xong**

| Hạng mục | Trạng thái | Nơi lưu |
| --- | --- | --- |
| Web demo (Streamlit) | **Demo chính thức** để báo cáo; người dùng đã chạy được trên máy và duyệt giao diện qua nhiều vòng | `demo/app.py`, `demo/common.py`, `demo/train.py`, `demo/artifacts/`, theme `D:\CaoHoc\DWDM\.streamlit\config.toml` |
| Thực nghiệm chọn thuộc tính (9/12/13) và chọn k | Xong (Ghi chú của AI) | `ai_notes/so_sanh_5nhan.py` + `_ketqua.json`, `ai_notes/chon_k.py` + `_ketqua.json` |
| Báo cáo Word | **Bản viết đầy đủ** 28 trang, chờ người dùng đọc lại và bổ sung ảnh | `baocao/baocao-dwdm.docx`, nguồn dựng `baocao/_nguon/` |
| Bản nháp mục "Độ đo" | Đã đưa vào báo cáo (mục 1.4) | `bao_cao_nhap.md` |

**Giao diện web hiện tại (người dùng đã duyệt, giữ nguyên trừ khi được yêu cầu):**
- Thanh tiêu đề cố định nền teal; thanh tab kiểu tab trình duyệt (tab đang chọn nền trắng, nối liền khung nội dung, không viền/vạch trên, không bo góc thanh); dính dưới tiêu đề khi cuộn. Selector CSS dùng `[role="tab"]`, `aria-selected` (các `data-baseweb` không ăn ở Streamlit 1.66 của người dùng).
- 6 tab, không đánh số, thứ tự: Dự đoán phương tiện · So sánh mô hình · Dữ liệu gốc · Làm sạch & chọn cột · Khám phá dữ liệu · Phương tiện thay thế khi cấm xe máy.
- Tab Dự đoán: form 12 ô + chọn mô hình, nút **Dự đoán** và **Xóa** (về mặc định, ẩn kết quả); kết quả giữ trong `session_state` khi đổi tab.
- Footer: dòng đậm "Kho dữ liệu và khai phá dữ liệu (CTH603) · Lớp CTHT33 · Nhóm 2", "Thành viên:" + danh sách (Lê Nguyễn Bảo Ngọc, Trần Thị Thanh Hằng); đường kẻ dọc ở giữa (không chạm mép); nguồn dữ liệu bên phải 2 hàng; không bo góc; luôn nằm đáy màn hình khi nội dung ngắn (không sinh thanh cuộn).
- Chữ chú thích xám đậm `#4A5A60`; tiêu đề mục (subheader) 1,4rem; bảng tự cao vừa số dòng (`fit_height()`); `is_dark()` luôn trả False (theme cố định sáng).
- Sửa `common.py` thì phải **tắt và chạy lại** `streamlit run` (Streamlit không nạp lại module import); sửa `app.py` chỉ cần F5.

## 1. Đã làm được

| Ngày | Nội dung |
| --- | --- |
| 31/10–01/11 | Khảo sát sơ bộ nhiều dataset (Coupon, dưới 10 feature, lương VN, dữ liệu VN khác) rồi chốt đề tài. Chi tiết ở `../w0/ai_notes/README.md`. |
| 01/11 | **Chốt đề tài:** dự đoán lựa chọn phương tiện của người đô thị bằng phân lớp; dữ liệu UTM-Hanoi 2021 (OSF, 26.106 × 56). Nhãn 4 lớp, 9 feature, cột lộ nhãn (`travtime`, tốc độ, `reason`, `freq_*`) không dùng. |
| 01/11 | Dựng demo Streamlit (`demo/`) với 6 tab, kèm thí nghiệm rò rỉ nhãn. |
| 13/11 | **Chốt bộ giải thuật:** kNN, Decision Tree, Random Forest. Bỏ Naive Bayes. |
| 13/11 | Thêm kNN vào demo: bộ tiền xử lý riêng (`make_knn_preprocessor`: thứ bậc → MinMax [0,1], định danh → one-hot), k chọn bằng CV 5 fold trên train (lưới 3–51, được k=3). |
| 13/11 | Cập nhật CLAUDE.md và memory. Tạo `w1/` và chuyển `demo/` sang đây; sửa đường dẫn, kiểm tra app chạy không lỗi bằng `AppTest`. |
| 13/11 | Trao đổi giải thích feature/nhãn/accuracy/macro-F1, chẩn đoán k của kNN và macro-F1 thấp, đính chính 8 nhãn gốc. Tóm tắt ở mục 7. |
| 14/11 | Người dùng chốt: tên đề tài có chữ "Hệ thống" ở đầu; giữ nguyên các thư mục cũ trong `w0/`; dữ liệu gốc để nguyên trong `demo/data/`; bỏ yêu cầu làm theo quy trình từng bước (phối hợp theo yêu cầu của người dùng); README gốc đã sửa trỏ tới `w1/`. Đã cập nhật tên đề tài trong README gốc, `w1/README.md`, `demo/README.md`, `demo/common.py` (`TITLE`) và CLAUDE.md. |
| 14/11 | Trao đổi về nhãn và feature (Ghi chú của AI, chưa có số đo): bản gốc có 8 nhãn, không phải 7; đề xuất thử 5 nhãn (xe máy / ô tô / xe đạp + xe điện / đi bộ / công cộng và taxi); ứng viên feature thêm để đạt khoảng 12: `type`, `status`, `own`, có thể thêm `dist_to_pub` (cần xác nhận ý nghĩa). |
| 14/11 | **So sánh 5 nhãn × 9/12/13 feature** (Ghi chú của AI; script `ai_notes/so_sanh_5nhan.py`, kết quả `ai_notes/so_sanh_5nhan_ketqua.json`). Nhãn: xe máy / ô tô / xe đạp + xe điện / đi bộ / công cộng + taxi. Cùng tập test 4.860 chuyến. Random Forest accuracy / macro-F1: 9 feature 0,810 / 0,585; 12 feature 0,840 / 0,620; 13 feature 0,853 / 0,621. CV macro-F1 (5 fold, mean ± std): 0,556 ± 0,011 → 0,592 ± 0,012 → 0,606 ± 0,012. Hai lớp nhỏ nhất vẫn khó: "Công cộng + taxi" F1 0,17–0,29, "Đi bộ" 0,39–0,49. |
| 14/11 | **Chọn k cho kNN, bộ 12 feature, 5 nhãn** (Ghi chú của AI; `ai_notes/chon_k.py`, kết quả `ai_notes/chon_k_ketqua.json`). CV lặp 5 fold × 3 lần trên tập train (19.436 dòng), k = 1–15, `uniform` và `distance`. Tốt nhất: `distance`, k=5, macro-F1 CV 0,584 ± 0,021, accuracy 0,806. Đường cong `distance` phẳng ở k=4–8 (chênh so với k=5 chỉ 0,001–0,004, nhỏ hơn độ lệch chuẩn ghép cặp 0,005–0,008). `uniform` đỉnh ở k=3 (0,583) nhưng dao động mạnh theo k (k=2: 0,557; k=4: 0,572). Khi cố định k=5 cho cả 3 bộ feature (uniform): macro-F1 test 0,573 / 0,604 / 0,610 cho 9 / 12 / 13 feature. |
| 14/11 | **Cập nhật demo theo cấu hình người dùng chốt:** 5 nhãn, 12 feature, kNN `weights="distance"` k=5 (Decision Tree và Random Forest dùng chung bộ 12 feature, tham số như cũ). Sửa `common.py` (`LABELS`, `GROUP`, `FEATURES`, `KNN_K`, `KNN_WEIGHTS`, nhãn tiếng Việt cho 3 cột nhà ở), `train.py` (kNN cố định k=5, vẫn đo CV vài k để ghi báo cáo), `app.py` (form 12 ô, 5 màu, ma trận nhầm lẫn 5×5). Chạy lại `train.py` trong sandbox của AI và ghi `artifacts/` về máy. **Chưa mở được app bằng `streamlit`/`AppTest`** (sandbox không có streamlit); mới kiểm tra bằng cách nạp mô hình, dự đoán thử với giá trị mặc định của form và đối chiếu khóa trong `report.json` với những gì `app.py` đọc. |
| 14/11 | **Web thành demo chính thức** theo yêu cầu người dùng: bỏ dòng "Demo của AI"; bố cục single page (6 tab cũ thành 6 mục nối tiếp); header cố định chứa tên đề tài và menu 6 mục (bấm để cuộn tới mục); footer ghi môn CTH603, lớp CTHT33, Nhóm 2, thành viên và nguồn dữ liệu; theme xanh lục đậm (teal, `#0F766E`) trong `.streamlit/config.toml` ở thư mục gốc. Nội dung các mục giữ nguyên. Đã chạy thử toàn bộ `app.py` với streamlit giả lập (không lỗi Python); **chưa xem giao diện thật** vì sandbox của AI không có streamlit. Người dùng muốn giữ đủ 6 mục và sẽ trao đổi thêm các chức năng. Bản nháp báo cáo (mục độ đo, vì sao không dùng RMSE/MAE) ở `bao_cao_nhap.md`. |
| 14/11 | **Chỉnh giao diện lần 2** theo ảnh chụp và yêu cầu của người dùng: bỏ single page, quay lại dạng tab; thanh tiêu đề tối cố định, thanh tab nền sáng dính bên dưới, tab đang chọn nền teal chữ trắng; bỏ đánh số; đổi tên tab 6 thành "Phương tiện thay thế khi cấm xe máy"; thứ tự tab mới: Dự đoán phương tiện · So sánh mô hình · Dữ liệu gốc · Làm sạch & chọn cột · Khám phá dữ liệu · Phương tiện thay thế khi cấm xe máy; footer gọn (dòng in đậm môn · lớp · nhóm, danh sách thành viên, nguồn dữ liệu bên phải). Chạy thử bằng streamlit giả lập không lỗi; chưa xem giao diện thật. |
| 15/11 | **Viết báo cáo `baocao/baocao-dwdm.docx`** (28 trang) theo khung của `baocao-sample.docx`: 2 bìa (tên đề tài mới), mục lục có số trang và liên kết, danh sách 13 bảng / 6 hình, từ viết tắt, Mở đầu, Chương 1–4, Kết luận, 5 tài liệu tham khảo. Số liệu lấy từ `demo/artifacts/report.json` (lần chạy 14/11) và `ai_notes/*.json`; 5 hình vẽ bằng matplotlib, Hình 4.2 là ảnh chụp tab Dự đoán của người dùng; Hình 4.3, 4.4 là khung chờ chèn ảnh chụp. Nguồn dựng ở `baocao/_nguon/`. Người dùng đã xóa dòng ghi chú đầu mục lục trước khi AI ghi bản này (bản mới không còn dòng đó). |

**Số đo của demo (tập test 4.860 chuyến, 14/11, 5 nhãn, 12 feature):**

| Mô hình | CV macro-F1 (train) | Accuracy | Macro-F1 |
| --- | --- | --- | --- |
| Random Forest | 0,591 | 0,838 | 0,612 |
| kNN (`distance`, k=5) | 0,582 | 0,804 | 0,594 |
| Decision Tree | 0,567 | 0,801 | 0,590 |
| Luôn đoán xe máy | — | 0,570 | 0,145 |

Số đo cũ ngày 13/11 (4 nhãn, 9 feature): Random Forest 0,805 / 0,659; kNN k=3 0,772 / 0,653; Decision Tree 0,778 / 0,630. Không so trực tiếp được vì khác số nhãn (macro-F1 trung bình trên số lớp khác nhau).
Ghi chú: Random Forest ở `ai_notes/so_sanh_5nhan.py` cho 0,840 / 0,620 với cùng cấu hình; chênh 0,008 là do thứ tự cột sau mã hóa khác nhau, cho thấy mức nhiễu giữa các lần chạy. Với kNN, `uniform` k=5 trên tập test cho 0,604, hơn `distance` k=5 (0,594); chênh lệch nằm trong nhiễu, còn CV lặp trên train ủng hộ `distance` (xem dòng "Chọn k" ở trên).

## 2. Đang vướng / cần lưu ý

- **Báo cáo còn thiếu (người dùng làm):** chèn ảnh chụp Hình 4.3 (tab So sánh mô hình) và Hình 4.4 (tab Khám phá dữ liệu), hiện là khung viền đứt; Hình 4.2 là ảnh chụp tab Dự đoán trước khi có nút Xóa, nên chụp lại; điền tên giảng viên hướng dẫn trên bìa; đọc lại văn phong; cập nhật mục lục trong Word (chuột phải → Update Field → Update entire table) vì số trang đo bằng LibreOffice.
- **Hai lớp nhỏ dự đoán kém:** "Công cộng + taxi" F1 ~0,20–0,23, "Đi bộ" ~0,40–0,44 (bản 14/11). Chưa thử xử lý mất cân bằng (resampling, ngưỡng) trên bộ 5 nhãn; `class_weight="balanced"` chỉ thử trên bản 4 nhãn cũ (không cải thiện macro-F1).
- **Nhãn tiếng Việt của 3 cột nhà ở là diễn giải tạm** (`HOUSE_TYPE`, `STATUS`, `TENURE` trong `common.py`), cần đối chiếu từ điển dữ liệu UTM-Hanoi. `so_huu_nha` đứng thứ 3 về độ quan trọng (0,112). Báo cáo đã ghi chú điều này ở mục 2.6.
- **Tham số Decision Tree / Random Forest chưa tinh chỉnh**; chênh lệch giữa 3 mô hình không lớn so với độ dao động giữa các lần chia (RF 0,612 ở demo so với 0,620 ở `ai_notes`, do thứ tự cột sau mã hóa).
- **kNN có thể hòa phiếu** (ví dụ kịch bản 2 trong báo cáo: Xe đạp 40% = Đi bộ 40%); web hiện lấy lớp xuất hiện trước. Chưa xử lý riêng.
- **Màu thứ 5 (tím `#7a5cc7`) của biểu đồ chưa kiểm tra mù màu.**
- **Môi trường của AI** không có streamlit, altair và mạng: AI chỉ kiểm tra `app.py` bằng bản giả lập; giao diện thật phải nhờ người dùng chạy và gửi ảnh chụp. Trình duyệt tích hợp không mở được `localhost:8501` (thử 14/11).
- **Bản gốc `hn_survey_26k.csv`** để nguyên trong `demo/data/`; người dùng sẽ yêu cầu khi nào cần chuyển.
- **Đính chính (13/11):** bản gốc OSF có **8 giá trị** ở cột nhãn `vehic` (7 là bản Kaggle). Một số ghi chú cũ trong `w0/ai_notes/` vẫn ghi "7 lớp", chưa sửa.

## 3. Quyết định của người dùng

**Đã chốt (14/11/2026)**
- Tên đề tài: **"Hệ thống dự đoán lựa chọn phương tiện di chuyển của người dân đô thị dựa vào kỹ thuật phân lớp"** (có chữ "Hệ thống" ở đầu và "người dân đô thị"; người dùng xác nhận nguyên văn 14/11).
- Các thư mục cũ trong `w0/` (`demo_luong`, `demo_coupon`, `ai_notes`): giữ lại, không xóa.
- Vị trí dữ liệu gốc: để nguyên trong `demo/data/`.
- Cách làm việc: không bắt buộc quy trình từng bước; AI phối hợp theo yêu cầu của người dùng.

**Đã chốt thêm (14/11/2026, sau khi xem số đo của AI)**
- **Nhãn: 5 lớp** (xe máy / ô tô / xe đạp + xe điện / đi bộ / công cộng + taxi). Không dùng 4 nhãn nữa.
- **Feature: 12** = 9 feature cũ + loại nhà (`type`), tình trạng cư trú (`status`), hình thức sở hữu nhà (`own`). Cả 3 giải thuật dùng chung bộ này; form web có 12 ô. Yêu cầu "dưới 10 feature" trước đây không còn áp dụng; cần ghi lý do trong báo cáo (thêm 3 feature nhà ở làm macro-F1 tăng từ khoảng 0,57–0,59 lên 0,60–0,62).
- **kNN: `weights="distance"`, k=5.**
- Phần trình bày quá trình tìm hiểu từng giải thuật sẽ kèm số đo thử với 9 / 12 / 13 feature và nhiều k (3, 5, 11…): người dùng sẽ yêu cầu thêm sau. Số đo hiện có nằm ở `ai_notes/so_sanh_5nhan_ketqua.json` và `ai_notes/chon_k_ketqua.json`.

## 4. Công việc tiếp theo (người dùng quyết định làm gì trước)

1. **Báo cáo:** người dùng đọc lại `baocao/baocao-dwdm.docx`, chèn ảnh chụp, nêu chỗ cần sửa; AI sửa đúng đoạn được yêu cầu (không dựng lại cả file, xem mục 8). Người dùng đã nói sẽ yêu cầu thêm phần trình bày quá trình tìm hiểu từng giải thuật với số đo 9/12/13 thuộc tính và nhiều k (3, 5, 11…): hiện báo cáo đã có Bảng 3.2 và Hình 3.1, có thể cần mở rộng.
2. **Web:** người dùng đang duyệt và sẽ trao đổi thêm các chức năng cần thiết cho "hệ thống" (không muốn web quá đơn giản). Mỗi thay đổi giao diện ảnh hưởng mục 4.3 của báo cáo.
3. **Cải thiện mô hình (tùy chọn):** xử lý mất cân bằng cho 2 lớp nhỏ; tinh chỉnh tham số DT/RF bằng CV; nếu đổi cấu hình thì chạy lại `train.py` và cập nhật báo cáo theo bảng ở mục 8.
4. **Đối chiếu từ điển dữ liệu** UTM-Hanoi cho các cột `type`, `status`, `own`, `dist_to_pub`.
5. **Slide thuyết trình** (chưa được yêu cầu): có thể cần khi nộp / báo cáo.
6. **Bài cá nhân:** chờ người dùng yêu cầu.

## 5. Chọn k cho kNN (đã làm ngày 14/11 bằng `ai_notes/chon_k.py`; danh sách dưới đây là kế hoạch gốc)

Mục tiêu: ra được một giá trị k (và cấu hình đi kèm) có căn cứ, không phụ thuộc vào nhiễu của một lần chia dữ liệu. Số đo hiện có: macro-F1 CV 5 fold, `weights="distance"`: k=3 0,627 · k=5 0,630 · k=11 0,633 · k=21 0,624; trọng số đều: k=3 0,624 · k=5 0,623 · k=11 0,615 · k=21 0,580.

1. **Đo độ dao động:** lấy trung bình và độ lệch chuẩn của macro-F1 trên các fold cho từng k; nếu khoảng "trung bình ± độ lệch chuẩn" của hai k chồng nhau thì coi như chưa phân biệt được.
2. **Lặp lại với nhiều seed:** dùng CV lặp (ví dụ `RepeatedStratifiedKFold`, 5 fold × 3–5 lần) để giảm phụ thuộc vào một cách chia.
3. **Quy tắc chọn:** thử "k nhỏ nhất (hoặc đơn giản nhất) có điểm nằm trong 1 độ lệch chuẩn của điểm cao nhất" so với "k có điểm cao nhất"; ghi rõ quy tắc dùng.
4. **So sánh `weights`:** "uniform" và "distance" cùng một lưới k; xem cấu hình nào phẳng và ổn định hơn.
5. **Mở rộng lưới k:** thêm các giá trị lẻ giữa 5 và 21 (ví dụ 7, 9, 13, 15, 17) để thấy hình dạng đường cong.
6. **Xem tác động của các điểm hòa khoảng cách:** vì có nhiều dòng trùng feature (8.534 tổ hợp / 24.296 dòng), kiểm tra kết quả khi gộp dòng trùng hoặc dùng `weights="distance"`.
7. **Đo thêm thước đo khác:** accuracy và F1 theo từng lớp (đặc biệt lớp "Khác") ở mỗi k, không chỉ macro-F1.
8. **Giữ nguyên quy tắc:** chọn k chỉ trên tập train; tập test chỉ dùng một lần ở bước đánh giá cuối.

## 6. Dữ liệu gốc: bao nhiêu cột, bao nhiêu nhãn, sau khi gộp còn bao nhiêu (13/11, Ghi chú của AI; số liệu của bản 4 nhãn / 9 feature, nay là 5 nhãn / 12 feature)

- **56 cột** gồm: 1 cột nhãn (`vehic`), 10 cột gốc dùng để tạo 9 feature, và 45 cột còn lại không dùng.
- **Nhãn gốc: 8 giá trị** (moto 14.988, car 7.019, ebike 1.493, bike 1.281, walk 545, bus 427, taxi 341, tram 12). **Sau gộp: 4 nhãn** (xe máy / ô tô / xe đạp + xe điện / khác).
- **Feature: 9** (tạo từ 10 cột gốc: age, gender, occup, purp, OD_dist, freqpweek, own_car, own_motob, own_bike + own_ebike gộp thành "số xe đạp + xe điện").
- **45 cột không dùng:**
    - 3 cột định danh/chỉ số (`rowid`, `id`, `index`);
    - 4 cột tọa độ (`origlat`, `origlon`, `destlat`, `destlon`);
    - 8 cột lộ nhãn (`travtime`, `reason`, `freq_car`, `freq_motob`, `freq_ebike`, `freq_bike`, `freq_taxi`, `freq_bus`);
    - 30 cột còn lại thuộc nhóm khảo sát chính sách và nhận thức (khả năng tiếp cận dịch vụ `*_acc`, `type`, `status`, `own`, `reas_not_*`, `dist_to_pub`, `aware_ban`, `fut_veh`, `alt_*`, `opinion_*`). Việc xét từng cột này (có biết trước khi chọn xe hay không) thuộc bước khai báo dữ liệu, chưa làm.
- Sau làm sạch (bỏ trùng, ngoại lai khoảng cách): 24.296 dòng.

## 7. Nhật ký trao đổi 13/11/2026 về cột (feature) và nhãn, để tiếp tục ở session sau

**Câu hỏi của người dùng và trả lời tóm tắt**

1. *Feature là gì, nhãn là gì, ví dụ từ dữ liệu?* Mỗi dòng là một người trả lời kèm chuyến đi chính. **Feature** = thông tin biết trước khi chọn xe (tuổi, giới tính, nghề nghiệp, mục đích, quãng đường, số chuyến/tuần, số ô tô / xe máy / xe đạp + xe điện của hộ). **Nhãn** = phương tiện của chuyến đi (cột `vehic`).
    - Ví dụ thật: Nữ, 18–25, sinh viên, đi học, dưới 1 km, hộ không có xe nào → nhãn `walk` → "Khác". Nam, 36–55, doanh nghiệp FDI, đi thăm hỏi, trên 10 km → `moto` → "Xe máy".
2. *File gốc có bao nhiêu feature và nhãn, sau gộp còn bao nhiêu?* Xem mục 6: 8 nhãn gốc → 4 nhãn; 56 cột → 1 nhãn + 9 feature (từ 10 cột gốc) + 45 cột không dùng.
3. *Vì sao gộp 4 nhãn?* Các lớp nhỏ không đủ mẫu để học và chia train/test (tram chỉ 12 dòng; taxi 341, bus 427, walk 545). Xe đạp và xe đạp điện đều là hai bánh cá nhân nhẹ nên gộp. Người dùng ưu tiên bài toán ít nhãn. **Cái giá:** nhãn "Khác" lẫn đi bộ (chuyến ngắn) với bus/taxi/tàu (chuyến dài), nên khó nhất (recall 0,24, F1 0,34 ở Random Forest).
4. *Vì sao 9 feature?* Hai ràng buộc: người dùng muốn dưới 10 feature, và phải loại cột lộ nhãn (`travtime`, `reason`, `freq_*`). Chưa có bằng chứng thực nghiệm rằng đúng 9 cột này là tập tối ưu; 30 cột về chính sách/nhận thức chưa được xét từng cột.
5. *Accuracy và macro-F1 là gì?* Accuracy = đoán đúng / tổng. Macro-F1 = trung bình F1 của từng lớp, mỗi lớp trọng số bằng nhau. Mô hình "luôn đoán xe máy" có accuracy 0,570 nhưng macro-F1 chỉ 0,182. Slide "5. Model evaluation" (slide 6, ví dụ 9.990 so với 10) nói về hạn chế của accuracy; chưa có slide nào về macro-F1; Bài 12 và 13 (WEKA) yêu cầu Accuracy và F1 nhưng trong docx mới có phần đề, chưa có phần giải.
6. *Nên chọn k bằng bao nhiêu?* Đề xuất `weights="distance"` và k=11 (CV macro-F1 0,633), nhưng chênh lệch giữa các k rất nhỏ, chưa đo độ lệch chuẩn. Việc cần làm ở mục 5.

**Số đo tham chiếu (tập train, CV 5 fold; test 4.860 chuyến)**

- 24.296 dòng sau làm sạch, 8.534 tổ hợp feature khác nhau.
- Random Forest theo lớp (test): xe máy recall 0,907 · ô tô 0,776 · xe đạp/xe điện 0,595 · Khác 0,236.
- Random Forest `class_weight="balanced"`: recall "Khác" 0,665 nhưng precision 0,300, accuracy 0,739 (giảm từ 0,805), macro-F1 0,652 (không cải thiện).
- Script chẩn đoán: `chan_doan.py` nằm trong scratchpad của session (có thể đã mất); chạy lại bằng các bước ở mục 5 nếu cần.

**Ghi chú đính chính:** lúc đầu AI nói "7 lớp"; đúng là 8 giá trị trong bản gốc OSF (7 là của bản Kaggle). Script `ai_notes/utm_hanoi_khao_sat.py` và ghi chú cũ trong `w0/ai_notes/README.md` vẫn còn chữ "7 lớp" (do khảo sát trên bản Kaggle), chưa sửa.

**Quy ước làm việc đã chốt trong phiên này:** người dùng tự quyết định trực tiếp; không hỏi hay theo dõi việc "nhóm đã đồng ý chưa".

**Để tiếp tục:** người dùng sẽ tự làm mục 5 (chọn k). Phương án đang chờ người dùng quyết (mục 3): giữ 4 nhãn, hay tách đi bộ ra khỏi "Khác", hay bỏ "Khác" (3 nhãn); giữ 9 feature hay thêm/bớt. Tài liệu w1 trên claude.ai (https://claude.ai/artifact/QMko3XdiCM5MKHniSdiyPS) **chưa** cập nhật theo các nội dung từ mục 5 đến 7 này và vẫn còn ô tick "Cần nhóm xác nhận" cũ.

> Quy ước: việc AI tự đo hoặc tự đề xuất luôn gắn nhãn "Ghi chú của AI" và tách khỏi phần chính thức của nhóm.

## 8. Báo cáo `baocao/baocao-dwdm.docx`: cập nhật khi source thay đổi

Báo cáo chứa số liệu **gõ cứng** của lần chạy 14/11/2026 (5 nhãn, 12 thuộc tính, kNN `distance` k=5; Random Forest accuracy 0,838 / macro-F1 0,612). Mỗi khi source hoặc kết quả thay đổi, phải cập nhật các mục tương ứng trong báo cáo, rồi cập nhật mục lục (chuột phải → Update Field → Update entire table) và danh sách bảng / hình.

- Người dùng có thể đã sửa báo cáo bằng Word: **không dựng lại toàn bộ file** bằng `_nguon/make2.py` (sẽ ghi đè chỉnh sửa). Sửa trực tiếp các đoạn bị ảnh hưởng trong file Word (giải nén, sửa `word/document.xml`, sao lưu trước), hoặc báo cho người dùng danh sách chỗ cần sửa.
- Sau khi sửa, ghi vào mục 1 của file này: đã cập nhật những mục nào của báo cáo và theo số liệu lần chạy nào.
- Còn chờ người dùng: chèn ảnh chụp cho Hình 4.3 (tab So sánh mô hình) và Hình 4.4 (tab Khám phá dữ liệu); kiểm tra tên giảng viên hướng dẫn trên bìa (đang để trống như mẫu).

| Khi thay đổi | Cập nhật trong báo cáo |
| --- | --- |
| Dữ liệu, `clean()` trong `common.py` (bước làm sạch, ngưỡng quãng đường) | Mục 2.3, 2.4 (Bảng 2.2), 2.5 (Bảng 2.3 số mẫu mỗi lớp), Hình 2.1, 2.2, mục 2.7 (số dòng train/test), Kết luận |
| Nhãn (`LABELS`, `GROUP`) | Mục 2.5 (Bảng 2.3), toàn bộ Chương 3 (Bảng 3.3–3.5), mục 4.3.1, Bảng 4.2, Mở đầu mục 3 |
| Thuộc tính (`FEATURES`, giá trị trong `OPTIONS`) | Mục 2.6 (Bảng 2.5), 2.7, mục 3.5, Hình 3.2, mục 4.3.1, Bảng 4.2 |
| Tham số mô hình (`KNN_K`, `KNN_WEIGHTS`, tham số cây/rừng trong `train.py`) | Bảng 3.1, mục 3.2–3.4, Hình 3.1 (nếu đổi lưới k), Bảng 3.3–3.6 |
| Chạy lại `train.py` (số liệu trong `artifacts/report.json` đổi) | Bảng 3.3, 3.4, 3.5, 3.6, Hình 3.2, mục 3.6–3.7, Bảng 4.2 (chạy lại các kịch bản), Kết luận mục 1 |
| `ai_notes/so_sanh_5nhan.py`, `chon_k.py` chạy lại | Bảng 3.2, Hình 3.1, mục 3.2, 3.5 |
| Giao diện `app.py` (tab, nút, bố cục) | Mục 4.1, 4.3 (Hình 4.2–4.4: chụp lại ảnh), 4.4 |
| Thư viện / phiên bản (`requirements.txt`, `.venv`) | Mục 3.1, Bảng 4.1 |
| Thông tin nhóm (`COURSE`, `CLASS_NAME`, `GROUP_NAME`, `MEMBERS` trong `common.py`) | Hai trang bìa |

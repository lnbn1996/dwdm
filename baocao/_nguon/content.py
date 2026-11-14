# -*- coding: utf-8 -*-
"""Nội dung báo cáo. Số liệu lấy từ artifacts/report.json (lần chạy 14/11/2026: 5 nhãn, 12 thuộc tính,
kNN distance k=5) và ai_notes/*.json. Khi huấn luyện lại hoặc đổi cấu hình, phải sửa các con số ở đây."""
import os
FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig")
SHOT_PRED = os.path.join(FIG, "h4_2_tab_du_doan.png")  # ảnh chụp tab Dự đoán (14/11/2026)

ABBR = [("CV", "Cross-Validation – kiểm định chéo"), ("DT", "Decision Tree – cây quyết định"),
        ("EDA", "Exploratory Data Analysis – khám phá dữ liệu"), ("F1", "Trung bình điều hòa của Precision và Recall"),
        ("FN / FP", "False Negative / False Positive – âm tính giả / dương tính giả"),
        ("kNN", "k-Nearest Neighbors – k láng giềng gần nhất"), ("OSF", "Open Science Framework"),
        ("RF", "Random Forest – rừng ngẫu nhiên"), ("TP / TN", "True Positive / True Negative – dương tính thật / âm tính thật"),
        ("UTM-Hanoi", "Dự án khảo sát giao thông đô thị Hà Nội (bộ dữ liệu sử dụng)"),
        ("CC BY 4.0", "Giấy phép Creative Commons Attribution 4.0")]

B = []
def h1(t): B.append(("h1", t))
def h2(t): B.append(("h2", t))
def h3(t): B.append(("h3", t))
def p(t): B.append(("p", t))
def ul(*items): B.append(("ul", list(items)))
def eq(t): B.append(("eq", t))
def table(cap, widths, head, rows): B.append(("table", cap, widths, head, rows))
def fig(cap, path, cm=15.5): B.append(("fig", cap, path, cm))
def ph(cap, text): B.append(("ph", cap, text))

# =========================================================== MỞ ĐẦU
h1("MỞ ĐẦU")
h2("1. Lý do chọn đề tài")
p("Giao thông ở các đô thị lớn của Việt Nam phụ thuộc rất nhiều vào phương tiện cá nhân, đặc biệt là xe máy. Trong dữ liệu khảo sát người dân nội đô Hà Nội năm 2021 mà nhóm sử dụng, xe máy chiếm 57,4% số chuyến đi chính, ô tô chiếm 26,9%, trong khi xe buýt, taxi và tàu điện cộng lại chưa tới 3%. Cơ cấu này gây áp lực lên hạ tầng, ùn tắc và ô nhiễm, và là lý do các chính sách như hạn chế xe máy trong nội đô được đặt ra.")
p("Để xây dựng chính sách và quy hoạch giao thông phù hợp, cần hiểu người dân lựa chọn phương tiện dựa trên những yếu tố nào: đặc điểm cá nhân, đặc điểm hộ gia đình, mục đích và quãng đường chuyến đi. Bài toán dự đoán phương tiện từ các yếu tố này là một bài toán phân lớp điển hình trong khai phá dữ liệu, phù hợp để áp dụng các kỹ thuật được học trong môn Kho dữ liệu và khai phá dữ liệu trên một bộ dữ liệu thực tế, có nguồn gốc rõ ràng và gần gũi với bối cảnh Việt Nam.")
p("Vì vậy nhóm chọn đề tài **“Hệ thống dự đoán lựa chọn phương tiện di chuyển của người dân đô thị dựa vào kỹ thuật phân lớp”**.")
h2("2. Mục tiêu")
p("Đề tài hướng tới các mục tiêu sau, bám theo yêu cầu của bài tập nhóm:")
ul("Tìm, mô tả và xử lý một tập dữ liệu thực tế về hành vi đi lại của người dân đô thị.",
   "Huấn luyện ba mô hình phân lớp là k-Nearest Neighbors, Decision Tree và Random Forest; so sánh kết quả và lựa chọn mô hình tốt nhất.",
   "Xây dựng hệ thống web đơn giản tích hợp các mô hình: người dùng chọn thông tin đầu vào, bấm nút Dự đoán và nhận phương tiện có khả năng cao nhất kèm xác suất của từng phương tiện.")
h2("3. Đối tượng và phạm vi")
ul("**Đối tượng nghiên cứu:** lựa chọn phương tiện cho chuyến đi chính của người dân đô thị, phân thành 5 nhóm: xe máy, ô tô, xe đạp / xe đạp điện, đi bộ và phương tiện công cộng + taxi.",
   "**Phạm vi dữ liệu:** khảo sát người dân Hà Nội năm 2021 thuộc dự án UTM-Hanoi, với mẫu lấy ở 4 quận trung tâm Hoàn Kiếm, Ba Đình, Hai Bà Trưng và Đống Đa.",
   "**Giới hạn:** kết quả mô hình phản ánh bối cảnh nội đô Hà Nội tại thời điểm khảo sát. Muốn áp dụng cho đô thị khác, có thể giữ nguyên quy trình nhưng cần huấn luyện lại trên dữ liệu địa phương.")
h2("4. Phương pháp thực hiện")
p("Nhóm thực hiện theo quy trình khai phá dữ liệu: khai báo và mô tả dữ liệu, khám phá dữ liệu (EDA), làm sạch, tiền xử lý và lựa chọn thuộc tính, huấn luyện mô hình, đánh giá và so sánh, cuối cùng tích hợp mô hình vào hệ thống web. Tham số mô hình được chọn bằng kiểm định chéo chỉ trên tập huấn luyện; tập kiểm tra chỉ dùng một lần để báo cáo kết quả cuối cùng. Toàn bộ chương trình được viết bằng Python với các thư viện pandas, scikit-learn và Streamlit.")
h2("5. Bố cục báo cáo")
p("Ngoài phần Mở đầu, Kết luận và Tài liệu tham khảo, báo cáo gồm 4 chương:")
ul("**Chương 1 – Cơ sở lý thuyết:** bài toán phân lớp, quy trình khai phá dữ liệu, ba giải thuật sử dụng, các độ đo đánh giá và kiểm định chéo.",
   "**Chương 2 – Dữ liệu và tiền xử lý:** nguồn dữ liệu, mô tả, khám phá, làm sạch, xác định nhãn, lựa chọn thuộc tính và chuẩn bị dữ liệu.",
   "**Chương 3 – Xây dựng và đánh giá mô hình:** thiết lập thực nghiệm, chọn tham số, so sánh các mô hình và phân tích kết quả.",
   "**Chương 4 – Xây dựng hệ thống web dự đoán:** kiến trúc, công nghệ, chức năng, hướng dẫn sử dụng và kết quả chạy thử.")

# =========================================================== CHƯƠNG 1
h1("CHƯƠNG 1: CƠ SỞ LÝ THUYẾT")
h2("1.1. Bài toán phân lớp trong khai phá dữ liệu")
p("Phân lớp (classification) là bài toán học một hàm ánh xạ từ tập thuộc tính x của một đối tượng sang một nhãn lớp y thuộc một tập hữu hạn các lớp đã biết trước [3]. Dữ liệu được chia thành tập huấn luyện, dùng để xây dựng mô hình, và tập kiểm tra, dùng để ước lượng khả năng dự đoán của mô hình trên dữ liệu chưa thấy. Mỗi bản ghi gồm các thuộc tính (feature) và một thuộc tính đặc biệt là nhãn (label).")
p("Trong đề tài này, mỗi bản ghi là một người trả lời khảo sát cùng chuyến đi chính của họ. Thuộc tính là những thông tin biết được trước khi chọn phương tiện như tuổi, nghề nghiệp, mục đích, quãng đường, số xe của hộ; nhãn là phương tiện của chuyến đi. Đầu ra là một nhãn rời rạc chứ không phải một con số, nên đây là bài toán phân lớp, khác với bài toán hồi quy hay dự báo (ví dụ dự báo doanh số) và khác với bài toán dự đoán điểm đánh giá trong hệ gợi ý.")
h2("1.2. Quy trình khai phá dữ liệu")
p("Khai phá dữ liệu là một bước trong quá trình phát hiện tri thức từ dữ liệu, gồm các giai đoạn chính: thu thập và hiểu dữ liệu, tiền xử lý (làm sạch, chọn và biến đổi thuộc tính), khai phá (áp dụng giải thuật), đánh giá và diễn giải kết quả, rồi đưa tri thức vào sử dụng [3]. Báo cáo được tổ chức theo đúng trình tự này: Chương 2 ứng với hiểu dữ liệu và tiền xử lý, Chương 3 ứng với khai phá và đánh giá, Chương 4 ứng với triển khai mô hình thành hệ thống cho người dùng.")
h2("1.3. Các giải thuật phân lớp sử dụng")
h3("1.3.1. k-Nearest Neighbors (kNN)")
p("kNN là phương pháp học dựa trên thể hiện (instance-based): mô hình không xây dựng hàm tường minh mà lưu lại toàn bộ tập huấn luyện. Khi cần phân lớp một đối tượng mới, giải thuật tìm k đối tượng gần nhất trong tập huấn luyện theo một độ đo khoảng cách, thường là khoảng cách Euclid, rồi gán nhãn theo đa số phiếu của k láng giềng đó:")
eq("d(x, z) = √( Σᵢ (xᵢ − zᵢ)² )")
p("Giá trị k quyết định độ mượt của ranh giới phân lớp: k nhỏ dễ bị ảnh hưởng bởi nhiễu, k lớn làm mờ các lớp nhỏ. Có hai cách bỏ phiếu: trọng số đều (uniform), mỗi láng giềng một phiếu, và trọng số theo khoảng cách (distance), láng giềng gần hơn có trọng số 1/d lớn hơn. Vì dựa trên khoảng cách nên kNN nhạy với thang đo: thuộc tính có miền giá trị lớn sẽ lấn át thuộc tính khác, do đó dữ liệu cần được chuẩn hóa về cùng thang đo trước khi dùng.")
h3("1.3.2. Cây quyết định (Decision Tree)")
p("Cây quyết định phân lớp bằng một chuỗi câu hỏi trên các thuộc tính, tổ chức theo cấu trúc cây: mỗi nút trong là một phép kiểm tra trên thuộc tính, mỗi nhánh là một kết quả của phép kiểm tra, mỗi nút lá mang một nhãn lớp. Cây được xây dựng từ trên xuống, tại mỗi nút chọn phép tách làm giảm độ hỗn tạp (impurity) nhiều nhất. Hai độ đo hỗn tạp thường dùng là Gini và Entropy, với p(i|t) là tỉ lệ mẫu thuộc lớp i tại nút t:")
eq("Gini(t) = 1 − Σᵢ p(i|t)²        Entropy(t) = − Σᵢ p(i|t) · log₂ p(i|t)")
p("Cây phát triển hết cỡ dễ bị quá khớp (overfitting) với tập huấn luyện. Để hạn chế, có thể giới hạn độ sâu tối đa (max_depth) và số mẫu tối thiểu ở mỗi lá (min_samples_leaf). Ưu điểm lớn của cây quyết định là dễ diễn giải: có thể đọc mô hình thành các luật “nếu … thì …”.")
h3("1.3.3. Rừng ngẫu nhiên (Random Forest)")
p("Random Forest là phương pháp kết hợp (ensemble) gồm nhiều cây quyết định. Mỗi cây được huấn luyện trên một mẫu bootstrap (lấy mẫu có hoàn lại từ tập huấn luyện), và tại mỗi nút chỉ xét một tập con ngẫu nhiên các thuộc tính khi chọn phép tách. Hai nguồn ngẫu nhiên này làm các cây khác nhau, nên khi kết hợp dự đoán của nhiều cây (bỏ phiếu hoặc lấy trung bình xác suất), phương sai giảm và mô hình ít quá khớp hơn một cây đơn lẻ. Random Forest còn cho biết độ quan trọng của từng thuộc tính, tính bằng mức giảm độ hỗn tạp trung bình mà thuộc tính đó mang lại trên các cây.")
h2("1.4. Các độ đo đánh giá mô hình phân lớp")
p("**Ma trận nhầm lẫn** là bảng đếm số mẫu theo cặp (lớp thực tế, lớp dự đoán). Với một lớp đang xét, TP là số mẫu của lớp được đoán đúng, FP là số mẫu lớp khác bị đoán nhầm thành lớp này, FN là số mẫu của lớp bị đoán thành lớp khác. Từ đó định nghĩa:")
eq("Accuracy = số mẫu đoán đúng / tổng số mẫu")
eq("Precision = TP / (TP + FP)        Recall = TP / (TP + FN)")
eq("F1 = 2 · Precision · Recall / (Precision + Recall)")
eq("macro-F1 = (1/K) · Σₖ F1ₖ   (K là số lớp)")
p("Accuracy dễ hiểu nhưng có hạn chế lớn khi dữ liệu mất cân bằng: trong ví dụ của bài giảng, với 9.990 mẫu lớp 0 và 10 mẫu lớp 1, một mô hình luôn đoán lớp 0 vẫn đạt accuracy 99,9% dù không nhận ra mẫu nào của lớp 1 [5]. Dữ liệu của đề tài cũng mất cân bằng mạnh (xe máy chiếm 57% số chuyến), nên nhóm dùng thêm **macro-F1**: mỗi lớp có trọng số bằng nhau, lớp nhỏ bị đoán sai sẽ kéo điểm xuống rõ rệt. Macro-F1 được dùng làm tiêu chí chính để chọn tham số và chọn mô hình.")
p("**Vì sao không dùng RMSE và MAE.** RMSE và MAE đo độ lệch giữa giá trị dự đoán và giá trị thật của một đại lượng số, nên chỉ phù hợp khi đầu ra là một con số. Trong tài liệu môn học, chúng được dùng cho bài toán dự báo (sai số của dự báo doanh số theo thời gian) và cho hệ gợi ý khi dự đoán điểm đánh giá. Nhãn phương tiện không có thứ tự và không có khoảng cách: đoán nhầm xe máy thành ô tô hay thành đi bộ đều chỉ là một lần dự đoán sai. Nếu mã hóa nhãn thành các số 0–4 rồi tính RMSE hay MAE thì kết quả phụ thuộc vào thứ tự mã hóa tùy ý và không phản ánh chất lượng dự đoán.")
h2("1.5. Kiểm định chéo và chọn siêu tham số")
p("Siêu tham số (như k của kNN, độ sâu của cây) không học được từ dữ liệu mà phải chọn trước. Nếu chọn siêu tham số dựa trên tập kiểm tra thì kết quả báo cáo sẽ lạc quan hơn thực tế. Vì vậy nhóm dùng kiểm định chéo k-fold trên tập huấn luyện: chia tập huấn luyện thành k phần (fold), lần lượt dùng mỗi phần làm tập đánh giá và k − 1 phần còn lại để huấn luyện, rồi lấy trung bình điểm của k lần. Kiểm định chéo phân tầng (stratified) giữ tỉ lệ các lớp ở mỗi fold giống tỉ lệ chung, quan trọng khi có lớp nhỏ. Kiểm định chéo lặp (repeated) thực hiện nhiều lần với cách chia khác nhau để giảm phụ thuộc vào một lần chia ngẫu nhiên, đồng thời cho biết độ lệch chuẩn của điểm số.")
p("Nguyên tắc nhóm tuân thủ: mọi lựa chọn (tham số, mô hình) chỉ dựa trên tập huấn luyện; tập kiểm tra được giữ riêng và chỉ dùng một lần để báo cáo kết quả cuối.")

# =========================================================== CHƯƠNG 2
h1("CHƯƠNG 2: DỮ LIỆU VÀ TIỀN XỬ LÝ")
h2("2.1. Nguồn dữ liệu và giấy phép")
p("Nhóm sử dụng bộ dữ liệu khảo sát người dân Hà Nội năm 2021 thuộc dự án UTM-Hanoi, được công bố trong bài báo của Kieu và cộng sự trên tạp chí Scientific Data năm 2024 [1]. Dữ liệu do Tổng cục Thống kê thực hiện qua điện thoại; theo bài báo, mẫu được lấy ngẫu nhiên 2,5% số hộ ở 4 quận trung tâm Hoàn Kiếm, Ba Đình, Hai Bà Trưng và Đống Đa. Ngoài thông tin chuyến đi, khảo sát còn hỏi nhận thức của người dân về các chính sách giao thông, trong đó có đề xuất hạn chế xe máy nội đô.")
p("File sử dụng là hn_survey_26k.csv tải từ kho Open Science Framework (OSF) [2], phát hành theo giấy phép CC BY 4.0, cho phép sử dụng với điều kiện ghi nguồn. Nguồn được ghi trong báo cáo, ở tab Dữ liệu gốc và chân trang của hệ thống web.")
p("Nhóm dùng bản gốc trên OSF thay vì bản sao “Vehicle at Ha Noi” trên Kaggle, vì bản Kaggle thiếu 516 dòng, có thêm một dòng tổng ở cuối file, và cột OD_dist_km bị nhân nhầm hệ số 1,609 (đổi dặm sang km) trong khi cột OD_dist của bản gốc vốn đã là km.")
h2("2.2. Mô tả dữ liệu")
p("Dữ liệu gốc gồm **26.106 dòng × 56 cột**; mỗi dòng là một người trả lời cùng chuyến đi chính của họ. Nhóm phân 56 cột thành các nhóm theo vai trò trong bài toán như Bảng 2.1.")
table("Bảng 2.1: Các nhóm cột trong dữ liệu gốc", [2600, 900, 5572], ["Nhóm cột", "Số cột", "Các cột"], [
    ["Định danh, chỉ số", "3", "rowid, id, index"],
    ["Tọa độ điểm đi, điểm đến", "4", "origlat, origlon, destlat, destlon"],
    ["Nhãn (phương tiện)", "1", "vehic"],
    ["Dùng tạo thuộc tính", "13", "age, gender, occup, purp, OD_dist, freqpweek, own_car, own_motob, own_bike, own_ebike, type, status, own"],
    ["Lộ nhãn (không dùng)", "8", "travtime, reason, freq_car, freq_motob, freq_ebike, freq_bike, freq_taxi, freq_bus"],
    ["Khảo sát chính sách, nhận thức", "27", "school_acc, market_acc, hosp_acc, bank_acc, leis_acc, reas_not_* (4 cột), dist_to_pub, aware_ban, fut_veh, alt_veh, alt_* (7 cột), opinion_* (7 cột)"],
])
p("Cột nhãn vehic có 8 giá trị: moto (xe máy), car (ô tô), ebike (xe đạp điện), bike (xe đạp), walk (đi bộ), bus (xe buýt), taxi và tram (tàu điện). Các thuộc tính đầu vào chủ yếu là biến phân loại đã được chia nhóm sẵn trong khảo sát (ví dụ tuổi theo nhóm 18_25, 26_35…; số chuyến mỗi tuần theo khoảng 1_3, 4_7…), riêng OD_dist là quãng đường đường chim bay tính bằng km.")
h2("2.3. Khám phá dữ liệu (EDA)")
p("**Phân bố nhãn.** Hình 2.1 cho thấy dữ liệu mất cân bằng mạnh: xe máy chiếm 57,4% và ô tô 26,9%, trong khi đi bộ, xe buýt, taxi chỉ 1–2% mỗi loại và tàu điện chỉ có 12 chuyến.")
fig("Hình 2.1: Phân bố phương tiện trong dữ liệu gốc (26.106 chuyến)", f"{FIG}/h2_1.png")
p("**Giá trị thiếu.** Chỉ 11 cột có giá trị thiếu. Sáu cột freq_* thiếu 44–91% vì chỉ có giá trị khi người trả lời có dùng loại xe đó; năm cột *_acc thiếu khoảng 50% vì không phải ai cũng được hỏi. Cả hai nhóm này đều không được dùng làm thuộc tính, nên các thuộc tính sử dụng không có giá trị thiếu.")
p("**Dòng trùng và ngoại lai.** Có 811 dòng giống hệt nhau ở mọi câu trả lời, chỉ khác mã người trả lời. Về quãng đường, 913 chuyến có OD_dist dưới 0,1 km (điểm đi gần như trùng điểm đến) và 106 chuyến trên 50 km (vượt phạm vi thành phố). Thời gian chuyến đi lớn nhất lên tới 5.432 phút, một giá trị bất thường; tuy nhiên cột thời gian không được dùng làm thuộc tính (xem mục 2.6).")
p("**Quan hệ giữa thuộc tính và phương tiện.** Hình 2.2 minh họa tỉ lệ phương tiện theo quãng đường sau khi làm sạch. Đi bộ chỉ xuất hiện đáng kể ở chuyến dưới 1 km (10,3%) và gần như biến mất từ 1 km trở lên; xe đạp / xe điện giảm dần theo quãng đường (21,9% ở nhóm dưới 1 km, 1,2% ở nhóm trên 10 km); ô tô tăng lên ở các chuyến 5–10 km (37,7%). Quãng đường trung vị của chuyến đi ô tô là 4,6 km, xe máy 3,7 km, trong khi đi bộ chỉ 0,5 km. Số ô tô của hộ cũng là yếu tố rõ rệt: ở hộ không có ô tô, chỉ 1,4% chuyến đi bằng ô tô; ở hộ có 2 ô tô, tỉ lệ này là 54,8%. Theo mục đích, chuyến đi làm chủ yếu bằng xe máy (69,1%), còn chuyến đi mua sắm và thăm hỏi dùng ô tô nhiều hơn xe máy.")
fig("Hình 2.2: Tỉ lệ phương tiện theo nhóm quãng đường (sau làm sạch)", f"{FIG}/h2_2.png")
h2("2.4. Làm sạch dữ liệu")
p("Dựa trên kết quả EDA, nhóm thực hiện hai bước làm sạch như Bảng 2.2. Sau làm sạch còn **24.296 chuyến đi**.")
table("Bảng 2.2: Các bước làm sạch dữ liệu", [2600, 4272, 1100, 1100], ["Bước", "Chi tiết", "Trước", "Sau"], [
    ["Bỏ dòng trùng", "811 dòng giống hệt nhau ở mọi câu trả lời (chỉ khác mã người trả lời)", "26.106", "25.295"],
    ["Bỏ quãng đường bất thường", "OD_dist dưới 0,1 km hoặc trên 50 km (999 dòng sau khi đã bỏ trùng)", "25.295", "24.296"],
])
h2("2.5. Xác định nhãn")
p("Giữ nguyên 8 nhãn gốc là không khả thi: tàu điện chỉ có 12 dòng, không đủ để học và để chia tập huấn luyện / kiểm tra; taxi, xe buýt, đi bộ cũng chỉ vài trăm dòng mỗi loại. Nhóm gộp 8 nhãn thành 5 lớp theo tính chất phương tiện (Bảng 2.3): xe đạp và xe đạp điện đều là xe hai bánh cá nhân hạng nhẹ; xe buýt, taxi và tàu điện là các phương tiện người đi không tự lái xe của mình. Đi bộ được giữ thành lớp riêng vì có đặc điểm rất khác (gần như chỉ xuất hiện ở chuyến dưới 1 km); nếu gộp đi bộ chung với xe buýt, taxi thì lớp gộp sẽ lẫn chuyến rất ngắn với chuyến dài và khó dự đoán.")
table("Bảng 2.3: Gộp 8 nhãn gốc thành 5 lớp", [2900, 3772, 2400], ["Lớp", "Nhãn gốc", "Số chuyến sau làm sạch"], [
    ["Xe máy", "moto", "13.856 (57,0%)"],
    ["Ô tô", "car", "6.636 (27,3%)"],
    ["Xe đạp / xe điện", "bike, ebike", "2.596 (10,7%)"],
    ["Đi bộ", "walk", "473 (1,9%)"],
    ["Công cộng + taxi", "bus, taxi, tram", "735 (3,0%)"],
])
h2("2.6. Lựa chọn thuộc tính")
p("**Nguyên tắc.** Thuộc tính phải là thông tin biết được trước khi người đi chọn phương tiện, vì hệ thống dùng chúng để dự đoán. Theo nguyên tắc này, các cột lộ nhãn bị loại (Bảng 2.4): chúng chỉ biết được sau khi đã chọn phương tiện, hoặc gần như nói thẳng phương tiện. Các cột thuộc phần khảo sát chính sách (reas_not_*, alt_*, aware_ban, fut_veh, opinion_*) là câu hỏi về tình huống giả định hoặc ý kiến, không thuộc bài toán; các cột *_acc thiếu khoảng một nửa số dòng; tọa độ không nhập được một cách tự nhiên trên form.")
table("Bảng 2.4: Các cột lộ nhãn bị loại", [3300, 5772], ["Cột", "Lý do loại"], [
    ["travtime (và tốc độ suy ra)", "Thời gian chuyến đi phụ thuộc vào phương tiện đã chọn"],
    ["reason", "Lý do chọn phương tiện hiện tại, được hỏi sau khi đã chọn"],
    ["freq_car, freq_motob, freq_ebike, freq_bike, freq_taxi, freq_bus", "Tần suất dùng từng loại xe, gần như cho biết phương tiện của chuyến đi"],
])
p("**Kết quả lựa chọn.** Nhóm dùng 12 thuộc tính như Bảng 2.5, gồm 9 thuộc tính về người đi, chuyến đi và số xe của hộ, cộng thêm 3 thuộc tính về nơi ở (loại nhà, tình trạng cư trú, hình thức sở hữu nhà). Số xe đạp và xe đạp điện của hộ được gộp thành một thuộc tính, giới hạn ở mức “3+”. Quãng đường được chia thành 5 mức (dưới 1 km, 1–3 km, 3–5 km, 5–10 km, trên 10 km) để người dùng dễ chọn trên form. Lý do mở rộng từ 9 lên 12 thuộc tính được trình bày ở mục 3.5: thêm 3 thuộc tính nơi ở làm macro-F1 của cả ba mô hình tăng rõ.")
table("Bảng 2.5: 12 thuộc tính sử dụng", [3300, 2672, 1700, 1400], ["Thuộc tính", "Cột gốc", "Kiểu", "Số giá trị"], [
    ["Tuổi", "age", "Thứ bậc", "6"], ["Giới tính", "gender", "Định danh", "2"],
    ["Nghề nghiệp", "occup", "Định danh", "5"], ["Mục đích chuyến đi", "purp", "Định danh", "6"],
    ["Quãng đường", "OD_dist (km)", "Thứ bậc", "5"], ["Số chuyến mỗi tuần", "freqpweek", "Thứ bậc", "7"],
    ["Số ô tô của hộ", "own_car", "Thứ bậc", "6"], ["Số xe máy của hộ", "own_motob", "Thứ bậc", "6"],
    ["Số xe đạp + xe điện của hộ", "own_bike + own_ebike", "Thứ bậc", "4"], ["Loại nhà ở", "type", "Định danh", "6"],
    ["Tình trạng cư trú", "status", "Định danh", "3"], ["Hình thức sở hữu nhà", "own", "Định danh", "4"],
])
p("Lưu ý: tên tiếng Việt của các giá trị ở ba cột nơi ở (ví dụ “Nhà riêng (khu mới)”, “Chung cư / nhà tập thể cũ”) được nhóm diễn giải từ mã giá trị trong dữ liệu (private_new, old_building…), cần đối chiếu thêm với từ điển dữ liệu của bộ UTM-Hanoi.")
h2("2.7. Mã hóa, chuẩn hóa và chia dữ liệu")
ul("**Thuộc tính thứ bậc** (tuổi, quãng đường, số chuyến mỗi tuần, số ô tô, số xe máy, số xe đạp) được mã hóa thành số nguyên theo đúng thứ tự tự nhiên của chúng.",
   "**Thuộc tính định danh** (giới tính, nghề nghiệp, mục đích, loại nhà, tình trạng cư trú, sở hữu nhà) được mã hóa one-hot, vì các giá trị này không có thứ tự.",
   "**Riêng cho kNN**, các thuộc tính thứ bậc sau khi mã hóa được chuẩn hóa Min–Max về đoạn [0, 1] để cùng thang đo với các cột one-hot (0/1); nếu không, một thuộc tính có 7 mức như số chuyến mỗi tuần sẽ chi phối khoảng cách. Hai mô hình cây không cần chuẩn hóa.",
   "Các bước mã hóa, chuẩn hóa được đặt trong pipeline của scikit-learn nên chỉ học từ tập huấn luyện, tránh rò rỉ thông tin từ tập kiểm tra.",
   "**Chia dữ liệu:** 80% huấn luyện (19.436 dòng) và 20% kiểm tra (4.860 dòng), phân tầng theo nhãn, với hạt giống ngẫu nhiên cố định (random_state = 42) để kết quả lặp lại được.")

# =========================================================== CHƯƠNG 3
h1("CHƯƠNG 3: XÂY DỰNG VÀ ĐÁNH GIÁ MÔ HÌNH")
h2("3.1. Thiết lập thực nghiệm")
p("Chương trình được viết bằng Python 3.13 với pandas 3.1, numpy 2.5 và scikit-learn 1.9. Tham số của các mô hình được chọn bằng kiểm định chéo phân tầng 5 fold trên tập huấn luyện, tiêu chí là macro-F1. Ngoài ba mô hình, nhóm đưa thêm một mô hình cơ sở luôn đoán lớp đông nhất (xe máy) để làm mốc so sánh. Bảng 3.1 tóm tắt cấu hình cuối cùng.")
table("Bảng 3.1: Cấu hình các mô hình", [2400, 2700, 3972], ["Mô hình", "Tiền xử lý", "Tham số"], [
    ["kNN", "Mã hóa + Min–Max [0, 1] + one-hot", "k = 5, weights = distance, khoảng cách Euclid"],
    ["Decision Tree", "Mã hóa thứ bậc + one-hot", "Gini, max_depth = 10, min_samples_leaf = 20"],
    ["Random Forest", "Mã hóa thứ bậc + one-hot", "200 cây, min_samples_leaf = 5, chọn ngẫu nhiên √m thuộc tính tại mỗi nút"],
    ["Luôn đoán xe máy", "—", "Mốc so sánh"],
])
h2("3.2. Mô hình kNN")
p("Với kNN, cần chọn k và cách bỏ phiếu. Nhóm thử k từ 1 đến 15 với cả hai kiểu trọng số uniform và distance, dùng kiểm định chéo lặp 5 fold × 3 lần trên tập huấn luyện (15 lần chia) để có cả trung bình và độ lệch chuẩn. Kết quả ở Hình 3.1.")
fig("Hình 3.1: Macro-F1 kiểm định chéo của kNN theo k", f"{FIG}/h3_1.png")
p("Với trọng số distance, đường cong đạt cao nhất tại k = 5 (macro-F1 0,584 ± 0,021) và gần như phẳng trong vùng k = 4–8: chênh lệch so với k = 5 chỉ 0,001–0,004, nhỏ hơn độ lệch chuẩn của chênh lệch ghép cặp giữa các fold. Với trọng số uniform, điểm cao nhất ở k = 3 (0,583) xấp xỉ, nhưng dao động mạnh theo k (k = 2 chỉ 0,557, k = 4 là 0,572) và giảm nhanh khi k tăng (k = 15 còn 0,531). Nhóm chọn **weights = distance, k = 5** vì nằm giữa một vùng ổn định thay vì một đỉnh đơn lẻ. Dữ liệu có nhiều dòng trùng tổ hợp thuộc tính, nên nhiều láng giềng có khoảng cách bằng 0; khi đó bỏ phiếu theo khoảng cách chỉ tính các điểm trùng hoàn toàn, giúp kết quả ổn định hơn.")
h2("3.3. Mô hình Decision Tree")
p("Cây quyết định dùng độ đo Gini, giới hạn độ sâu tối đa 10 và yêu cầu mỗi lá có ít nhất 20 mẫu để tránh quá khớp với các tổ hợp hiếm. Trên tập kiểm tra, cây đạt accuracy 0,801 và macro-F1 0,590. Cây có precision cao ở các lớp nhỏ (đi bộ 0,689) nhưng recall thấp, nghĩa là khi cây đoán “đi bộ” thì thường đúng nhưng bỏ sót nhiều chuyến đi bộ.")
h2("3.4. Mô hình Random Forest")
p("Random Forest gồm 200 cây, mỗi lá ít nhất 5 mẫu. Mô hình đạt accuracy cao nhất trong ba mô hình (0,838) và macro-F1 0,612. Hình 3.2 cho thấy độ quan trọng của các thuộc tính: số ô tô của hộ quan trọng nhất (0,162), tiếp theo là mục đích chuyến đi (0,124) và hình thức sở hữu nhà (0,112); quãng đường và loại nhà ở xếp sau. Kết quả phù hợp với EDA: sở hữu ô tô gần như quyết định khả năng đi ô tô, còn quãng đường tách được đi bộ và xe đạp khỏi các phương tiện khác. Việc hai thuộc tính nơi ở nằm trong nhóm đầu cũng giải thích vì sao thêm chúng làm kết quả tăng (mục 3.5).")
fig("Hình 3.2: Độ quan trọng của thuộc tính trong Random Forest", f"{FIG}/h3_2.png")
h2("3.5. Thử nghiệm số lượng thuộc tính")
p("Ban đầu nhóm dự định dùng dưới 10 thuộc tính (9 thuộc tính về người đi, chuyến đi và số xe của hộ). Để kiểm tra xem có nên mở rộng hay không, nhóm so sánh ba bộ thuộc tính trên cùng cách chia dữ liệu: 9 thuộc tính; 12 thuộc tính (thêm loại nhà, tình trạng cư trú, sở hữu nhà); và 13 thuộc tính (tách riêng số xe đạp và số xe điện, thêm loại nhà, sở hữu nhà và khoảng cách tới điểm giao thông công cộng). Ở thử nghiệm này kNN dùng trọng số uniform với k chọn bằng kiểm định chéo cho từng bộ.")
table("Bảng 3.2: So sánh 9 / 12 / 13 thuộc tính (CV trên tập huấn luyện; Accuracy, macro-F1 trên tập kiểm tra)", [2000, 1700, 2072, 1600, 1700],
      ["Bộ thuộc tính", "Mô hình", "CV macro-F1", "Accuracy", "Macro-F1"], [
    ["9", "kNN (k = 5)", "0,553 ± 0,018", "0,770", "0,573"], ["9", "Decision Tree", "0,548 ± 0,007", "0,778", "0,562"], ["9", "Random Forest", "0,556 ± 0,011", "0,810", "0,585"],
    ["12", "kNN (k = 3)", "0,586 ± 0,017", "0,801", "0,612"], ["12", "Decision Tree", "0,567 ± 0,010", "0,801", "0,590"], ["12", "Random Forest", "0,592 ± 0,012", "0,840", "0,620"],
    ["13", "kNN (k = 3)", "0,584 ± 0,015", "0,808", "0,598"], ["13", "Decision Tree", "0,583 ± 0,010", "0,812", "0,614"], ["13", "Random Forest", "0,606 ± 0,012", "0,853", "0,621"],
])
p("Cả ba mô hình đều cải thiện rõ khi chuyển từ 9 lên 12 thuộc tính: macro-F1 kiểm định chéo của Random Forest tăng từ 0,556 lên 0,592, lớn hơn nhiều so với độ lệch chuẩn khoảng 0,012. Khi cố định k = 5 cho kNN ở cả ba bộ, macro-F1 trên tập kiểm tra lần lượt là 0,573, 0,604 và 0,610, cùng xu hướng. Bộ 13 thuộc tính chỉ nhỉnh hơn 12 ở Random Forest (0,606 so với 0,592) và tương đương ở kNN, trong khi cột khoảng cách tới điểm giao thông công cộng có giá trị lỗi (giá trị âm, tới 50 triệu) phải tự sửa và đoán đơn vị. Vì vậy nhóm chọn **12 thuộc tính**: cả ba thuộc tính thêm vào đều đầy đủ, không phải sửa dữ liệu, và dễ nhập trên form.")
h2("3.6. So sánh kết quả và lựa chọn mô hình")
p("Bảng 3.3 là kết quả cuối cùng với cấu hình đã chọn (5 lớp, 12 thuộc tính), đánh giá trên tập kiểm tra 4.860 chuyến.")
table("Bảng 3.3: Kết quả các mô hình trên tập kiểm tra", [2272, 1500, 1300, 1400, 1300, 1300],
      ["Mô hình", "CV macro-F1", "Accuracy", "Precision (macro)", "Recall (macro)", "Macro-F1"], [
    ["Random Forest", "0,591", "0,838", "0,777", "0,565", "0,612"],
    ["kNN (distance, k = 5)", "0,582", "0,804", "0,627", "0,578", "0,594"],
    ["Decision Tree", "0,567", "0,801", "0,708", "0,548", "0,590"],
    ["Luôn đoán xe máy", "—", "0,570", "0,114", "0,200", "0,145"],
])
p("Cả ba mô hình đều vượt xa mốc “luôn đoán xe máy” (accuracy 0,570 nhưng macro-F1 chỉ 0,145), cho thấy mô hình thực sự học được quan hệ giữa thuộc tính và phương tiện. **Random Forest được chọn làm mô hình tốt nhất** vì có macro-F1 kiểm định chéo trên tập huấn luyện cao nhất (0,591); trên tập kiểm tra, mô hình này cũng có accuracy, precision và macro-F1 cao nhất. kNN có recall trung bình cao nhất (0,578) do nhận ra lớp nhỏ tốt hơn, còn Decision Tree đơn giản và dễ diễn giải nhất. Trong hệ thống web, Random Forest là mô hình mặc định, người dùng vẫn có thể chọn hai mô hình còn lại để so sánh.")
h2("3.7. Phân tích kết quả")
p("**F1 theo từng lớp.** Bảng 3.4 cho thấy cả ba mô hình dự đoán tốt hai lớp lớn (xe máy, ô tô có F1 0,78–0,88) và khá ở xe đạp / xe điện (khoảng 0,66–0,69), nhưng yếu ở hai lớp nhỏ nhất: đi bộ (0,40–0,44) và công cộng + taxi (0,20–0,23).")
table("Bảng 3.4: F1 theo từng lớp trên tập kiểm tra", [2672, 1300, 1100, 1500, 1100, 1400],
      ["Mô hình", "Xe máy", "Ô tô", "Xe đạp / xe điện", "Đi bộ", "Công cộng + taxi"], [
    ["Random Forest", "0,884", "0,850", "0,693", "0,436", "0,197"],
    ["kNN", "0,858", "0,816", "0,662", "0,402", "0,234"],
    ["Decision Tree", "0,862", "0,775", "0,662", "0,443", "0,207"],
])
p("**Ma trận nhầm lẫn.** Bảng 3.5 là ma trận nhầm lẫn của Random Forest. Lỗi lớn nhất là nhầm giữa xe máy và ô tô (226 chuyến ô tô bị đoán là xe máy, 129 chuyến xe máy bị đoán là ô tô): hai lớp này có hồ sơ người đi gần nhau, nhất là ở hộ có cả ô tô và xe máy. Với lớp công cộng + taxi, chỉ 17/147 chuyến được đoán đúng (recall 0,116); phần lớn bị đoán thành xe máy (75 chuyến) hoặc xe đạp / xe điện (43 chuyến). Nguyên nhân là lớp này ít mẫu (3% dữ liệu), gồm các phương tiện có đặc điểm khác nhau (xe buýt, taxi, tàu điện), và các thuộc tính hiện có (như tuổi, số xe của hộ) không phân biệt rõ người dùng phương tiện công cộng.")
table("Bảng 3.5: Ma trận nhầm lẫn của Random Forest (hàng: thực tế, cột: dự đoán)", [2272, 1300, 1100, 1500, 1100, 1800],
      ["Thực tế \\ Dự đoán", "Xe máy", "Ô tô", "Xe đạp / xe điện", "Đi bộ", "Công cộng + taxi"], [
    ["Xe máy", "2.600", "129", "41", "1", "1"], ["Ô tô", "226", "1.093", "8", "0", "0"],
    ["Xe đạp / xe điện", "162", "15", "333", "5", "4"], ["Đi bộ", "45", "0", "17", "29", "4"],
    ["Công cộng + taxi", "75", "9", "43", "3", "17"],
])
p("Ở giai đoạn khảo sát với cấu hình 4 lớp trước đó, nhóm đã thử đặt trọng số lớp cân bằng (class_weight = balanced) cho Random Forest: recall của lớp nhỏ tăng nhưng precision giảm mạnh, accuracy giảm và macro-F1 không cải thiện, nên không áp dụng. Đây là hướng cần nghiên cứu thêm (xem phần Kết luận).")
p("**Thí nghiệm rò rỉ nhãn.** Để minh họa vì sao phải loại các cột lộ nhãn, nhóm huấn luyện lại Random Forest khi thêm từng nhóm cột này vào 12 thuộc tính (Bảng 3.6). Accuracy tăng lên 0,860–0,874, nhưng đây là kết quả “đẹp giả”: khi dự đoán cho một chuyến đi chưa diễn ra, ta chưa biết thời gian, lý do chọn hay tần suất dùng từng loại xe.")
table("Bảng 3.6: Accuracy của Random Forest khi lỡ dùng cột lộ nhãn", [6072, 3000], ["Thuộc tính sử dụng", "Accuracy (tập kiểm tra)"], [
    ["12 thuộc tính (không lộ nhãn)", "0,838"], ["+ thời gian và tốc độ chuyến đi", "0,862"],
    ["+ lý do chọn phương tiện", "0,860"], ["+ tần suất dùng từng loại xe", "0,874"],
])

# =========================================================== CHƯƠNG 4
h1("CHƯƠNG 4: XÂY DỰNG HỆ THỐNG WEB DỰ ĐOÁN")
h2("4.1. Kiến trúc hệ thống")
p("Hệ thống gồm hai phần tách biệt: phần huấn luyện chạy một lần để tạo mô hình, và phần web đọc mô hình đã huấn luyện để phục vụ người dùng (Hình 4.1). Cách tổ chức này giúp web khởi động nhanh, không phải huấn luyện lại mỗi lần mở.")
fig("Hình 4.1: Kiến trúc hệ thống", f"{FIG}/h4_1.png")
ul("**common.py:** khai báo dùng chung gồm tên đề tài, phạm vi và trích dẫn dữ liệu, bảng chuyển giá trị sang tiếng Việt, cách gộp nhãn, danh sách thuộc tính, cột lộ nhãn, hàm làm sạch clean() và hai bộ tiền xử lý (cho cây và cho kNN).",
   "**train.py:** đọc dữ liệu gốc, thống kê EDA, làm sạch, chia tập huấn luyện / kiểm tra, huấn luyện ba mô hình và mốc so sánh, đánh giá, chạy thí nghiệm rò rỉ nhãn; lưu mô hình vào artifacts/models.joblib và các số liệu vào artifacts/report.json.",
   "**app.py:** ứng dụng Streamlit đọc hai file trên để hiển thị số liệu và thực hiện dự đoán.")
h2("4.2. Công nghệ sử dụng")
table("Bảng 4.1: Công nghệ sử dụng", [2600, 1500, 4972], ["Thành phần", "Phiên bản", "Vai trò"], [
    ["Python", "3.13", "Ngôn ngữ lập trình"], ["pandas, numpy", "3.1, 2.5", "Đọc, làm sạch, biến đổi dữ liệu"],
    ["scikit-learn", "1.9", "Tiền xử lý, ba mô hình phân lớp, kiểm định chéo, độ đo"],
    ["joblib", "1.6", "Lưu và nạp mô hình đã huấn luyện"], ["Streamlit", "1.66", "Xây dựng giao diện web"],
    ["Altair", "6.3", "Vẽ biểu đồ trên web"],
])
h2("4.3. Các chức năng của hệ thống")
p("Giao diện gồm thanh tiêu đề cố định và 6 tab; tab đang chọn được làm nổi bật và nối liền với khung nội dung. Chân trang ghi thông tin môn học, lớp, nhóm, thành viên và nguồn dữ liệu theo yêu cầu của giấy phép CC BY 4.0. Các tab được sắp theo thứ tự: chức năng chính, kết quả mô hình, dữ liệu theo trình tự xử lý, và phần phân tích thêm.")
h3("4.3.1. Dự đoán phương tiện")
p("Đây là chức năng chính, đáp ứng yêu cầu “giao diện cho người dùng chọn / nhập thuộc tính đầu vào, bấm nút dự đoán để xuất kết quả”. Form gồm 12 ô chọn ứng với 12 thuộc tính và một ô chọn mô hình (mặc định Random Forest). Khi bấm **Dự đoán**, hệ thống hiển thị phương tiện có xác suất cao nhất và biểu đồ xác suất của cả 5 lớp, giúp người dùng thấy mức độ chắc chắn của mô hình. Nút **Xóa** đưa các ô về giá trị mặc định và ẩn kết quả. Kết quả được giữ lại khi chuyển sang tab khác.")
fig("Hình 4.2: Tab Dự đoán phương tiện với kết quả của mô hình Decision Tree", SHOT_PRED, 15.5)
h3("4.3.2. So sánh mô hình")
p("Tab hiển thị bảng độ đo của ba mô hình và mốc so sánh trên tập kiểm tra, mô hình được chọn và lý do, ma trận nhầm lẫn của từng mô hình, biểu đồ độ quan trọng thuộc tính của Random Forest và bảng thí nghiệm rò rỉ nhãn.")
ph("Hình 4.3: Tab So sánh mô hình", "[Chèn ảnh chụp màn hình tab So sánh mô hình]")
h3("4.3.3. Dữ liệu gốc, làm sạch và khám phá dữ liệu")
ul("**Dữ liệu gốc:** số dòng, số cột, số dòng trùng, thời gian đi lớn nhất; nguồn và trích dẫn đầy đủ; mẫu 8 dòng dữ liệu gốc; phân bố phương tiện gốc; bảng giá trị thiếu.",
   "**Làm sạch & chọn cột:** bảng các bước làm sạch với số dòng trước / sau, danh sách 12 thuộc tính được chọn và các cột lộ nhãn bị loại, thông tin chia tập huấn luyện / kiểm tra.",
   "**Khám phá dữ liệu:** người dùng chọn một thuộc tính để xem tỉ lệ 5 nhóm phương tiện theo từng giá trị của thuộc tính đó (biểu đồ cột 100% kèm bảng số liệu), cùng quãng đường trung vị theo phương tiện.")
ph("Hình 4.4: Tab Khám phá dữ liệu", "[Chèn ảnh chụp màn hình tab Khám phá dữ liệu]")
h3("4.3.4. Phương tiện thay thế khi cấm xe máy")
p("Khảo sát có hỏi người dân sẽ chuyển sang phương tiện nào nếu nội đô cấm xe máy (mỗi người được chọn nhiều phương án). Tab này mô tả câu trả lời của 13.856 người đang đi xe máy: 48,4% chọn ô tô, 41,8% xe buýt, 37,1% taxi, khoảng 29% xe đạp hoặc xe đạp điện, 27,7% tàu điện và 25,4% đi bộ. Đây là phần mô tả dữ liệu, không đưa vào mô hình, nhưng bổ sung góc nhìn về tác động của chính sách.")
h2("4.4. Hướng dẫn cài đặt và sử dụng")
p("Từ thư mục gốc của dự án, tạo môi trường và cài thư viện, huấn luyện mô hình một lần rồi chạy web:")
ul("python -m venv .venv",
   ".venv\\Scripts\\python.exe -m pip install -r requirements.txt",
   ".venv\\Scripts\\python.exe assignment\\w1\\demo\\train.py   (tạo thư mục artifacts/)",
   ".venv\\Scripts\\streamlit.exe run assignment\\w1\\demo\\app.py   (mở http://localhost:8501)")
p("Cần chạy lệnh streamlit từ thư mục gốc để ứng dụng đọc được file cấu hình giao diện .streamlit/config.toml. Trên Windows, nếu gặp lỗi khi in tiếng Việt ra màn hình, đặt biến môi trường PYTHONIOENCODING = utf-8 trước khi chạy.")
h2("4.5. Kết quả chạy thử")
p("Nhóm chạy thử bốn kịch bản nhập liệu với cả ba mô hình (Bảng 4.2).")
table("Bảng 4.2: Kết quả dự đoán với một số kịch bản", [3972, 1700, 1700, 1700], ["Kịch bản", "Random Forest", "kNN", "Decision Tree"], [
    ["1. Nam 26–35, nhà nước, đi làm 3–5 km, hộ có 1 ô tô, 2 xe máy, nhà riêng, thường trú, chủ sở hữu (giá trị mặc định)", "Xe máy (66%)", "Xe máy (60%)", "Xe máy (66%)"],
    ["2. Nữ 18–25, sinh viên, đi học dưới 1 km, hộ không có xe, chung cư, tạm trú ngắn hạn, thuê nhà", "Đi bộ (42%)", "Xe đạp / xe điện (40%) – hòa với Đi bộ (40%)", "Đi bộ (82%)"],
    ["3. Như kịch bản 1 nhưng 36–55 tuổi, doanh nghiệp FDI, 5–10 km, hộ có 2 ô tô, 1 xe máy, nhà riêng khu mới", "Ô tô (89%)", "Xe máy (59%)", "Ô tô (85%)"],
    ["4. Như kịch bản 1 nhưng dưới 18 tuổi, học sinh, đi học 1–3 km, hộ không có ô tô, 1 xe máy, 2 xe đạp", "Xe đạp / xe điện (53%)", "Xe đạp / xe điện (84%)", "Xe đạp / xe điện (73%)"],
])
p("Các dự đoán nhìn chung hợp lý và khớp với EDA: chuyến rất ngắn của sinh viên không có xe được đoán là đi bộ; người làm doanh nghiệp FDI, hộ có 2 ô tô, đi 5–10 km được đoán là ô tô; học sinh đi học gần, hộ có xe đạp được đoán là xe đạp / xe điện. Kịch bản 2 cho thấy kNN có thể hòa giữa hai lớp khi các láng giềng chia đều; khi đó hệ thống hiển thị lớp xuất hiện trước, nên người dùng cần xem cả biểu đồ xác suất. Ở kịch bản 3, kNN khác hai mô hình cây: đây là trường hợp nằm giữa hai lớp xe máy và ô tô, đúng là cặp lớp bị nhầm nhiều nhất (Bảng 3.5).")

# =========================================================== KẾT LUẬN
h1("KẾT LUẬN")
h2("1. Kết quả đạt được")
p("Nhóm đã hoàn thành các yêu cầu của bài tập nhóm. Về dữ liệu, nhóm sử dụng bộ khảo sát UTM-Hanoi 2021 có nguồn gốc rõ ràng, làm sạch từ 26.106 xuống 24.296 chuyến đi, gộp 8 phương tiện thành 5 lớp và chọn 12 thuộc tính biết trước khi chọn phương tiện, loại bỏ các cột lộ nhãn. Về mô hình, nhóm huấn luyện và so sánh kNN, Decision Tree và Random Forest; Random Forest cho kết quả tốt nhất với accuracy 0,838 và macro-F1 0,612 trên tập kiểm tra, vượt xa mốc luôn đoán xe máy (macro-F1 0,145). Tham số kNN và số lượng thuộc tính được chọn có căn cứ bằng kiểm định chéo. Về sản phẩm, nhóm xây dựng hệ thống web 6 tab cho phép dự đoán phương tiện, so sánh mô hình và khám phá dữ liệu.")
h2("2. Hạn chế")
ul("Dữ liệu chỉ thuộc 4 quận nội đô Hà Nội năm 2021, nên kết quả không đại diện cho đô thị khác hay thời điểm khác.",
   "Hai lớp nhỏ là đi bộ và công cộng + taxi dự đoán chưa tốt (F1 khoảng 0,2–0,44); lớp công cộng + taxi gộp nhiều phương tiện khác nhau.",
   "Tham số của Decision Tree và Random Forest chưa được tinh chỉnh có hệ thống; chênh lệch giữa các mô hình không lớn so với độ dao động giữa các lần chia dữ liệu.",
   "Tên tiếng Việt của một số giá trị ở ba cột nơi ở là diễn giải của nhóm, cần đối chiếu từ điển dữ liệu gốc.")
h2("3. Hướng phát triển")
ul("Xử lý mất cân bằng lớp bằng lấy mẫu lại (oversampling, SMOTE) hoặc điều chỉnh ngưỡng quyết định, và đánh giá bằng kiểm định chéo lặp.",
   "Tinh chỉnh tham số Decision Tree, Random Forest; thử thêm các mô hình khác đã học trong môn như SVM hay mạng nơ-ron.",
   "Xét thêm các thuộc tính như khoảng cách tới điểm giao thông công cộng sau khi làm rõ ý nghĩa và làm sạch.",
   "Thu thập dữ liệu ở các đô thị khác (ví dụ Cần Thơ) để kiểm tra khả năng tổng quát; triển khai web trực tuyến.")

# =========================================================== TÀI LIỆU THAM KHẢO
h1("TÀI LIỆU THAM KHẢO")
REFS = [
 "[1] Kieu, M., Comber, A., Nguyen Thi Thuy, H., Bui Quang, T., Phe Hoang Huu, & Malleson, N. (2024). An open dataset on individual perceptions of transport policies. Scientific Data, 11, 104. https://doi.org/10.1038/s41597-024-02950-9",
 "[2] Dự án UTM-Hanoi (2023). UTM-Hanoi [bộ dữ liệu, file hn_survey_26k.csv]. Open Science Framework. https://doi.org/10.17605/OSF.IO/497US. Giấy phép CC BY 4.0, truy cập ngày 01/11/2026.",
 "[3] Tan, P.-N., Steinbach, M., Karpatne, A., & Kumar, V. (2019). Introduction to Data Mining (2nd ed.). Pearson.",
 "[4] Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825–2830.",
 "[5] Bài giảng môn Kho dữ liệu và khai phá dữ liệu (CTH603): Classification, Model evaluation, kNN. Trường Công nghệ Thông tin và Truyền thông, Đại học Cần Thơ.",
]
B.append(("refs", REFS))

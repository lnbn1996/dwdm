# -*- coding: utf-8 -*-
"""Phần dùng chung cho train.py và app.py.
Đề tài: Hệ thống dự đoán lựa chọn phương tiện di chuyển của người dân đô thị dựa vào kỹ thuật phân lớp.
Cấu hình chốt 14/11/2026: 5 nhãn, 12 feature, kNN weights="distance" k=5 (căn cứ ở ../ai_notes/).
Dữ liệu thực nghiệm: khảo sát người dân Hà Nội năm 2021 (UTM-Hanoi) - nguồn ở CITATIONS bên dưới.
Bản demo chính thức của nhóm (dùng để báo cáo), từ 14/11/2026."""
import os

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, OrdinalEncoder

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "data", "hn_survey_26k.csv")  # bản gốc trên OSF, doi 10.17605/OSF.IO/497US

TITLE = "Hệ thống dự đoán lựa chọn phương tiện di chuyển của người dân đô thị dựa vào kỹ thuật phân lớp"
DATA_SCOPE = ("Dữ liệu thực nghiệm: khảo sát người dân Hà Nội năm 2021 (dự án UTM-Hanoi), 26.106 người trả lời, "
              "do Tổng cục Thống kê thực hiện qua điện thoại; theo bài báo, mẫu lấy ngẫu nhiên 2,5% số hộ "
              "ở 4 quận trung tâm (Hoàn Kiếm, Ba Đình, Hai Bà Trưng, Đống Đa).")
CITATIONS = [
    "Kieu, M., Comber, A., Nguyen Thi Thuy, H., Bui Quang, T., Phe Hoang Huu, & Malleson, N. (2024). "
    "An open dataset on individual perceptions of transport policies. *Scientific Data*, 11, 104. "
    "https://doi.org/10.1038/s41597-024-02950-9",
    "Dự án UTM-Hanoi (2023). *UTM-Hanoi* [bộ dữ liệu, file hn_survey_26k.csv]. Open Science Framework. "
    "https://doi.org/10.17605/OSF.IO/497US. Giấy phép CC BY 4.0, truy cập ngày 01/11/2026.",
]
SOURCE_SHORT = ("Nguồn dữ liệu: khảo sát người dân Hà Nội 2021 (UTM-Hanoi) – Kieu et al. (2024), Scientific Data 11:104, "
                "doi 10.1038/s41597-024-02950-9; bộ dữ liệu trên [OSF](https://doi.org/10.17605/OSF.IO/497US), "
                "CC BY 4.0.")
# Thông tin nhóm, hiển thị ở footer của web
COURSE = "Kho dữ liệu và khai phá dữ liệu (CTH603)"
CLASS_NAME = "Lớp CTHT33"
GROUP_NAME = "Nhóm 2"
MEMBERS = ["Lê Nguyễn Bảo Ngọc", "Trần Thị Thanh Hằng"]
ART_DIR = os.path.join(HERE, "artifacts")
MODELS_PATH = os.path.join(ART_DIR, "models.joblib")
REPORT_PATH = os.path.join(ART_DIR, "report.json")

TARGET = "phuong_tien"
LABELS = ["Xe máy", "Ô tô", "Xe đạp / xe điện", "Đi bộ", "Công cộng + taxi"]  # 5 nhãn, chốt 14/11/2026
GROUP = {"moto": LABELS[0], "car": LABELS[1], "bike": LABELS[2], "ebike": LABELS[2], "walk": LABELS[3],
         "bus": LABELS[4], "taxi": LABELS[4], "tram": LABELS[4]}
LABELS_SHORT = ["Xe máy", "Ô tô", "Xe đạp", "Đi bộ", "Công cộng"]
# kNN chốt 14/11/2026 (CV lặp 5 fold x 3 lần trên tập train, xem ai_notes/chon_k.py)
KNN_K = 5
KNN_WEIGHTS = "distance"
VEHIC_VI = {"moto": "Xe máy", "car": "Ô tô", "ebike": "Xe đạp điện", "bike": "Xe đạp", "walk": "Đi bộ",
            "bus": "Xe buýt", "taxi": "Taxi", "tram": "Tàu điện"}

AGE = {"less_18": "Dưới 18", "18_25": "18–25", "26_35": "26–35", "36_55": "36–55", "56_75": "56–75", "more_75": "Trên 75"}
GENDER = {"male": "Nam", "female": "Nữ"}
OCCUP = {"state": "Nhà nước", "private": "Tư nhân", "fdi": "Doanh nghiệp FDI", "student": "Học sinh / sinh viên",
         "retired": "Nghỉ hưu"}
PURPOSE = {"work": "Đi làm", "education": "Đi học", "visit": "Thăm hỏi", "shopping": "Mua sắm",
           "leisure": "Giải trí", "caring": "Đưa đón / chăm sóc"}
FREQ = {"1_3": "1–3 chuyến", "4_7": "4–7 chuyến", "8_10": "8–10 chuyến", "11_13": "11–13 chuyến",
        "14_16": "14–16 chuyến", "17_20": "17–20 chuyến", "more_20": "Trên 20 chuyến"}
# Nhãn tiếng Việt của 3 cột nhà ở: diễn giải TẠM từ tên giá trị, cần đối chiếu với từ điển dữ liệu của bộ UTM-Hanoi
HOUSE_TYPE = {"private_house": "Nhà riêng", "private_new": "Nhà riêng (khu mới)", "high_rise": "Chung cư cao tầng",
              "old_building": "Chung cư / nhà tập thể cũ", "social_house": "Nhà ở xã hội", "resettlement": "Khu tái định cư"}
STATUS = {"permanent": "Thường trú", "long_stay": "Tạm trú dài hạn", "short_stay": "Tạm trú ngắn hạn"}
TENURE = {"parent_house": "Nhà của bố mẹ", "owner": "Chủ sở hữu", "rent": "Thuê nhà", "morgate": "Đang thế chấp"}
COUNT = {"0": "0", "1": "1", "2": "2", "3": "3", "4": "4", "more_5": "5+"}
BIKES = ["0", "1", "2", "3+"]
DIST_BINS = [0, 1, 3, 5, 10, np.inf]
DIST = ["Dưới 1 km", "1–3 km", "3–5 km", "5–10 km", "Trên 10 km"]  # khoảng cách đường chim bay

ORDINAL = {"tuoi": list(AGE.values()), "quang_duong": DIST, "so_chuyen_tuan": list(FREQ.values()),
           "so_o_to": list(COUNT.values()), "so_xe_may": list(COUNT.values()), "so_xe_dap": BIKES}
NOMINAL = ["gioi_tinh", "nghe_nghiep", "muc_dich", "loai_nha", "tinh_trang_cu_tru", "so_huu_nha"]
FEATURES = ["tuoi", "gioi_tinh", "nghe_nghiep", "muc_dich", "quang_duong", "so_chuyen_tuan", "so_o_to",
            "so_xe_may", "so_xe_dap", "loai_nha", "tinh_trang_cu_tru", "so_huu_nha"]  # 12 feature, chốt 14/11/2026
OPTIONS = {**ORDINAL, "gioi_tinh": list(GENDER.values()), "nghe_nghiep": list(OCCUP.values()),
           "muc_dich": list(PURPOSE.values()), "loai_nha": list(HOUSE_TYPE.values()),
           "tinh_trang_cu_tru": list(STATUS.values()), "so_huu_nha": list(TENURE.values())}
COL_VI = {"tuoi": "Tuổi", "gioi_tinh": "Giới tính", "nghe_nghiep": "Nghề nghiệp", "muc_dich": "Mục đích chuyến đi",
          "quang_duong": "Quãng đường", "so_chuyen_tuan": "Số chuyến mỗi tuần", "so_o_to": "Số ô tô của hộ",
          "so_xe_may": "Số xe máy của hộ", "so_xe_dap": "Số xe đạp + xe điện của hộ", "loai_nha": "Loại nhà ở",
          "tinh_trang_cu_tru": "Tình trạng cư trú", "so_huu_nha": "Hình thức sở hữu nhà", TARGET: "Phương tiện"}
RAW_SOURCE = {"tuoi": "age", "gioi_tinh": "gender", "nghe_nghiep": "occup", "muc_dich": "purp",
              "quang_duong": "OD_dist (km)", "so_chuyen_tuan": "freqpweek", "so_o_to": "own_car",
              "so_xe_may": "own_motob", "so_xe_dap": "own_bike + own_ebike", "loai_nha": "type",
              "tinh_trang_cu_tru": "status", "so_huu_nha": "own"}
ID_COLS = ["rowid", "id", "index"]
# Cột biết được SAU khi đã chọn phương tiện, hoặc gần như nói thẳng phương tiện → không dùng làm feature
LEAK = {"travtime": "thời gian chuyến đi (phụ thuộc phương tiện)",
        "reason": "lý do chọn phương tiện hiện tại (hỏi sau khi đã chọn)",
        "freq_car, freq_motob, freq_ebike, freq_bike, freq_taxi, freq_bus": "tần suất dùng từng loại xe"}


def load_raw():
    return pd.read_csv(DATA_PATH, low_memory=False)


def _count(s):
    return s.astype(str).str.strip().map(lambda v: COUNT.get(v, np.nan))


def clean(raw):
    """Làm sạch + tạo feature + gán nhãn. Trả về (df, nhật ký các bước)."""
    df, log = raw.copy(), []
    df.columns = df.columns.str.strip()

    def step(name, detail, before):
        log.append({"Bước": name, "Chi tiết": detail, "Số dòng trước": before, "Số dòng sau": len(df)})

    before = len(df)
    n_dup = int(df.drop(columns=ID_COLS).duplicated().sum())
    df = df.loc[~df.drop(columns=ID_COLS).duplicated()].copy()
    step("Bỏ dòng trùng", f"{n_dup} dòng giống hệt nhau ở mọi câu trả lời (chỉ khác mã người trả lời)", before)

    before = len(df)
    bad = (df["OD_dist"] < 0.1) | (df["OD_dist"] > 50)
    df = df[~bad].copy()
    step("Bỏ quãng đường bất thường", "dưới 0,1 km (điểm đi trùng điểm đến) hoặc trên 50 km (ngoài phạm vi thành phố)",
         before)

    df[TARGET] = df["vehic"].map(GROUP)
    df["tuoi"] = df["age"].map(AGE)
    df["gioi_tinh"] = df["gender"].map(GENDER)
    df["nghe_nghiep"] = df["occup"].map(OCCUP)
    df["muc_dich"] = df["purp"].map(PURPOSE)
    df["quang_duong"] = pd.cut(df["OD_dist"], DIST_BINS, labels=DIST, right=False).astype(str)
    df["so_chuyen_tuan"] = df["freqpweek"].map(FREQ)
    df["so_o_to"] = _count(df["own_car"])
    df["so_xe_may"] = _count(df["own_motob"])
    df["loai_nha"] = df["type"].astype(str).str.strip().map(HOUSE_TYPE)
    df["tinh_trang_cu_tru"] = df["status"].astype(str).str.strip().map(STATUS)
    df["so_huu_nha"] = df["own"].astype(str).str.strip().map(TENURE)
    n_bike = sum(df[c].astype(str).str.strip().replace("more_5", "5").astype(int) for c in ["own_bike", "own_ebike"])
    df["so_xe_dap"] = n_bike.clip(upper=3).astype(str).replace("3", "3+")
    log.append({"Bước": "Gán nhãn & tạo feature",
                "Chi tiết": "gộp 8 phương tiện thành 5 lớp; Việt hoá giá trị; chia quãng đường thành 5 mức; "
                            "gộp xe đạp + xe điện; thêm 3 feature nhà ở (loại nhà, tình trạng cư trú, sở hữu nhà)", "Số dòng trước": len(df), "Số dòng sau": len(df)})
    return df.reset_index(drop=True), log


def make_preprocessor():
    """Thứ bậc → mã số theo thứ tự; định danh → one-hot. Điền thiếu bằng mode, chỉ học từ tập train."""
    return ColumnTransformer([
        ("ordinal", make_pipeline(SimpleImputer(strategy="most_frequent"),
                                  OrdinalEncoder(categories=[ORDINAL[c] for c in ORDINAL])), list(ORDINAL)),
        ("nominal", make_pipeline(SimpleImputer(strategy="most_frequent"),
                                  OneHotEncoder(handle_unknown="ignore")), NOMINAL),
    ])


def make_knn_preprocessor():
    """Cho kNN (dựa trên khoảng cách nên nhạy với thang đo): thứ bậc → mã số rồi chuẩn hóa MinMax về [0, 1]
    để cùng thang với các cột one-hot (0/1); định danh → one-hot. Mọi thứ chỉ học từ tập train."""
    return ColumnTransformer([
        ("ordinal", make_pipeline(SimpleImputer(strategy="most_frequent"),
                                  OrdinalEncoder(categories=[ORDINAL[c] for c in ORDINAL]), MinMaxScaler()),
         list(ORDINAL)),
        ("nominal", make_pipeline(SimpleImputer(strategy="most_frequent"),
                                  OneHotEncoder(handle_unknown="ignore")), NOMINAL),
    ])

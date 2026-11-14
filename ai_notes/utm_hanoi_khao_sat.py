# -*- coding: utf-8 -*-
"""
GHI CHÚ CỦA AI - khảo sát sơ bộ dataset "Vehicle at Ha Noi" (khảo sát UTM-Hanoi) (01/11/2026).
Bài toán: dự đoán phương tiện của chuyến đi chính. Chỉ để đánh giá độ khả thi, không phải kết quả chính thức.

Chạy (từ D:/CaoHoc/DWDM):  .venv/Scripts/python.exe assignment/w0/ai_notes/utm_hanoi_khao_sat.py <đường dẫn dataHN.csv>
"""
import sys
import warnings

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")
SEED = 42
raw = pd.read_csv(sys.argv[1], low_memory=False)
raw.columns = raw.columns.str.strip()  # cột "traspeed " có dấu cách thừa

# ---- Làm sạch tối thiểu
df = raw[raw["rowid"].notna()].copy()                    # bỏ dòng "tổng cộng" ở cuối file (rowid trống)
print("Bỏ dòng tổng:", len(raw) - len(df))
before = len(df)
df = df.drop(columns="rowid").drop_duplicates()
print("Bỏ dòng trùng (không tính rowid):", before - len(df), "→ còn", len(df))

# ---- Nhãn: 7 phương tiện, hoặc gộp 4 lớp
GROUP4 = {"moto": "Xe máy", "car": "Ô tô", "bike": "Xe đạp / xe điện", "ebike": "Xe đạp / xe điện",
          "bus": "Khác (bus, taxi, đi bộ)", "taxi": "Khác (bus, taxi, đi bộ)", "walk": "Khác (bus, taxi, đi bộ)"}
df["vehic4"] = df["vehic"].map(GROUP4)
print("Nhãn 4 lớp:", df["vehic4"].value_counts(normalize=True).round(3).to_dict())

# ---- Feature (9), không có cột nào lộ nhãn
COUNT = ["0", "1", "2", "3", "4", "more_5"]
df["own_xe_dap"] = (df["own_bike"].replace("more_5", "5").astype(int) + df["own_ebike"].replace("more_5", "5").astype(int)
                    ).clip(upper=3).astype(str).replace("3", "3+")
df["khoang_cach"] = pd.cut(df["OD_dist_km"], [-1, 2, 5, 10, 20, 1e9],
                           labels=["< 2 km", "2–5 km", "5–10 km", "10–20 km", "> 20 km"]).astype(str)
ORD = {"age": ["less_18", "18_25", "26_35", "36_55", "56_75", "more_75"],
       "freqpweek": ["1_3", "4_7", "8_10", "11_13", "14_16", "17_20", "more_20"],
       "khoang_cach": ["< 2 km", "2–5 km", "5–10 km", "10–20 km", "> 20 km"],
       "own_car": COUNT, "own_motob": COUNT, "own_xe_dap": ["0", "1", "2", "3+"]}
NOM = ["gender", "occup", "purp"]
BASE = list(ORD) + NOM
LEAK = {"+ travtime, traspeed (thời gian/tốc độ chuyến đi)": ["travtime", "traspeed"],
        "+ reason (lý do chọn phương tiện)": ["reason"],
        "+ freq_* (tần suất dùng từng loại xe)": ["freq_car", "freq_motob", "freq_ebike", "freq_bike", "freq_taxi",
                                                  "freq_bus"]}


def run(cols, target):
    data = df[cols + [target]].copy()
    tr, te = train_test_split(data, test_size=0.2, stratify=data[target], random_state=SEED)
    nums = [c for c in cols if c in ("travtime", "traspeed")]
    ords = [c for c in cols if c in ORD]
    noms = [c for c in cols if c not in ORD and c not in nums]
    pre = ColumnTransformer([
        ("ord", make_pipeline(SimpleImputer(strategy="most_frequent"), OrdinalEncoder(categories=[ORD[c] for c in ords])),
         ords),
        ("nom", make_pipeline(SimpleImputer(strategy="constant", fill_value="không"),
                              OneHotEncoder(handle_unknown="ignore")), noms),
        ("num", SimpleImputer(strategy="median"), nums),
    ])
    models = {"Decision Tree": make_pipeline(pre, DecisionTreeClassifier(max_depth=10, min_samples_leaf=20,
                                                                         random_state=SEED)),
              "Random Forest": make_pipeline(pre, RandomForestClassifier(n_estimators=200, min_samples_leaf=5,
                                                                         random_state=SEED, n_jobs=-1))}
    if not nums:
        models["Naive Bayes"] = make_pipeline(
            SimpleImputer(strategy="most_frequent"),
            OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), CategoricalNB(min_categories=60))
    out = {}
    for name, m in models.items():
        pred = m.fit(tr[cols], tr[target]).predict(te[cols])
        out[name] = (accuracy_score(te[target], pred), f1_score(te[target], pred, average="macro"))
    base_acc = te[target].value_counts(normalize=True).iloc[0]
    return base_acc, out


for target, name in [("vehic4", "4 lớp"), ("vehic", "7 lớp")]:
    base_acc, out = run(BASE, target)
    print(f"\n== Nhãn {name}, 9 feature | luôn đoán lớp đông nhất: acc={base_acc:.3f}")
    for m, (a, f) in out.items():
        print(f"   {m:14s} acc={a:.3f} macro-F1={f:.3f}")
print("\n== Thêm cột lộ nhãn (nhãn 4 lớp, Random Forest)")
for name, extra in LEAK.items():
    _, out = run(BASE + extra, "vehic4")
    a, f = out["Random Forest"]
    print(f"   {name:50s} acc={a:.3f} macro-F1={f:.3f}")

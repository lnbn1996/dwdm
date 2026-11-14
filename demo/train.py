# -*- coding: utf-8 -*-
"""Huấn luyện 3 mô hình (kNN, Decision Tree, Random Forest) dự đoán lựa chọn phương tiện di chuyển (dữ liệu: khảo sát người dân Hà Nội 2021), lưu vào artifacts/. Bản demo chính thức của nhóm.

Chạy (từ D:\\CaoHoc\\DWDM):  .venv/Scripts/python.exe assignment/w1/demo/train.py
"""
import json
import os
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (ART_DIR, FEATURES, KNN_K, KNN_WEIGHTS, LABELS, MODELS_PATH, NOMINAL, OPTIONS, ORDINAL, RAW_SOURCE, REPORT_PATH, TARGET,
                    VEHIC_VI, clean, load_raw, make_knn_preprocessor, make_preprocessor)

SEED = 42

# ---- 1. Hiểu dữ liệu gốc
raw = load_raw()
raw.columns = raw.columns.str.strip()
eda = {
    "shape": list(raw.shape),
    "vehic": {VEHIC_VI[k]: int(v) for k, v in raw["vehic"].value_counts().items()},
    "missing": {c: int(n) for c, n in raw.isna().sum().items() if n > 0},
    "duplicates": int(raw.drop(columns=["rowid", "id", "index"]).duplicated().sum()),
    "travtime_max": int(raw["travtime"].max()), "dist_small": int((raw["OD_dist"] < 0.1).sum()),
    "dist_large": int((raw["OD_dist"] > 50).sum()),
    "sample": raw[["age", "gender", "occup", "purp", "vehic", "OD_dist", "travtime", "freqpweek", "own_car",
                   "own_motob", "reason", "opinion_ban"]].head(8).astype(str).to_dict(orient="records"),
}

# ---- 2. Làm sạch, tạo feature, gán nhãn
df, cleaning_log = clean(raw)
X, y = df[FEATURES], df[TARGET]
features = [{"Feature": c, "Cột gốc": RAW_SOURCE[c], "Số giá trị": int(df[c].nunique()),
             "Kiểu": "Thứ bậc" if c in ORDINAL else "Định danh"} for c in FEATURES]
explore = {}
for c in FEATURES:
    share = pd.crosstab(df[c], df[TARGET], normalize="index").reindex(columns=LABELS, fill_value=0)
    count = df[c].value_counts()
    explore[c] = [{"giá trị": v, "lớp": lab, "tỉ lệ": float(share.loc[v, lab]), "số chuyến": int(count[v])}
                  for v in OPTIONS[c] if v in share.index for lab in LABELS]
moto = df[df["vehic"] == "moto"]
alt = {"Ô tô": "alt_car", "Xe buýt": "alt_bus", "Taxi": "alt_taxi", "Xe đạp": "alt_bike", "Tàu điện": "alt_ltrain",
       "Xe đạp điện": "alt_ebike", "Đi bộ": "alt_walk"}
ban = {"n_moto": len(moto), "alt": {k: float((moto[c] == 1).mean()) for k, c in alt.items()},
       "opinion": moto["opinion_ban"].value_counts(normalize=True).round(4).to_dict()}
print("Sau làm sạch:", df.shape)

# ---- 3. Chia train/test có phân tầng theo nhãn
idx_tr, idx_te = train_test_split(df.index, test_size=0.2, stratify=y, random_state=SEED)
X_tr, X_te, y_tr, y_te = X.loc[idx_tr], X.loc[idx_te], y.loc[idx_tr], y.loc[idx_te]

# ---- 4. Ba mô hình (+ baseline đoán lớp đông nhất)
cv = StratifiedKFold(5, shuffle=True, random_state=SEED)
# kNN: cấu hình chốt 14/11/2026 là weights="distance", k=5 (chọn bằng CV lặp trên tập train, xem ai_notes/chon_k.py).
# Ở đây vẫn đo CV macro-F1 vài giá trị k để ghi vào báo cáo; tập test không được đụng tới.
knn_cv = {k: float(cross_val_score(make_pipeline(make_knn_preprocessor(),
                                                 KNeighborsClassifier(n_neighbors=k, weights=KNN_WEIGHTS)),
                                   X_tr, y_tr, cv=cv, scoring="f1_macro").mean()) for k in (3, 5, 11, 21)}
best_k = KNN_K
print(f"kNN ({KNN_WEIGHTS}) – CV macro-F1 theo k:", {k: round(v, 3) for k, v in knn_cv.items()}, "→ dùng k =", best_k)
models = {
    "kNN": make_pipeline(make_knn_preprocessor(), KNeighborsClassifier(n_neighbors=best_k, weights=KNN_WEIGHTS)),
    "Decision Tree": make_pipeline(make_preprocessor(),
                                   DecisionTreeClassifier(max_depth=10, min_samples_leaf=20, random_state=SEED)),
    "Random Forest": make_pipeline(make_preprocessor(),
                                   RandomForestClassifier(n_estimators=200, min_samples_leaf=5, random_state=SEED,
                                                          n_jobs=-1)),
}
baseline = DummyClassifier(strategy="most_frequent")
cv_f1 = {}
for name, model in models.items():
    cv_f1[name] = float(cross_val_score(model, X_tr, y_tr, cv=cv, scoring="f1_macro").mean())
    print(f"CV macro-F1 {name}: {cv_f1[name]:.3f}")
best = max(cv_f1, key=cv_f1.get)

# ---- 5. Đánh giá trên tập test
metrics, confusion = {}, {}
for name, model in [("Luôn đoán xe máy", baseline), *models.items()]:
    model.fit(X_tr, y_tr)
    pred = model.predict(X_te)
    metrics[name] = {
        "CV macro-F1 (train)": cv_f1.get(name),
        "Accuracy": accuracy_score(y_te, pred),
        "Precision (macro)": precision_score(y_te, pred, average="macro", zero_division=0),
        "Recall (macro)": recall_score(y_te, pred, average="macro"),
        "F1 (macro)": f1_score(y_te, pred, average="macro"),
    }
    confusion[name] = confusion_matrix(y_te, pred, labels=LABELS).tolist()
    print(f"Test {name}: " + ", ".join(f"{k}={v:.3f}" for k, v in metrics[name].items() if v is not None))

rf = models["Random Forest"]
imp = {}
for n, v in zip(rf[0].get_feature_names_out(), rf[-1].feature_importances_):
    col = n.split("__", 1)[1]
    base = next((c for c in NOMINAL if col.startswith(c + "_")), col)
    imp[base] = imp.get(base, 0.0) + float(v)

# ---- 6. Thí nghiệm rò rỉ nhãn: thêm các cột chỉ biết SAU khi đã chọn phương tiện
df["toc_do"] = df["OD_dist"] / (df["travtime"].where(df["travtime"] > 0) / 60)
freq = ["freq_car", "freq_motob", "freq_ebike", "freq_bike", "freq_taxi", "freq_bus"]
leak_sets = {"+ thời gian và tốc độ chuyến đi": (["travtime", "toc_do"], []),
             "+ lý do chọn phương tiện": ([], ["reason"]),
             "+ tần suất dùng từng loại xe": ([], freq)}
leakage = {f"{len(FEATURES)} feature (không lộ nhãn)": metrics["Random Forest"]["Accuracy"]}
for name, (nums, cats) in leak_sets.items():
    pre = ColumnTransformer([("base", make_preprocessor(), FEATURES),
                             ("num", SimpleImputer(strategy="median"), nums),
                             ("cat", make_pipeline(SimpleImputer(strategy="constant", fill_value="không dùng"),
                                                   OneHotEncoder(handle_unknown="ignore")), cats)])
    m = make_pipeline(pre, RandomForestClassifier(n_estimators=200, min_samples_leaf=5, random_state=SEED, n_jobs=-1))
    cols = FEATURES + nums + cats
    leakage[name] = accuracy_score(y_te, m.fit(df.loc[idx_tr, cols], y_tr).predict(df.loc[idx_te, cols]))
    print(f"Rò rỉ {name}: acc={leakage[name]:.3f}")

os.makedirs(ART_DIR, exist_ok=True)
joblib.dump({"models": models, "best": best}, MODELS_PATH, compress=3)
report = {
    "eda": eda, "cleaning": cleaning_log, "clean_rows": len(df), "features": features, "explore": explore,
    "ban": ban, "label_counts": {lab: int((y == lab).sum()) for lab in LABELS},
    "median_dist": {VEHIC_VI[k]: round(float(v), 2) for k, v in df.groupby("vehic")["OD_dist"].median().items()},
    "split": {"train": len(idx_tr), "test": len(idx_te)},
    "knn_cv": knn_cv, "best_k": best_k, "metrics": metrics, "confusion": confusion, "best": best, "leakage": leakage,
    "importance": dict(sorted(imp.items(), key=lambda kv: -kv[1])),
}
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2, default=lambda o: o.item() if isinstance(o, np.generic) else o)
print("Mô hình chọn:", best, "→ đã lưu", MODELS_PATH)

# -*- coding: utf-8 -*-
"""Ghi chú của AI (14/11/2026) - chạy từ D:\\CaoHoc\\DWDM:  .venv\\Scripts\\python.exe assignment\\w1\\ai_notes\\so_sanh_5nhan.py
So sánh 5 nhãn x 3 bộ feature (9 / 12 / 13) với kNN, Decision Tree, Random Forest."""
import os, sys, json, warnings
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "demo"))
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier
import common as C

SEED = 42
LAB5 = ["Xe máy", "Ô tô", "Xe đạp / xe điện", "Đi bộ", "Công cộng + taxi"]
G5 = {"moto": LAB5[0], "car": LAB5[1], "bike": LAB5[2], "ebike": LAB5[2], "walk": LAB5[3],
      "bus": LAB5[4], "taxi": LAB5[4], "tram": LAB5[4]}

raw = C.load_raw(); raw.columns = raw.columns.str.strip()
df, _ = C.clean(raw)
df["y"] = df["vehic"].map(G5)
print("Số dòng sau làm sạch:", len(df)); print(df["y"].value_counts().to_dict())

# feature bổ sung
df["loai_nha"] = df["type"].astype(str)
df["tinh_trang_cu_tru"] = df["status"].astype(str)
df["so_huu_nha"] = df["own"].astype(str)
df["kc_cong_cong_m"] = df["dist_to_pub"].clip(0, 3000)          # dữ liệu có giá trị âm và 5e7 -> cắt [0, 3000]
bk = lambda c: df[c].astype(str).str.strip().replace("more_5", "5").astype(int).clip(upper=3).astype(str).replace("3", "3+")
df["so_xe_dap_thuong"] = bk("own_bike"); df["so_xe_dien"] = bk("own_ebike")

ORD = dict(C.ORDINAL); ORD["so_xe_dap_thuong"] = C.BIKES; ORD["so_xe_dien"] = C.BIKES
base_ord = ["tuoi", "quang_duong", "so_chuyen_tuan", "so_o_to", "so_xe_may"]
base_nom = ["gioi_tinh", "nghe_nghiep", "muc_dich"]
CONFIGS = {
    "9 feature": dict(ordc=base_ord + ["so_xe_dap"], nom=base_nom, num=[]),
    "12 feature (9 + loại nhà, tình trạng cư trú, sở hữu nhà)":
        dict(ordc=base_ord + ["so_xe_dap"], nom=base_nom + ["loai_nha", "tinh_trang_cu_tru", "so_huu_nha"], num=[]),
    "13 feature (tách xe đạp/xe điện + loại nhà, sở hữu nhà, KC công cộng)":
        dict(ordc=base_ord + ["so_xe_dap_thuong", "so_xe_dien"], nom=base_nom + ["loai_nha", "so_huu_nha"], num=["kc_cong_cong_m"]),
}

def prep(cfg, knn):
    ordsteps = [SimpleImputer(strategy="most_frequent"), OrdinalEncoder(categories=[ORD[c] for c in cfg["ordc"]])]
    if knn: ordsteps.append(MinMaxScaler())
    tr = [("ord", make_pipeline(*ordsteps), cfg["ordc"]),
          ("nom", make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore")), cfg["nom"])]
    if cfg["num"]:
        nsteps = [SimpleImputer(strategy="median")] + ([MinMaxScaler()] if knn else [])
        tr.append(("num", make_pipeline(*nsteps), cfg["num"]))
    return ColumnTransformer(tr)

y = df["y"]
idx_tr, idx_te = train_test_split(df.index, test_size=0.2, stratify=y, random_state=SEED)
cv = StratifiedKFold(5, shuffle=True, random_state=SEED)
out = {}
for cname, cfg in CONFIGS.items():
    cols = cfg["ordc"] + cfg["nom"] + cfg["num"]
    Xtr, Xte, ytr, yte = df.loc[idx_tr, cols], df.loc[idx_te, cols], y.loc[idx_tr], y.loc[idx_te]
    ks = {k: cross_val_score(make_pipeline(prep(cfg, True), KNeighborsClassifier(n_neighbors=k)), Xtr, ytr, cv=cv, scoring="f1_macro").mean()
          for k in (3, 5, 11, 21, 31)}
    bk_ = max(ks, key=ks.get)
    models = {"kNN": make_pipeline(prep(cfg, True), KNeighborsClassifier(n_neighbors=bk_)),
              "Decision Tree": make_pipeline(prep(cfg, False), DecisionTreeClassifier(max_depth=10, min_samples_leaf=20, random_state=SEED)),
              "Random Forest": make_pipeline(prep(cfg, False), RandomForestClassifier(n_estimators=200, min_samples_leaf=5, random_state=SEED, n_jobs=2))}
    out[cname] = {"k": bk_, "knn_cv": {int(k): round(v, 4) for k, v in ks.items()}}
    for mname, m in models.items():
        s = cross_val_score(m, Xtr, ytr, cv=cv, scoring="f1_macro")
        m.fit(Xtr, ytr); p = m.predict(Xte)
        pc = f1_score(yte, p, labels=LAB5, average=None, zero_division=0)
        out[cname][mname] = {"cv_f1_mean": round(s.mean(), 4), "cv_f1_std": round(s.std(), 4),
                             "acc": round(accuracy_score(yte, p), 4), "f1_macro": round(f1_score(yte, p, average="macro"), 4),
                             "f1_class": {l: round(v, 3) for l, v in zip(LAB5, pc)}}
        print(cname, mname, out[cname][mname]["cv_f1_mean"], out[cname][mname]["acc"], out[cname][mname]["f1_macro"], flush=True)
out["_meta"] = {"n": len(df), "n_train": len(idx_tr), "n_test": len(idx_te), "counts": y.value_counts().to_dict(), "test_counts": y.loc[idx_te].value_counts().to_dict()}
json.dump(out, open(os.path.join(HERE, "so_sanh_5nhan_ketqua.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

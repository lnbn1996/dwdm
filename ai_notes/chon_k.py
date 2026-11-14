# -*- coding: utf-8 -*-
"""Ghi chú của AI (14/11/2026) - chạy: .venv\\Scripts\\python.exe assignment\\w1\\ai_notes\\chon_k.py
 chọn k cho kNN bằng CV lặp (5 fold x 3 lần) trên TẬP TRAIN, bộ 12 feature, 5 nhãn."""
import os, warnings; warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "so_sanh_5nhan.py"), encoding="utf-8").read().split("y = df[\"y\"]")[0])
import json
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.neighbors import NearestNeighbors
y = df["y"]
idx_tr, idx_te = train_test_split(df.index, test_size=0.2, stratify=y, random_state=42)
cfg = CONFIGS["12 feature (9 + loại nhà, tình trạng cư trú, sở hữu nhà)"]
cols = cfg["ordc"] + cfg["nom"] + cfg["num"]
X, yy = df.loc[idx_tr, cols].reset_index(drop=True), y.loc[idx_tr].reset_index(drop=True)
classes = np.array(sorted(yy.unique())); yi = pd.Categorical(yy, categories=classes).codes
KS = list(range(1, 16)); KMAX = max(KS)
rskf = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)
res = {(w, k): {"f1": [], "acc": []} for w in ("uniform", "distance") for k in KS}
for f, (a, b) in enumerate(rskf.split(X, yy)):
    pre = prep(cfg, True).fit(X.iloc[a]); Xa, Xb = pre.transform(X.iloc[a]), pre.transform(X.iloc[b])
    nn = NearestNeighbors(n_neighbors=KMAX).fit(Xa); dist, ind = nn.kneighbors(Xb)
    lab = yi[a][ind]                                  # nhãn của KMAX láng giềng, đã sắp theo khoảng cách
    for w in ("uniform", "distance"):
        if w == "uniform": W = np.ones_like(dist)
        else:
            with np.errstate(divide="ignore"): W = 1.0 / dist
            z = np.isinf(W).any(axis=1); W[z] = np.isinf(W[z]).astype(float)   # như sklearn: d=0 thì chỉ các điểm trùng được tính
        for k in KS:
            votes = np.zeros((len(b), len(classes)))
            for c in range(len(classes)): votes[:, c] = (W[:, :k] * (lab[:, :k] == c)).sum(1)
            p = votes.argmax(1)
            res[(w, k)]["f1"].append(f1_score(yi[b], p, average="macro")); res[(w, k)]["acc"].append(accuracy_score(yi[b], p))
    print("fold", f + 1, "xong", flush=True)
out = {}
best = max(res, key=lambda t: np.mean(res[t]["f1"])); bf = np.array(res[best]["f1"])
print("\nTốt nhất theo CV macro-F1:", best, "%.4f" % bf.mean())
print("%-9s %2s  %-16s %-8s %s" % ("weights", "k", "macro-F1 ± sd", "acc", "chênh so với tốt nhất (mean ± sd chênh theo fold ghép cặp)"))
for w in ("uniform", "distance"):
    for k in KS:
        f = np.array(res[(w, k)]["f1"]); a_ = np.array(res[(w, k)]["acc"]); d = f - bf
        out[f"{w}_{k}"] = {"f1_mean": f.mean(), "f1_sd": f.std(), "acc_mean": a_.mean(), "diff_mean": d.mean(), "diff_sd": d.std()}
        print("%-9s %2d  %.4f ± %.4f  %.4f   %+.4f ± %.4f" % (w, k, f.mean(), f.std(), a_.mean(), d.mean(), d.std()))
json.dump({"best": list(best), "n_train": len(X), "folds": 15, "ket_qua": out}, open(os.path.join(HERE, "chon_k_ketqua.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

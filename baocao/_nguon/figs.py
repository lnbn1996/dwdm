# -*- coding: utf-8 -*-
"""Vẽ các hình cho báo cáo từ artifacts/report.json và ai_notes/chon_k_ketqua.json."""
import json, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
REPORT, CHONK, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
r = json.load(open(REPORT, encoding="utf8")); ck = json.load(open(CHONK, encoding="utf8"))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
TEAL, TEAL2 = "#0F766E", "#94C9C2"
LABELS = ["Xe máy", "Ô tô", "Xe đạp / xe điện", "Đi bộ", "Công cộng + taxi"]
PAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#7a5cc7"]
def save(fig, name): fig.tight_layout(); fig.savefig(f"{OUT}/{name}.png", dpi=170); plt.close(fig)

# Hình 2.1 – phân bố phương tiện gốc
v = r["eda"]["vehic"]; tot = sum(v.values())
fig, ax = plt.subplots(figsize=(7, 3.4))
names = list(v)[::-1]; vals = [v[n] for n in names]
ax.barh(names, vals, color=TEAL)
for i, x in enumerate(vals): ax.text(x + 150, i, f"{x:,}".replace(",", ".") + f" ({x / tot:.1%})".replace(".", ",", 1), va="center", fontsize=9)
ax.set_xlim(0, max(vals) * 1.28); ax.set_xlabel("Số chuyến đi")
save(fig, "h2_1")

# Hình 2.2 – tỉ lệ phương tiện theo quãng đường
ex = r["explore"]["quang_duong"]; groups = ["Dưới 1 km", "1–3 km", "3–5 km", "5–10 km", "Trên 10 km"]
fig, ax = plt.subplots(figsize=(7, 3.2))
left = [0] * len(groups)
for lab, col in zip(LABELS, PAL):
    w = [next(e["tỉ lệ"] for e in ex if e["giá trị"] == g and e["lớp"] == lab) for g in groups]
    ax.barh(groups, w, left=left, color=col, label=lab, edgecolor="white", linewidth=1)
    left = [a + b for a, b in zip(left, w)]
ax.invert_yaxis(); ax.set_xlim(0, 1); ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1))
ax.legend(ncol=5, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, 1.18), frameon=False)
save(fig, "h2_2")

# Hình 3.1 – macro-F1 CV theo k
ks = list(range(1, 16)); res = ck["ket_qua"]
fig, ax = plt.subplots(figsize=(7, 3.2))
for w, col, lab in [("uniform", "#9AA5A8", "weights = uniform"), ("distance", TEAL, "weights = distance")]:
    m = [res[f"{w}_{k}"]["f1_mean"] for k in ks]
    ax.plot(ks, m, marker="o", color=col, label=lab, linewidth=2 if w == "distance" else 1.5)
ax.axvline(5, color=TEAL, linestyle=":", linewidth=1); ax.text(5.2, 0.533, "k = 5 (chọn)", color=TEAL, fontsize=9)
ax.set_xticks(ks); ax.set_xlabel("k"); ax.set_ylabel("macro-F1 (CV lặp 5 fold × 3)"); ax.legend(frameon=False)
save(fig, "h3_1")

# Hình 3.2 – độ quan trọng thuộc tính (Random Forest)
COL_VI = {"tuoi": "Tuổi", "gioi_tinh": "Giới tính", "nghe_nghiep": "Nghề nghiệp", "muc_dich": "Mục đích chuyến đi",
          "quang_duong": "Quãng đường", "so_chuyen_tuan": "Số chuyến mỗi tuần", "so_o_to": "Số ô tô của hộ",
          "so_xe_may": "Số xe máy của hộ", "so_xe_dap": "Số xe đạp + xe điện của hộ", "loai_nha": "Loại nhà ở",
          "tinh_trang_cu_tru": "Tình trạng cư trú", "so_huu_nha": "Hình thức sở hữu nhà"}
imp = r["importance"]; names = [COL_VI[k] for k in imp][::-1]; vals = list(imp.values())[::-1]
fig, ax = plt.subplots(figsize=(7, 3.8))
ax.barh(names, vals, color=TEAL)
for i, x in enumerate(vals): ax.text(x + 0.002, i, f"{x:.3f}".replace(".", ","), va="center", fontsize=8.5)
ax.set_xlim(0, max(vals) * 1.15); ax.set_xlabel("Độ quan trọng (giảm Gini trung bình)")
save(fig, "h3_2")

# Hình 4.1 – kiến trúc hệ thống
fig, ax = plt.subplots(figsize=(7.2, 2.6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 3.2)
boxes = [(0.1, "Dữ liệu gốc\nhn_survey_26k.csv"), (2.6, "train.py\nlàm sạch, huấn luyện,\nđánh giá"),
         (5.1, "artifacts/\nmodels.joblib\nreport.json"), (7.6, "app.py (Streamlit)\nweb 6 tab\n→ người dùng")]
for x, t in boxes:
    ax.add_patch(FancyBboxPatch((x, 0.9), 2.2, 1.5, boxstyle="round,pad=0.05", fc="#E3EFED", ec=TEAL, lw=1.4))
    ax.text(x + 1.1, 1.65, t, ha="center", va="center", fontsize=9)
for x in (2.35, 4.85, 7.35):
    ax.annotate("", xy=(x + 0.22, 1.65), xytext=(x - 0.05, 1.65), arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.5))
ax.text(5.0, 0.35, "common.py: hằng số, ánh xạ giá trị, hàm clean() và bộ tiền xử lý dùng chung cho train.py và app.py",
        ha="center", fontsize=8.5, color="#3E4C52")
save(fig, "h4_1")
print("ok")

# -*- coding: utf-8 -*-
"""Web demo: Hệ thống dự đoán lựa chọn phương tiện di chuyển của người dân đô thị (bản chính thức của nhóm).
Bố cục: thanh tiêu đề cố định; thanh tab dính ngay dưới tiêu đề (bấm tab nào hiện tab đó, tab đang chọn được tô màu);
footer ghi thông tin nhóm và nguồn dữ liệu.

Chạy (từ D:\\CaoHoc\\DWDM):
    .venv/Scripts/python.exe assignment/w1/demo/train.py      # một lần, tạo artifacts/
    .venv/Scripts/streamlit.exe run assignment/w1/demo/app.py
"""
import json
import os
import re
import sys

import altair as alt
import joblib
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (CITATIONS, CLASS_NAME, COL_VI, COURSE, DATA_SCOPE, FEATURES, GROUP_NAME, KNN_K, KNN_WEIGHTS, LABELS,
                    LABELS_SHORT, LEAK, MEMBERS, MODELS_PATH, OPTIONS, ORDINAL, REPORT_PATH, SOURCE_SHORT, TITLE)

st.set_page_config(page_title="Hệ thống dự đoán phương tiện di chuyển", layout="wide")

# ---- Giao diện: tông xanh lục đậm (teal). Màu nền/nút chính đặt ở .streamlit/config.toml (thư mục gốc D:\CaoHoc\DWDM)
PRIMARY, PRIMARY_DARK = "#0F766E", "#0B4F4A"
TITLE_H = 64  # chiều cao thanh tiêu đề cố định (px); thanh tab dính ngay bên dưới
TOP_GAP = 2   # khoảng cách từ thanh tiêu đề tới thanh tab (px)
# Thứ tự tab: chức năng chính trước, rồi kết quả mô hình, rồi dữ liệu theo đúng trình tự xử lý, cuối cùng là phân tích thêm
TAB_NAMES = ["Dự đoán phương tiện", "So sánh mô hình", "Dữ liệu gốc", "Làm sạch & chọn cột", "Khám phá dữ liệu",
             "Phương tiện thay thế khi cấm xe máy"]

CSS = f"""
<style>
header[data-testid="stHeader"], div[data-testid="stDecoration"], div[data-testid="stToolbar"] {{display: none !important;}}
div[data-testid="stMainBlockContainer"], .block-container {{padding-top: {TITLE_H + TOP_GAP}px !important;
    padding-bottom: 0 !important; max-width: 1280px;}}

/* Thanh tiêu đề cố định */
.app-header {{position: fixed; top: 0; left: 0; right: 0; height: {TITLE_H}px; z-index: 999999; display: flex;
    align-items: center; background: linear-gradient(90deg, {PRIMARY_DARK}, {PRIMARY}); box-shadow: 0 2px 8px rgba(0,0,0,.2);}}
.app-header .inner {{width: 100%; max-width: 1280px; margin: 0 auto; padding: 0 24px;}}
.app-header .title {{font-size: 1.25rem; font-weight: 700; line-height: 1.25; color: #fff; letter-spacing: .2px;}}

/* Thanh tab kiểu tab trình duyệt: tab đang chọn cùng nền với khung nội dung và nối liền với khung;
   các tab còn lại nền xanh nhạt nằm phía sau. Thanh tab dính dưới tiêu đề khi cuộn.
   Dùng thuộc tính ARIA (role, aria-selected) vì ổn định hơn các data-* nội bộ của Streamlit. */
[role="tablist"] {{position: sticky; top: {TITLE_H}px; z-index: 999990; gap: 4px !important; padding: 6px 0 0 0;
    margin: 0 !important; background: #F7FAF9; border: none !important; border-bottom: 1px solid #C9E0DC !important;
    border-radius: 0; box-shadow: none;}}
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {{display: none !important;}}
[role="tab"] {{height: auto !important; padding: 9px 18px !important; margin: 0 0 -1px 0 !important;
    background: #E3EFED !important; border: 1px solid #C9E0DC !important; border-bottom: none !important;
    border-radius: 10px 10px 0 0 !important; transition: background .18s;}}
[role="tab"] p {{font-size: .95rem; font-weight: 500; color: {PRIMARY_DARK} !important;}}
[role="tab"]:hover {{background: #D3E7E3 !important;}}
[role="tab"]:focus-visible {{outline: 2px solid {PRIMARY}; outline-offset: -2px;}}
[role="tab"][aria-selected="true"] {{background: #FFFFFF !important; box-shadow: none;
    border-bottom: 1px solid #FFFFFF !important;}}
[role="tab"][aria-selected="true"] p {{color: {PRIMARY} !important; font-weight: 700;}}
/* Khung nội dung của tab: nền trắng, viền nối tiếp từ tab đang chọn */
[role="tabpanel"] {{background: #FFFFFF; border: 1px solid #C9E0DC; border-top: none; border-radius: 0 0 10px 10px;
    padding: 20px 24px !important;}}

/* Tiêu đề mục (st.subheader) nhỏ lại để tiêu đề dài như "Độ quan trọng của feature (Random Forest)" nằm trên một hàng */
[data-testid="stHeadingWithActionElements"] h3, .stMarkdown h3 {{font-size: 1.4rem !important; line-height: 1.35;}}

/* Chữ xám (chú thích, nhãn metric) đậm hơn mặc định */
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] *, [data-testid="stCaption"],
[data-testid="stCaption"] *, .stCaption, .stCaption *, [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * {{color: #4A5A60 !important; opacity: 1 !important;}}

/* Footer: luôn nằm cuối màn hình khi nội dung ngắn hơn chiều cao cửa sổ */
div[data-testid="stVerticalBlock"]:has(> div .app-footer) {{min-height: calc(100vh - {TITLE_H + TOP_GAP}px);}}
div[data-testid="stElementContainer"]:has(.app-footer) {{margin-top: auto; margin-bottom: 0 !important;}}
div[data-testid="stMarkdownContainer"]:has(> .app-footer), div[data-testid="stMarkdown"]:has(.app-footer) {{
    margin: 0 !important; padding: 0 !important;}}
.app-footer {{margin: 24px 0 0; padding: 12px 24px; border-radius: 0; background: {PRIMARY_DARK};
    color: #E3EFED; font-size: .95rem; line-height: 1.5; display: flex; align-items: stretch; gap: 20px;}}
.app-footer .col {{flex: 0 0 auto;}}
.app-footer .vline {{width: 1px; flex: 0 0 1px; margin: 6px 0; background: rgba(255,255,255,.35);}}
.app-footer b {{color: #fff;}}
.app-footer a {{color: #fff !important;}}
.app-footer ul {{margin: 2px 0 0; padding-left: 20px;}}
.app-footer li {{margin: 0; padding: 0;}}
.app-footer .col.src {{flex: 1 1 auto; min-width: 0; font-size: .88rem; opacity: .92; align-self: center;}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# Bảng màu phân loại 5 lớp (thứ tự cố định). 4 màu đầu đã kiểm tra mù màu ở nền sáng và tối; màu thứ 5 (tím) thêm ngày 14/11, chưa kiểm tra
PALETTE = {"light": ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#7a5cc7"],
           "dark": ["#3987e5", "#d95926", "#199e70", "#c98500", "#9b7de0"]}


@st.cache_resource
def load_artifacts():
    bundle = joblib.load(MODELS_PATH)
    with open(REPORT_PATH, encoding="utf-8") as f:
        return bundle["models"], bundle["best"], json.load(f)


def fit_height(n_rows):
    """Chiều cao (px) để bảng st.dataframe hiện đủ n_rows dòng + dòng tiêu đề, không có thanh cuộn."""
    return 35 * (n_rows + 1) + 3


def num(n):
    return f"{n:,}".replace(",", ".")


def is_dark():
    """Theme đã cố định nền sáng trong .streamlit/config.toml (base = "light").
    Không đọc st.context.theme: ở lần hiển thị đầu tiên giá trị này có thể chưa đúng (theo theme của máy),
    làm biểu đồ vẽ viền đen; chỉ khi chọn lại mới đúng."""
    return False


def hbar(data, label, value, fmt, order="-x", domain=None, tooltip_extra=()):
    """Biểu đồ cột ngang một chuỗi, có nhãn giá trị và tooltip. order: "-x" (giảm dần) hoặc danh sách thứ tự."""
    x = alt.X(f"{value}:Q", title=None, axis=alt.Axis(format=fmt),
              scale=alt.Scale(domain=domain) if domain else alt.Undefined)
    base = alt.Chart(data).encode(
        y=alt.Y(f"{label}:N", sort=order, title=None, axis=alt.Axis(labelLimit=320)), x=x,
        tooltip=[alt.Tooltip(f"{label}:N"), alt.Tooltip(f"{value}:Q", format=fmt), *tooltip_extra])
    bars = base.mark_bar(color=PRIMARY, size=18, cornerRadiusEnd=4)
    text = base.mark_text(align="left", dx=4).encode(text=alt.Text(f"{value}:Q", format=fmt))
    return (bars + text).properties(height=34 * len(data) + 20)


def stacked(data, order):
    """Cột ngang 100%: tỉ lệ 5 nhóm phương tiện trong từng nhóm; khe 2px giữa các đoạn."""
    # Ghi số chuyến cạnh tên nhóm: nhóm rất nhỏ (vài chục chuyến) vẫn vẽ dài bằng nhóm lớn
    data = data.assign(thu_tu=data["lớp"].map(LABELS.index),
                       nhom=data["giá trị"] + " (" + data["số chuyến"].map(num) + ")")
    order = [n for v in order for n in data.loc[data["giá trị"] == v, "nhom"].unique()]
    surface = "#0e1117" if is_dark() else "#ffffff"
    chart = alt.Chart(data).mark_bar(size=22, stroke=surface, strokeWidth=2).encode(
        y=alt.Y("nhom:N", sort=order, title=None, axis=alt.Axis(labelLimit=320)),
        x=alt.X("tỉ lệ:Q", stack="normalize", title=None, axis=alt.Axis(format="%")),
        color=alt.Color("lớp:N", title=None, legend=alt.Legend(orient="top"),
                        scale=alt.Scale(domain=LABELS, range=PALETTE["dark" if is_dark() else "light"])),
        order=alt.Order("thu_tu:Q"),
        tooltip=[alt.Tooltip("giá trị:N", title="Nhóm"), alt.Tooltip("lớp:N", title="Phương tiện"),
                 alt.Tooltip("tỉ lệ:Q", format=".0%", title="Tỉ lệ"), alt.Tooltip("số chuyến:Q", format=",")])
    return chart.properties(height=36 * data["giá trị"].nunique() + 40)


if not (os.path.exists(MODELS_PATH) and os.path.exists(REPORT_PATH)):
    st.error("Chưa có mô hình. Chạy train.py trước:")
    st.code(".venv/Scripts/python.exe assignment/w1/demo/train.py")
    st.stop()

models, best, report = load_artifacts()
eda = report["eda"]

# ---------------------------------------------------------------- thanh tiêu đề + thanh tab
st.markdown(f'<div class="app-header"><div class="inner"><div class="title">{TITLE}</div></div></div>',
            unsafe_allow_html=True)
tab = dict(zip(TAB_NAMES, st.tabs(TAB_NAMES)))

# ---------------------------------------------------------------- Dự đoán phương tiện
with tab["Dự đoán phương tiện"]:
    st.caption("Chọn thông tin người đi và chuyến đi rồi bấm nút: mô hình cho biết phương tiện nhiều khả năng nhất.")
    defaults = {"tuoi": "26–35", "gioi_tinh": "Nam", "nghe_nghiep": "Nhà nước", "muc_dich": "Đi làm",
                "quang_duong": "3–5 km", "so_chuyen_tuan": "4–7 chuyến", "so_o_to": "1", "so_xe_may": "2",
                "so_xe_dap": "0", "loai_nha": "Nhà riêng", "tinh_trang_cu_tru": "Thường trú",
                "so_huu_nha": "Chủ sở hữu"}
    # Giá trị của form nằm trong session_state (khóa "f_<cột>", "f_model") để nút Xóa đưa được về mặc định
    for col in FEATURES:
        st.session_state.setdefault(f"f_{col}", defaults[col])
    st.session_state.setdefault("f_model", best)

    def reset_form():
        """Nút Xóa: đưa mọi ô về giá trị mặc định và ẩn kết quả dự đoán."""
        for c in FEATURES:
            st.session_state[f"f_{c}"] = defaults[c]
        st.session_state["f_model"] = best
        st.session_state.pop("ket_qua_du_doan", None)

    with st.form("predict"):
        row = {}
        for container, group in zip(st.columns(3), [FEATURES[0:4], FEATURES[4:8], FEATURES[8:12]]):
            for col in group:
                row[col] = container.selectbox(COL_VI[col], OPTIONS[col], key=f"f_{col}")
        model_name = st.selectbox("Mô hình", list(models), key="f_model")
        b1, b2, _ = st.columns([1, 1, 10], gap="small")
        go = b1.form_submit_button("Dự đoán", type="primary", width="stretch")
        b2.form_submit_button("Xóa", type="secondary", width="stretch", on_click=reset_form)
    if go:
        st.session_state["ket_qua_du_doan"] = (model_name, row)
    # Kết quả được giữ lại khi chuyển tab hay thao tác ở tab khác, cho tới khi bấm Dự đoán lần nữa hoặc bấm Xóa
    if "ket_qua_du_doan" in st.session_state:
        model_name, row = st.session_state["ket_qua_du_doan"]
        model = models[model_name]
        proba = model.predict_proba(pd.DataFrame([row]))[0]
        probs = pd.DataFrame({"Phương tiện": model.classes_, "Xác suất": proba})
        top = probs.loc[probs["Xác suất"].idxmax()]
        st.success(f"{model_name} dự đoán: **{top['Phương tiện']}** (xác suất {top['Xác suất']:.0%}).")
        st.altair_chart(hbar(probs, "Phương tiện", "Xác suất", ".0%", order=LABELS, domain=[0, 1]), width="stretch")

# ---------------------------------------------------------------- So sánh mô hình
with tab["So sánh mô hình"]:
    st.subheader("Kết quả trên tập test")
    st.caption(f"Cấu hình: {len(LABELS)} nhãn, {len(FEATURES)} feature; kNN dùng weights=\"{KNN_WEIGHTS}\", k={KNN_K}; "
               "Decision Tree và Random Forest dùng tham số mặc định của demo (chưa tinh chỉnh).")
    st.dataframe(pd.DataFrame(report["metrics"]).T.style.format("{:.3f}", na_rep="—"))
    st.success(f"Mô hình được chọn: **{best}**, vì có CV macro-F1 trên tập train cao nhất. Tập test chỉ dùng để báo cáo.")

    st.subheader("Ma trận nhầm lẫn")
    short = LABELS_SHORT
    cols = st.columns(len(models))
    for c, name in zip(cols, models):
        c.markdown(f"**{name}**")
        c.dataframe(pd.DataFrame(report["confusion"][name], index=[f"Thực tế {s}" for s in short],
                                 columns=[f"Đoán {s}" for s in short]))

    left, right = st.columns(2)
    with left:
        st.subheader("Độ quan trọng của feature (Random Forest)")
        imp = pd.DataFrame([{"Feature": COL_VI[k], "Độ quan trọng": v} for k, v in report["importance"].items()])
        st.altair_chart(hbar(imp, "Feature", "Độ quan trọng", ".2f"), width="stretch")
    with right:
        st.subheader("Nếu lỡ dùng cột lộ nhãn")
        st.dataframe(pd.DataFrame([{"Feature dùng (Random Forest)": k, "Accuracy": v}
                                   for k, v in report["leakage"].items()]).style.format({"Accuracy": "{:.3f}"}),
                     hide_index=True)
        st.caption("Accuracy tăng là 'đẹp giả': khi dự đoán, ta chưa biết thời gian, lý do hay tần suất dùng xe.")

# ---------------------------------------------------------------- Dữ liệu gốc
with tab["Dữ liệu gốc"]:
    c = st.columns(4)
    c[0].metric("Số người trả lời (dòng)", num(eda["shape"][0]))
    c[1].metric("Số cột", eda["shape"][1])
    c[2].metric("Dòng trùng", num(eda["duplicates"]))
    c[3].metric("Thời gian đi lớn nhất", f"{num(eda['travtime_max'])} phút")
    st.subheader("Nguồn dữ liệu")
    st.markdown(DATA_SCOPE + "\n\n" + "\n".join(f"{i}. {c}" for i, c in enumerate(CITATIONS, 1)))

    st.subheader("Mẫu dữ liệu gốc (12 trong 56 cột)")
    st.dataframe(pd.DataFrame(eda["sample"]), hide_index=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Phương tiện trong dữ liệu gốc")
        total = sum(eda["vehic"].values())
        v = pd.DataFrame([{"Phương tiện": k, "Tỉ lệ": n / total, "Số chuyến": n} for k, n in eda["vehic"].items()])
        st.altair_chart(hbar(v, "Phương tiện", "Tỉ lệ", ".1%", tooltip_extra=[alt.Tooltip("Số chuyến:Q", format=",")]),
                        width="stretch")
    with right:
        st.subheader("Giá trị thiếu")
        st.dataframe(pd.DataFrame([{"Cột": k, "Số dòng thiếu": n, "Tỉ lệ": f"{n / eda['shape'][0]:.0%}"}
                                   for k, n in eda["missing"].items()]), hide_index=True,
                     height=fit_height(len(eda["missing"])))  # đủ cao để hiện hết các dòng, không cần cuộn
        st.caption("Thiếu ở đây có nghĩa: `freq_*` trống khi người đó không dùng loại xe ấy; nhóm `*_acc` không được "
                   "hỏi hết. Cả hai nhóm đều không dùng làm feature.")

# ---------------------------------------------------------------- Làm sạch & chọn cột
with tab["Làm sạch & chọn cột"]:
    st.subheader("Các bước làm sạch")
    st.dataframe(pd.DataFrame(report["cleaning"]), hide_index=True)
    st.caption(f"Ngoại lai trong dữ liệu gốc: {num(eda['dist_small'])} chuyến dưới 0,1 km, {num(eda['dist_large'])} "
               f"chuyến trên 50 km, thời gian đi lớn nhất {num(eda['travtime_max'])} phút.")

    left, right = st.columns(2)
    with left:
        st.subheader(f"{len(FEATURES)} feature được chọn")
        st.dataframe(pd.DataFrame(report["features"]).assign(Feature=lambda d: d.Feature.map(COL_VI)), hide_index=True,
                     height=fit_height(len(report["features"])))
    with right:
        st.subheader("Cột không dùng vì lộ nhãn")
        st.dataframe(pd.DataFrame([{"Cột": k, "Lý do": v} for k, v in LEAK.items()]), hide_index=True)
        st.caption("Các cột thái độ, chính sách (`opinion_*`, `alt_*`, `reas_not_*`…) không thuộc bài toán này; "
                   "`alt_*` được dùng riêng ở tab 6.")
    sp = report["split"]
    st.info(f"Sau làm sạch còn {num(report['clean_rows'])} chuyến đi. Chia train/test 80/20 có phân tầng theo nhãn: "
            f"train {num(sp['train'])}, test {num(sp['test'])}.")

# ---------------------------------------------------------------- Khám phá dữ liệu
with tab["Khám phá dữ liệu"]:
    col = st.selectbox("Xem tỉ lệ phương tiện theo", FEATURES, format_func=COL_VI.get)
    ex = pd.DataFrame(report["explore"][col])
    st.altair_chart(stacked(ex, ORDINAL.get(col, OPTIONS[col])), width="stretch")
    with st.expander("Xem bảng số liệu"):
        tbl = ex.pivot(index="giá trị", columns="lớp", values="tỉ lệ").reindex(index=OPTIONS[col], columns=LABELS)
        tbl = tbl.dropna(how="all").rename_axis("Giá trị").reset_index()
        # Cột "Giá trị" đặt rộng cố định để giá trị dài nhất của mọi feature (vd. "Chung cư / nhà tập thể cũ") hiện đủ
        st.dataframe(tbl.style.format("{:.0%}", subset=LABELS), hide_index=True, height=fit_height(len(tbl)),
                     column_config={"Giá trị": st.column_config.TextColumn("Giá trị", width=240)})
    md = pd.DataFrame([{"Phương tiện": k, "Quãng đường trung vị (km)": v} for k, v in report["median_dist"].items()])
    st.caption("Quãng đường trung vị theo phương tiện (đường chim bay): "
               + ", ".join(f"{r['Phương tiện']} {r['Quãng đường trung vị (km)']:.1f} km".replace(".", ",")
                           for r in md.sort_values("Quãng đường trung vị (km)", ascending=False).to_dict("records")))

# ---------------------------------------------------------------- Phương tiện thay thế khi cấm xe máy
with tab["Phương tiện thay thế khi cấm xe máy"]:
    ban = report["ban"]
    st.subheader("Người đang đi xe máy sẽ chuyển sang phương tiện gì nếu nội đô cấm xe máy?")
    alt_df = pd.DataFrame([{"Phương tiện thay thế": k, "Tỉ lệ người chọn": v} for k, v in ban["alt"].items()])
    st.altair_chart(hbar(alt_df, "Phương tiện thay thế", "Tỉ lệ người chọn", ".0%", domain=[0, 1]), width="stretch")
    st.caption(f"Tính trên {num(ban['n_moto'])} người đang đi xe máy. Mỗi người được chọn nhiều phương án, nên tổng "
               "lớn hơn 100%. Đây chỉ là phần mô tả dữ liệu (EDA), không đưa vào mô hình.")

# ---------------------------------------------------------------- nguồn dữ liệu (bắt buộc ghi theo giấy phép CC BY 4.0)
source_html = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2" target="_blank">\1</a>', SOURCE_SHORT)
source_html = source_html.replace("CC BY 4.0", "CC&nbsp;BY&nbsp;4.0")  # không để "4.0" rớt dòng một mình
members = "".join(f"<li>{m}</li>" for m in MEMBERS)
st.markdown(f'''<div class="app-footer">
<div class="col"><b>{COURSE} · {CLASS_NAME} · {GROUP_NAME}</b><br>Thành viên:<ul>{members}</ul></div>
<div class="vline"></div>
<div class="col src">{source_html}</div>
</div>''', unsafe_allow_html=True)

# -*- coding: utf-8 -*-
"""Dựng baocao-dwdm.docx: 2 bìa của baocao-sample.docx (đổi tên đề tài) + mục lục + danh sách bảng/hình/từ viết tắt
+ nội dung (content.py). Chạy 2 lần: lần 1 đo số trang (pages.json), lần 2 điền số trang vào mục lục và danh sách."""
import json, os, re, shutil, sys
from xml.sax.saxutils import escape as E
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C
U, PAGES_F = sys.argv[1], sys.argv[2]
PAGES = json.load(open(PAGES_F, encoding="utf8")) if os.path.exists(PAGES_F) else {}
doc = open(f"{U}/word/document.xml", encoding="utf8").read()
OLD_T = "XÂY DỰNG CƠ SỞ DỮ LIỆU PHÂN TÁN CHO HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ SỬ DỤNG MYSQL GROUP REPLICATION VÀ MONGODB"
NEW_T = "HỆ THỐNG DỰ ĐOÁN LỰA CHỌN PHƯƠNG TIỆN DI CHUYỂN CỦA NGƯỜI DÂN ĐÔ THỊ DỰA VÀO KỸ THUẬT PHÂN LỚP"
txt = lambda p: "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p))

# ---- bìa: đổi tên đề tài
n = 0
for p in re.findall(r"<w:p[ >].*?</w:p>", doc, flags=re.S):
    if txt(p).strip() == OLD_T:
        runs = re.findall(r"<w:r[ >].*?</w:r>", p, flags=re.S)
        rpr = re.search(r"<w:rPr>.*?</w:rPr>", runs[0], flags=re.S)
        newp = p
        for r in runs: newp = newp.replace(r, "", 1)
        newp = newp.replace("</w:p>", f'<w:r>{rpr.group(0) if rpr else ""}<w:t>{E(NEW_T)}</w:t></w:r></w:p>')
        doc = doc.replace(p, newp, 1); n += 1
assert n == 2
toc_title = next(p for p in re.findall(r"<w:p[ >].*?</w:p>", doc, flags=re.S) if txt(p).strip() == "MỤC LỤC" and "TOC2" not in p)
cut = doc.index(toc_title) + len(toc_title); end = doc.index("</w:body>")
final_sect = re.findall(r"<w:sectPr[^>]*>.*?</w:sectPr>", doc[cut:end], flags=re.S)[-1]
head, tail = doc[:cut], doc[end:]

# ---- tiện ích
BM = {}
def bm(t):
    if t not in BM: BM[t] = f"_Toc9{len(BM) + 1:05d}"
    return BM[t]
def bookmarked(t, inner):
    name = bm(t); i = 9000 + list(BM).index(t)
    return f'<w:bookmarkStart w:id="{i}" w:name="{name}"/>{inner}<w:bookmarkEnd w:id="{i}"/>'
def runs(t, extra=""):
    """Chữ có thể chứa **đậm**."""
    out = []
    for k, part in enumerate(re.split(r"\*\*", t)):
        if part: out.append(f'<w:r><w:rPr>{extra}{"<w:b/>" if k % 2 else ""}</w:rPr><w:t xml:space="preserve">{E(part)}</w:t></w:r>')
    return "".join(out)
def para(inner, ppr=""): return f"<w:p><w:pPr>{ppr}</w:pPr>{inner}</w:p>"
BUL = 9001
def h1(t, pb=True): return para(bookmarked(t, runs(t)), f'<w:pStyle w:val="Heading1"/>{"<w:pageBreakBefore/>" if pb else ""}')
def h2(t): return para(bookmarked(t, runs(t, "<w:b/>")), '<w:pStyle w:val="Heading2"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr><w:ind w:left="0" w:firstLine="0"/>')
def h3(t): return para(bookmarked(t, runs(t, "<w:b/><w:i/>")), '<w:pStyle w:val="Heading3"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr><w:spacing w:before="160"/><w:ind w:left="0" w:firstLine="0"/>')
def body(t): return para(runs(t))
def bullet(t): return para(runs(t), f'<w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="{BUL}"/></w:numPr><w:spacing w:before="60"/><w:ind w:left="567" w:hanging="283"/><w:jc w:val="both"/>')
def eqp(t): return para(runs(t, "<w:i/>"), '<w:spacing w:before="80" w:after="80"/><w:ind w:firstLine="0"/><w:jc w:val="center"/>')
def caption(t, before=True):
    return para(bookmarked(t, runs(t)), f'<w:pStyle w:val="Caption"/><w:keepNext w:val="{1 if before else 0}"/><w:spacing w:before="{160 if before else 60}" w:after="{60 if before else 160}"/>')
def cell(t, w, head=False, align="left"):
    shade = '<w:shd w:val="clear" w:color="auto" w:fill="DCEDEA"/>' if head else ""
    return (f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shade}<w:vAlign w:val="center"/></w:tcPr>'
            f'<w:p><w:pPr><w:spacing w:before="40" w:after="40" w:line="264" w:lineRule="auto"/><w:ind w:firstLine="0"/><w:jc w:val="{"center" if head else align}"/></w:pPr>'
            f'{runs(t, ("<w:b/>" if head else "") + "<w:sz w:val=\"23\"/><w:szCs w:val=\"23\"/>")}</w:p></w:tc>')
def tbl(widths, headr, rows):
    def is_num(s): return bool(re.fullmatch(r"[\d.,%()± —–/+\s]+", s)) and any(ch.isdigit() for ch in s) or s == "—"
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    trs = ['<w:tr><w:trPr><w:tblHeader/></w:trPr>' + "".join(cell(h, w, True) for h, w in zip(headr, widths)) + "</w:tr>"]
    for r in rows:
        trs.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>' + "".join(cell(c, w, False, "center" if (i and is_num(c)) else "left") for i, (c, w) in enumerate(zip(r, widths))) + "</w:tr>")
    return (f'<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="{sum(widths)}" w:type="dxa"/><w:jc w:val="center"/>'
            f'<w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr>'
            f'<w:tblGrid>{grid}</w:tblGrid>{"".join(trs)}</w:tbl>')
IMG = []
def image(path, cm):
    k = len(IMG) + 1; rid = f"rIdImgR{k}"; name = f"bc_img{k}.png"
    im = Image.open(path).convert("RGB"); im.save(f"{U}/word/media/{name}")
    w = int(cm * 360000); h = int(w * im.height / im.width)
    max_h = int(19 * 360000)
    if h > max_h: w = int(w * max_h / h); h = max_h
    IMG.append((rid, name))
    return para(f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{w}" cy="{h}"/>'
                f'<wp:docPr id="{500 + k}" name="Hinh {k}"/><wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
                f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
                f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="{500 + k}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>'
                f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
                f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
                f'</a:graphicData></a:graphic></wp:inline></w:drawing></w:r>', '<w:keepNext/><w:spacing w:before="120"/><w:ind w:firstLine="0"/><w:jc w:val="center"/>')
def placeholder(t):
    return para(runs(t, '<w:i/><w:color w:val="5A6B70"/>'),
                '<w:keepNext/><w:pBdr><w:top w:val="dashed" w:sz="6" w:space="20" w:color="8AA5A0"/><w:left w:val="dashed" w:sz="6" w:space="4" w:color="8AA5A0"/>'
                '<w:bottom w:val="dashed" w:sz="6" w:space="20" w:color="8AA5A0"/><w:right w:val="dashed" w:sz="6" w:space="4" w:color="8AA5A0"/></w:pBdr>'
                '<w:spacing w:before="360" w:after="360"/><w:ind w:left="567" w:right="567" w:firstLine="0"/><w:jc w:val="center"/>')
def entry(level, t, style=None):
    style = style or {1: "TOC1", 2: "TOC2", 3: "TOC3"}[level]
    name = bm(t); pg = E(str(PAGES.get(t, "")))
    return (f'<w:p><w:pPr><w:pStyle w:val="{style}"/><w:tabs><w:tab w:val="clear" w:pos="8211"/><w:tab w:val="right" w:leader="dot" w:pos="9062"/></w:tabs></w:pPr>'
            f'<w:hyperlink w:anchor="{name}" w:history="1">{runs(t)}<w:r><w:tab/></w:r>'
            f'<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGEREF {name} \\h </w:instrText></w:r>'
            f'<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>{pg}</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:hyperlink></w:p>')

# ---- danh sách tiêu đề, bảng, hình theo thứ tự
FRONT = ["DANH SÁCH BẢNG", "DANH SÁCH HÌNH", "DANH MỤC TỪ VIẾT TẮT"]
heads = [(1, t) for t in FRONT] + [({"h1": 1, "h2": 2, "h3": 3}[b[0]], b[1]) for b in C.B if b[0] in ("h1", "h2", "h3")]
tables = [b[1] for b in C.B if b[0] == "table"]
figs = [b[1] for b in C.B if b[0] in ("fig", "ph")]

# ---- mục lục (field TOC, nội dung điền sẵn)
out = []
first, rest = heads[0], heads[1:]
e0 = entry(*first)
e0 = e0.replace("</w:pPr>", "</w:pPr><w:r><w:fldChar w:fldCharType=\"begin\"/></w:r><w:r><w:instrText xml:space=\"preserve\"> TOC \\o \"1-3\" \\h \\z \\u </w:instrText></w:r><w:r><w:fldChar w:fldCharType=\"separate\"/></w:r>", 1)
out.append(e0); out += [entry(l, t) for l, t in rest]
out.append('<w:p><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')
# danh sách bảng / hình / từ viết tắt
out.append(h1("DANH SÁCH BẢNG")); out += [entry(2, t, "TOC1") for t in tables]
out.append(h1("DANH SÁCH HÌNH")); out += [entry(2, t, "TOC1") for t in figs]
out.append(h1("DANH MỤC TỪ VIẾT TẮT")); out.append(tbl([2400, 6672], ["Từ viết tắt", "Ý nghĩa"], [[a, b] for a, b in C.ABBR]))

FOOT = "rIdFootPage"
def sect(fmt, start=None):
    s = re.sub(r"<w:footerReference[^>]*/>", "", final_sect)
    s = re.sub(r"(<w:sectPr[^>]*>)", r'\1<w:footerReference w:type="default" r:id="%s"/>' % FOOT, s, count=1)
    return re.sub(r"<w:pgNumType[^>]*/>", f'<w:pgNumType w:fmt="{fmt}"' + (f' w:start="{start}"' if start else "") + "/>", s)
out.append(f'<w:p><w:pPr>{sect("lowerRoman")}</w:pPr></w:p>')

# ---- nội dung
firsth1 = True
for b in C.B:
    k = b[0]
    if k == "h1": out.append(h1(b[1], pb=not firsth1)); firsth1 = False
    elif k == "h2": out.append(h2(b[1]))
    elif k == "h3": out.append(h3(b[1]))
    elif k == "p": out.append(body(b[1]))
    elif k == "ul": out += [bullet(x) for x in b[1]]
    elif k == "eq": out.append(eqp(b[1]))
    elif k == "table": out.append(caption(b[1], True)); out.append(tbl(b[2], b[3], b[4])); out.append(para("", '<w:spacing w:before="0" w:after="0"/>'))
    elif k == "fig": out.append(image(b[2], b[3])); out.append(caption(b[1], False))
    elif k == "ph": out.append(placeholder(b[2])); out.append(caption(b[1], False))
    elif k == "refs": out += [para(runs(r), '<w:ind w:left="567" w:hanging="567"/><w:jc w:val="left"/>') for r in b[1]]
new_doc = head + "".join(out) + sect("decimal", 1) + tail
open(f"{U}/word/document.xml", "w", encoding="utf8").write(new_doc)

# ---- footer số trang, ảnh, đánh dấu đầu dòng
fx = open(f"{U}/word/footer4.xml", encoding="utf8").read()
root = re.match(r"(.*?<w:ftr[^>]*>)", fx, flags=re.S).group(1)
open(f"{U}/word/footer7.xml", "w", encoding="utf8").write(root + '<w:p><w:pPr><w:pStyle w:val="Footer"/><w:jc w:val="center"/></w:pPr><w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>')
rel = open(f"{U}/word/_rels/document.xml.rels", encoding="utf8").read()
add = f'<Relationship Id="{FOOT}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer7.xml"/>'
add += "".join(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{nm}"/>' for rid, nm in IMG)
open(f"{U}/word/_rels/document.xml.rels", "w", encoding="utf8").write(rel.replace("</Relationships>", add + "</Relationships>"))
ct = open(f"{U}/[Content_Types].xml", encoding="utf8").read()
open(f"{U}/[Content_Types].xml", "w", encoding="utf8").write(ct.replace("</Types>", '<Override PartName="/word/footer7.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>'))
nb = open(f"{U}/word/numbering.xml", encoding="utf8").read()
absn = ('<w:abstractNum w:abstractNumId="9001"><w:multiLevelType w:val="singleLevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/>'
        '<w:lvlText w:val="–"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="567" w:hanging="283"/></w:pPr><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr></w:lvl></w:abstractNum>')
i = nb.index("<w:num "); nb = nb[:i] + absn + nb[i:]
open(f"{U}/word/numbering.xml", "w", encoding="utf8").write(nb.replace("</w:numbering>", f'<w:num w:numId="{BUL}"><w:abstractNumId w:val="9001"/></w:num></w:numbering>'))
json.dump({"heads": [t for _, t in heads], "tables": tables, "figs": figs}, open(f"{U}/../items.json", "w", encoding="utf8"), ensure_ascii=False)
print("ok", len(out), len(IMG))

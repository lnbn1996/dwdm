# Nguồn dựng baocao-dwdm.docx (Ghi chú của AI, 15/11/2026)

`baocao-dwdm.docx` được dựng tự động từ các file trong thư mục này, dựa trên số liệu lần chạy 14/11/2026
(5 nhãn, 12 thuộc tính, kNN `weights="distance"` k=5):

| File | Vai trò |
| --- | --- |
| `content.py` | Toàn bộ nội dung báo cáo (văn bản, bảng, chú thích hình). **Các con số được gõ tay từ `demo/artifacts/report.json` và `ai_notes/*.json`.** |
| `figs.py` | Vẽ `fig/h2_1.png`, `h2_2.png`, `h3_1.png`, `h3_2.png`, `h4_1.png` từ `report.json` và `ai_notes/chon_k_ketqua.json` |
| `make2.py` | Ghép 2 trang bìa của `baocao-sample.docx` với mục lục, danh sách bảng/hình/từ viết tắt và nội dung |
| `fig/` | Hình đã vẽ và ảnh chụp tab Dự đoán |

Vẽ lại hình (từ `D:\CaoHoc\DWDM`, cần matplotlib trong .venv):
`.venv\Scripts\python.exe assignment\w1\baocao\_nguon\figs.py assignment\w1\demo\artifacts\report.json assignment\w1\ai_notes\chon_k_ketqua.json assignment\w1\baocao\_nguon\fig`

`make2.py` chạy trên thư mục đã giải nén của `baocao-sample.docx` và cần bước đo số trang bằng LibreOffice;
quy trình này AI chạy trong môi trường riêng, nên trên máy người dùng nên sửa trực tiếp file Word.

**Lưu ý:** khi người dùng đã chỉnh sửa `baocao-dwdm.docx` bằng Word, dựng lại sẽ ghi đè các chỉnh sửa đó.
Khi đó chỉ cập nhật các mục bị ảnh hưởng ngay trong file Word (xem bảng ánh xạ trong `../../AI-LOG.md` và `CLAUDE.md`).

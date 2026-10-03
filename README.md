# VFuho Mini House Review & ASMR Pipeline 🏗️

Hệ thống tự động biên soạn kịch bản, trích xuất phân cảnh, tạo thuyết minh tiếng Việt chuẩn Neural (Edge-TTS), lồng âm thanh ASMR xây dựng và render chuỗi video ngắn (1080x1920, tỷ lệ 9:16) chuẩn TikTok, YouTube Shorts, Facebook Reels.

---

## 📌 Nguồn Dữ Liệu & Đối Tượng
* **Video gốc:** [Facebook Reel VFuho](https://www.facebook.com/reel/912068778140320/)
* **Nội dung:** Toàn cảnh thi công mô hình nhà mini có garage (Bê tông cốt thép, xây gạch thẻ, trát phẳng xi măng, quét sàn ASMR, lợp mái ngói cổ trang).
* **Định dạng xuất:** Chuẩn dọc `1080x1920` (9:16), âm thanh trộn 2 lớp (Lớp nền: ASMR thi công gốc 35% âm lượng; Lớp thoại: Giọng đọc thuyết minh 100% âm lượng).

---

## 🎬 Danh Sách Phân Cảnh & Kịch Bản (Storyboard)

| Tập | Tên Phân Cảnh | Thời Lượng | Mốc Gốc | Điểm Nhấn Hình Ảnh & Lời Thoại |
| :---: | :--- | :---: | :---: | :--- |
| **01** | **Tập 1 - Đổ Móng & Cốt Thép Tí Hon** | ~20s | `00:01` - `00:21` | Đan lồng thép cột trụ mini, đổ móng bê tông kiên cố và gạt phẳng mặt sàn. |
| **02** | **Tập 2 - Xây Gạch Thẻ & Ô Cửa Tròn** | ~21s | `00:33` - `00:54` | Đặt từng viên gạch đỏ mini chuẩn chỉ, ghép ô cửa sổ tròn phong cách Á Đông. |
| **03** | **Tập 3 - Trát Vữa Phẳng & Vệ Sinh ASMR** | ~20s | `01:12` - `01:32` | Miết xi măng láng mịn, dùng chổi rơm mini quét sạch sàn cực kỳ thư giãn. |
| **04** | **Tập 4 - Lợp Ngói Đen & Hoàn Thiện** | ~22s | `01:50` - `02:12` | Lắp khung xà gồ, dán từng dải ngói đen lượn sóng, toàn cảnh biệt thự kèm garage. |
| **Full**| **Highlight - Biệt Thự Mini Trong Mơ** | ~30s | Tổng hợp | Tóm tắt 60 giây tinh hoa xây dựng thu nhỏ với nhịp cắt nhanh, kịch tính. |

---

## 🛠️ Yêu Cầu Môi Trường
* **Python 3.10+**
* **FFmpeg** (hỗ trợ libx264, aac, filter drawtext)
* **Thư viện Python:** `edge-tts`, `pytest`

Cài đặt phụ thuộc:
```bash
pip install edge-tts pytest
```

---

## 🚀 Hướng Dẫn Sử Dụng

### 1. Sinh giọng đọc thuyết minh & Phụ đề
```bash
python3 scripts/generate_voiceover.py
```
Script sẽ tự động kết nối Edge-TTS tiếng Việt (`vi-VN-NamMinhNeural`), tạo các tệp âm thanh `.mp3` và phụ đề `.vtt` tương ứng trong thư mục `output/`.

### 2. Render chuỗi video hoàn chỉnh
```bash
python3 scripts/render_pipeline.py
```
Script sẽ tự động:
1. Cắt từng phân cảnh chính xác từ video gốc.
2. Trộn âm thanh ASMR nguyên bản (35%) với giọng đọc thuyết minh (100%).
3. Thêm banner tiêu đề vàng nổi bật ở góc trên `(y=140)`.
4. Xuất video chất lượng cao 1080x1920 lưu tại `output/*_review.mp4`.

### 3. Chạy kiểm thử tự động
```bash
pytest tests/
```

---

## 📂 Cấu Trúc Dự Án
```text
vfuho-mini-house-review/
├── README.md               # Tài liệu dự án
├── specs/
│   └── storyboard.md       # Bảng phân cảnh chi tiết & lời thoại
├── scripts/
│   ├── generate_voiceover.py # Script sinh TTS tiếng Việt
│   └── render_pipeline.py    # Pipeline cắt ghép và render video
├── tests/
│   └── test_pipeline.py    # Bộ test kiểm tra chất lượng tự động
└── output/                 # Thư mục chứa audio, phụ đề và video hoàn thiện
```

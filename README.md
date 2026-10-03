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

### 2. Render chuỗi video hoàn chỉnh từng tập
```bash
python3 scripts/render_pipeline.py
```
Script sẽ tự động:
1. Cắt từng phân cảnh chính xác từ video gốc.
2. Trộn âm thanh ASMR nguyên bản (35%) với giọng đọc thuyết minh (100%).
3. Xuất video chất lượng cao 1080x1920 lưu tại `output/*_review.mp4`.
4. Tự động đồng bộ bản sao sang `/storage/emulated/0/Movies` và `/storage/emulated/0/Download`.

### 3. Render bản Full Liền Mạch 167s (Clean - Không Chữ Tựa Đề)
```bash
python3 scripts/generate_full_narration.py
python3 scripts/render_full_clean.py
```
Script sẽ tự động:
1. Giữ nguyên 100% video gốc (đầy đủ 167 giây, không cắt ghép đứt đoạn).
2. Xóa bỏ hoàn toàn chữ tựa đề / banner, giữ khung hình sạch đẹp 100%.
3. Trộn âm thanh ASMR thi công (35%) với 5 phân đoạn thuyết minh AI được căn giờ chuẩn xác theo hành động.
4. Tự động sao chép sang `Movies` và `Download` trên điện thoại, đồng thời gửi tín hiệu MediaScanner để xem được ngay trong Thư viện.

### 4. Render bản Master Hoàn Thiện (Full 167s + Thuyết Minh Dày Dặn 10 Phân Đoạn + Xóa Watermark + Phụ Đề Chữ Vàng)
```bash
python3 scripts/generate_dense_narration.py
python3 scripts/render_final_master.py
```
Script sẽ tự động:
1. **Thuyết minh dày dặn & liên tục**: Nâng cấp kịch bản lên 10 phân đoạn liền mạch (~125s thoại / 167s video, bao phủ 75%), giải quyết triệt để tình trạng nói thưa thớt, chỉ để lại các khoảng thở ASMR ngắn 2-3s cực kỳ cuốn hút.
2. **Xóa sạch watermark di chuyển (`VFuho @vfuho`)** trên toàn bộ 6 mốc thời gian bằng thuật toán `delogo`.
3. **Gắn phụ đề tiếng Việt chữ vàng viền đen chuẩn ASS** hiển thị nổi bật, chuẩn từng giây theo 10 phân đoạn thoại.
4. **Hòa trộn âm thanh 2 lớp**: Giọng thuyết minh AI `vi-VN-NamMinhNeural` (100%) và âm thanh ASMR thi công gốc (35%).
5. **Tự động đồng bộ ngay** vào `/storage/emulated/0/Movies` và `/storage/emulated/0/Download`.


### 5. Chạy kiểm thử tự động
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
│   ├── generate_voiceover.py     # Script sinh TTS tiếng Việt từng tập
│   ├── generate_full_narration.py# Script sinh TTS full 5 đoạn
│   ├── render_pipeline.py        # Pipeline cắt ghép 4 tập + highlight
│   ├── render_full_clean.py      # Pipeline render full clean
│   └── render_final_master.py    # Pipeline Master: Xóa watermark + Add phụ đề
├── tests/
│   └── test_pipeline.py    # Bộ test kiểm tra chất lượng tự động (6 tests passed)
└── output/                 # Thư mục chứa audio, phụ đề ASS/SRT và video hoàn thiện
```


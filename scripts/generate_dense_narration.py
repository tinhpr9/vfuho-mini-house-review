#!/usr/bin/env python3
"""
Generate dense continuous narration (10 segments) covering the entire 167s video.
Solves 'sao nói ít vậy' by providing non-stop engaging commentary with natural ASMR breathing room.
"""

import os
import subprocess
import json
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "dense_narration")
os.makedirs(OUTPUT_DIR, exist_ok=True)

SEGMENTS = [
    {
        "id": "dense_part1",
        "text": "Chào mừng anh em quay trở lại với series kiến trúc tí hon! Hôm nay chúng ta sẽ cùng theo dõi trọn vẹn quy trình thi công một căn biệt thự mini có cả gara xe hơi cực kỳ đẳng cấp từ bàn tay vàng của bác thợ phụ hồ này.",
        "target_start": 1.0
    },
    {
        "id": "dense_part2",
        "text": "Bắt đầu ngay từ phần móng nha. Từng thanh thép nhỏ như tăm tre được uốn nắn, đan thành những lồng cột trụ siêu chuẩn chỉ. Sau khi ghép cốp pha gỗ, bác thợ đổ bê tông mác cao rồi cán phẳng lì từng milimet mặt sàn.",
        "target_start": 16.5
    },
    {
        "id": "dense_part3",
        "text": "Khi móng đã đông kết cứng cáp, giờ là lúc những viên gạch thẻ đỏ tí hon lên sàn. Bác thợ đặt từng viên đều tăm tắp, miết mạch vữa chuẩn không cần chỉnh. Cứ một lớp gạch lại thêm một lớp vữa dẻo mịn, nhìn thôi đã thấy mê rồi!",
        "target_start": 33.5
    },
    {
        "id": "dense_part4",
        "text": "Điểm nhấn kiến trúc cực đỉnh ở gian nhà chính là chiếc cửa sổ vòm tròn phong cách cổ điển. Xung quanh được giằng thêm các cột bê tông cốt thép chịu lực, bảo đảm độ kiên cố tuyệt đối cho cả ngôi nhà nhỏ.",
        "target_start": 52.0
    },
    {
        "id": "dense_part5",
        "text": "Không chỉ có gian nhà chính đâu, bác thợ còn cẩn thận mở rộng thêm cả phần garage phụ bên hông nữa. Từng bức tường dần cao lên, các góc vuông được căn ke chính xác tuyệt đối, không một chi tiết nào bị lệch cữ.",
        "target_start": 71.0
    },
    {
        "id": "dense_part6",
        "text": "Và đây rồi, khoảnh khắc trát vữa gây nghiện nhất trên mạng xã hội! Chiếc bay mini lướt thoăn thoắt trên bề mặt tường, từng mảng vữa dẻo được miết phẳng lì, giấu nhẹm đi mọi đường gạch thô ráp.",
        "target_start": 90.0
    },
    {
        "id": "dense_part7",
        "text": "Chưa hết đâu nha, chiếc chổi rơm tí hon quét sạch từng vụn vữa trên sàn nhà, tạo nên một không gian gọn gàng tinh tươm. Xem đến đoạn này cảm giác mọi căng thẳng mệt mỏi đều tan biến hết đúng không các bạn?",
        "target_start": 109.0
    },
    {
        "id": "dense_part8",
        "text": "Bây giờ chuyển sang phần làm mái nè. Khung xà gồ gỗ được dựng lên chắc chắn, sau đó từng dải ngói lượn sóng màu đen mun được gắn so le cẩn thận. Mái ngói đen tuyền nhìn vừa sang trọng lại vừa cổ kính.",
        "target_start": 126.5
    },
    {
        "id": "dense_part9",
        "text": "Bước cuối cùng là khoác lên ngôi nhà lớp sơn trắng tinh khôi. Toàn bộ tường ngoài và gara kết hợp hài hòa, từng đường nét kiến trúc nổi bật rõ rệt dưới ánh sáng.",
        "target_start": 144.5
    },
    {
        "id": "dense_part10",
        "text": "Chỉ từ cát, xi măng và những viên gạch nhỏ xíu, một kiệt tác biệt thự mini hoàn hảo đã ra đời. Anh em chấm cho tay nghề bác thợ này mấy điểm? Đừng quên thả tim và follow nhé!",
        "target_start": 156.5
    }
]

def generate_tts_file(text, out_path, max_retries=5):
    for attempt in range(1, max_retries + 1):
        cmd = ["edge-tts", "--text", text, "--voice", "vi-VN-NamMinhNeural", "--write-media", out_path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
            return True
        print(f"  [Attempt {attempt}] Retrying in 2s...")
        time.sleep(2)
    return False

def get_duration(audio_path):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", audio_path]
    res = subprocess.check_output(cmd)
    return float(json.loads(res)["format"]["duration"])

def main():
    print(f"Generating {len(SEGMENTS)} dense narration segments...")
    manifest = []
    total_speech = 0.0

    current_start = 1.0
    for idx, seg in enumerate(SEGMENTS, 1):
        f_name = f"{seg['id']}.mp3"
        f_path = os.path.join(OUTPUT_DIR, f_name)
        print(f"\n[{idx}/{len(SEGMENTS)}] Generating {seg['id']}...")
        ok = generate_tts_file(seg["text"], f_path)
        if not ok:
            print(f"Failed to generate {seg['id']}")
            return

        dur = get_duration(f_path)
        total_speech += dur

        # Calculate actual start ensuring no overlap
        actual_start = max(seg["target_start"], current_start)
        actual_end = actual_start + dur
        current_start = actual_end + 1.2  # 1.2s breathing room

        entry = {
            "id": seg["id"],
            "file": f_path,
            "text": seg["text"],
            "duration": dur,
            "start": actual_start,
            "end": actual_end,
            "delay_ms": int(actual_start * 1000)
        }
        manifest.append(entry)
        print(f"  ✓ Duration: {dur:.2f}s | Timing: {actual_start:.2f}s -> {actual_end:.2f}s")
        time.sleep(1)

    print(f"\n=== Dense Narration Summary ===")
    print(f"Total Speech Time: {total_speech:.2f}s / 167.13s ({total_speech/167.13*100:.1f}% continuous coverage)")
    print(f"Video End Time: {manifest[-1]['end']:.2f}s")

    manifest_path = os.path.join(OUTPUT_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"Saved manifest to {manifest_path}")

if __name__ == "__main__":
    main()

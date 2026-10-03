#!/usr/bin/env python3
"""
Generate TTS audio voiceover and subtitles for each episode using edge-tts CLI.
"""

import os
import subprocess
import sys

EPISODES = [
    {
        "id": "ep1",
        "title": "Tập 1: Đổ Móng & Khung Thép Tí Hon",
        "start": "00:00:00",
        "duration": "28",
        "text": "Để xây dựng một ngôi nhà bền vững, dù là mô hình mini thì phần móng vẫn là linh hồn quan trọng nhất. Từng cột trụ được đan thép tỉ mỉ, đổ bê tông mác cao và cán phẳng từng milimet. Nhìn bàn tay khéo léo gạt từng bay vữa thế này, bạn có thấy độ mê hoặc của nghệ thuật xây dựng tí hon chưa?",
        "voice": "vi-VN-NamMinhNeural",
        "rate": "+0%",
    },
    {
        "id": "ep2",
        "title": "Tập 2: Đặt Gạch Xây Tường & Ô Cửa Sổ Tròn",
        "start": "00:00:32",
        "duration": "28",
        "text": "Bước sang công đoạn lên tường gạch. Mỗi viên gạch đỏ mini chỉ bằng đầu ngón tay nhưng được đặt thẳng tắp chuẩn dây dọi. Điểm nhấn đặc biệt chính là ô cửa sổ tròn mang phong cách Á Đông cổ điển. Từng đường mạch vữa được miết gọn gàng, tạo nên một kết cấu kiên cố không khác gì công trình thực thụ.",
        "voice": "vi-VN-NamMinhNeural",
        "rate": "+0%",
    },
    {
        "id": "ep3",
        "title": "Tập 3: Nghệ Thuật Trát Vữa & Quét Dọn Siêu Sạch",
        "start": "00:01:12",
        "duration": "28",
        "text": "Công đoạn trát vữa đòi hỏi sự kiên nhẫn tuyệt đối. Từng lớp xi măng được miết phẳng lì, che đi những mạch gạch thô ráp. Và khoảnh khắc thư giãn nhất chính là lúc dùng chiếc chổi rơm tí hon quét sạch từng vụn vữa trên sàn nhà. Cảm giác sạch sẽ và gọn gàng đến từng chi tiết nhỏ nhất.",
        "voice": "vi-VN-NamMinhNeural",
        "rate": "+0%",
    },
    {
        "id": "ep4",
        "title": "Tập 4: Lợp Mái Ngói Đen & Hoàn Thiện Kiệt Tác",
        "start": "00:01:48",
        "duration": "30",
        "text": "Phần mái ngói chính là linh hồn của ngôi nhà. Từng viên ngói đen cổ trang được xếp lớp so le hoàn hảo, chống chịu mọi cơn mưa giả lập. Kết hợp với tường sơn trắng tinh khôi và garage đỗ xe bên cạnh, một biệt thự mini hoàn mỹ đã ra đời. Bạn có muốn sở hữu một không gian sống tí hon như thế này không?",
        "voice": "vi-VN-NamMinhNeural",
        "rate": "+0%",
    },
    {
        "id": "highlight_60s",
        "title": "Bản Highlight 60s: Toàn Cảnh Xây Biệt Thự Mini",
        "start": "00:00:05",
        "duration": "55",
        "text": "Chỉ với 60 giây, đây là hành trình biến xi măng và gạch mini thành một căn biệt thự hoàn mỹ. Từ việc đan lồng thép, đổ móng bê tông kiên cố, cho đến khi từng hàng gạch đỏ mọc lên thẳng tắp. Mỗi động tác miết vữa, quét sàn đều mang lại cảm giác thư giãn tuyệt đối. Và khi mái ngói đen được lợp xong, một kiệt tác kiến trúc tí hon đã chính thức hoàn thiện!",
        "voice": "vi-VN-NamMinhNeural",
        "rate": "+5%",
    }
]

def generate_episode(ep, output_dir):
    audio_path = os.path.join(output_dir, f"{ep['id']}_voice.mp3")
    vtt_path = os.path.join(output_dir, f"{ep['id']}_sub.vtt")

    print(f"Generating TTS for {ep['id']}: {ep['title']}...")
    cmd = [
        "edge-tts",
        "--text", ep["text"],
        "--voice", ep["voice"],
        "--rate", ep["rate"],
        "--write-media", audio_path,
        "--write-subtitles", vtt_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error generating {ep['id']}: {res.stderr}")
        return False
    print(f"  ✓ {audio_path} ({os.path.getsize(audio_path)} bytes)")
    return True

def main():
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
    os.makedirs(output_dir, exist_ok=True)

    success_count = 0
    for ep in EPISODES:
        if generate_episode(ep, output_dir):
            success_count += 1
    print(f"\nGenerated {success_count}/{len(EPISODES)} voiceovers successfully!")

if __name__ == "__main__":
    main()

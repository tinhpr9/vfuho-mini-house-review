#!/usr/bin/env python3
import os
import subprocess

SECTIONS = [
    {
        "id": "full_part1",
        "text": "Chào mừng các bạn đến với quy trình xây dựng trọn gói một căn biệt thự mini có garage cực kỳ đẳng cấp. Bước đầu tiên không thể thiếu là tạo dựng phần nền móng kiên cố. Từng thanh thép tí hon được cắt uốn, đan thành những lồng cột trụ chắc chắn, sau đó đóng cốp pha gỗ và đổ bê tông mác cao, cán phẳng từng milimet mặt sàn.",
        "voice": "vi-VN-NamMinhNeural",
        "delay_ms": 1000  # 1s
    },
    {
        "id": "full_part2",
        "text": "Khi phần móng đã đông kết, từng viên gạch thẻ đỏ mini chỉ bằng đầu ngón tay bắt đầu được xếp lớp thẳng tắp. Từng đường mạch vữa được miết cực kỳ gọn gàng. Điểm nhấn kiến trúc độc đáo ở đây chính là ô cửa sổ vòm tròn mang hơi hướng cổ điển, kết hợp cùng những cột bê tông cốt thép chịu lực vững chãi.",
        "voice": "vi-VN-NamMinhNeural",
        "delay_ms": 33000  # 33s
    },
    {
        "id": "full_part3",
        "text": "Tiếp theo là công đoạn trát vữa xi măng. Bằng chiếc bay phụ hồ mini, người thợ khéo léo miết phẳng từng mảng tường, che đi những vết nối gạch thô ráp. Và khoảnh khắc gây nghiện nhất chính là lúc dùng chiếc chổi rơm tí hon quét sạch từng vụn vữa trên sàn nhà, tạo nên một không gian vô cùng sạch sẽ và ngăn nắp.",
        "voice": "vi-VN-NamMinhNeural",
        "delay_ms": 75000  # 75s
    },
    {
        "id": "full_part4",
        "text": "Bước vào giai đoạn quan trọng nhất: thi công hệ mái. Khung xà gồ được lắp đặt chuẩn xác, sau đó từng dải ngói lượn sóng màu đen tuyền được gắn so le hoàn hảo. Mái ngói đen không chỉ tạo vẻ sang trọng, cổ kính mà còn che chắn trọn vẹn cho ngôi nhà.",
        "voice": "vi-VN-NamMinhNeural",
        "delay_ms": 110000  # 110s
    },
    {
        "id": "full_part5",
        "text": "Cuối cùng, toàn bộ tường ngoài được phủ lớp sơn trắng tinh khôi, kết hợp hài hòa với phần garage mở rộng bên cạnh. Chỉ với xi măng, cát và gạch mini, một kiệt tác kiến trúc thu nhỏ đã chính thức hoàn thiện. Bạn chấm mấy điểm cho công trình tí hon đỉnh cao này?",
        "voice": "vi-VN-NamMinhNeural",
        "delay_ms": 148000  # 148s
    }
]

def main():
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
    os.makedirs(output_dir, exist_ok=True)

    for sec in SECTIONS:
        audio_path = os.path.join(output_dir, f"{sec['id']}.mp3")
        print(f"Generating TTS for {sec['id']}...")
        cmd = [
            "edge-tts",
            "--text", sec["text"],
            "--voice", sec["voice"],
            "--write-media", audio_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  ✓ {audio_path} ({os.path.getsize(audio_path)} bytes)")
        else:
            print(f"  ✗ Error: {res.stderr}")

if __name__ == "__main__":
    main()

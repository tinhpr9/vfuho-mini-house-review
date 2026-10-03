#!/usr/bin/env python3
"""
Render short video clips (1080x1920, 9:16) with mixed ASMR audio and TTS voiceover.
"""

import os
import subprocess
import sys
import json

SOURCE_VIDEO = "/root/vfuho_mini_house.mp4"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

EPISODES = [
    {
        "id": "ep1",
        "title": "TẬP 1 - ĐỔ MÓNG VÀ CỐT THÉP TÍ HON",
        "start": "00:00:01",
        "buffer": 3.0,
        "voice_file": "ep1_voice.mp3"
    },
    {
        "id": "ep2",
        "title": "TẬP 2 - XÂY GẠCH THẺ VÀ Ô CỬA TRÒN",
        "start": "00:00:33",
        "buffer": 3.0,
        "voice_file": "ep2_voice.mp3"
    },
    {
        "id": "ep3",
        "title": "TẬP 3 - TRÁT VỮA PHẲNG VÀ VỆ SINH ASMR",
        "start": "00:01:12",
        "buffer": 3.0,
        "voice_file": "ep3_voice.mp3"
    },
    {
        "id": "ep4",
        "title": "TẬP 4 - LỢP NGÓI ĐEN VÀ HOÀN THIỆN",
        "start": "00:01:50",
        "buffer": 3.0,
        "voice_file": "ep4_voice.mp3"
    },
    {
        "id": "highlight_60s",
        "title": "HIGHLIGHT - BIỆT THỰ MINI TRONG MƠ",
        "start": "00:00:05",
        "buffer": 2.0,
        "voice_file": "highlight_60s_voice.mp3"
    }
]

def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and res.stdout.strip():
        return float(res.stdout.strip())
    return 20.0

def render_episode(ep, output_dir):
    voice_path = os.path.join(output_dir, ep["voice_file"])
    final_video = os.path.join(output_dir, f"{ep['id']}_review.mp4")

    if not os.path.exists(voice_path):
        print(f"Error: Voice file not found: {voice_path}")
        return False

    audio_dur = get_audio_duration(voice_path)
    total_dur = audio_dur + ep.get("buffer", 2.0)

    print(f"\n[Render] Starting {ep['id']}: {ep['title']} (Length: {total_dur:.1f}s)...")

    # Filter complex:
    # 1. Title banner text on top
    # 2. Mix original video sound (volume=0.35) with TTS voice (volume=1.0)
    video_filter = (
        f"drawtext=fontfile={FONT_PATH}:text='{ep['title']}':"
        f"fontcolor=yellow:fontsize=44:box=1:boxcolor=black@0.65:boxborderw=12:"
        f"x=(w-text_w)/2:y=140"
    )

    cmd = [
        "ffmpeg", "-y",
        "-ss", ep["start"],
        "-t", f"{total_dur:.2f}",
        "-i", SOURCE_VIDEO,
        "-i", voice_path,
        "-filter_complex",
        f"[0:v]{video_filter}[v];[0:a]volume=0.35[bg];[1:a]volume=1.0[fg];[bg][fg]amix=inputs=2:duration=first[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "128k",
        "-t", f"{total_dur:.2f}",
        final_video
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error rendering {ep['id']}: {res.stderr[-400:]}")
        return False

    size_mb = os.path.getsize(final_video) / (1024 * 1024)
    print(f"  ✓ Rendered: {final_video} ({size_mb:.2f} MB)")
    sync_to_device_storage(final_video, ep)
    return True

def sync_to_device_storage(final_video, ep):
    import shutil
    targets = ["/storage/emulated/0/Movies", "/storage/emulated/0/Download"]
    name_map = {
        "ep1": "VFuho_Tap1_Do_Mong_Cot_Thep_Mini.mp4",
        "ep2": "VFuho_Tap2_Xay_Gach_The_O_Cua_Tron.mp4",
        "ep3": "VFuho_Tap3_Trat_Vua_Phang_Ve_Sinh_ASMR.mp4",
        "ep4": "VFuho_Tap4_Lop_Ngoi_Den_Hoan_Thien.mp4",
        "highlight_60s": "VFuho_Highlight_Biet_Thu_Mini_Trong_Mo.mp4",
    }
    clean_name = name_map.get(ep["id"], os.path.basename(final_video))
    for target in targets:
        if os.path.isdir(target):
            dest = os.path.join(target, clean_name)
            try:
                shutil.copyfile(final_video, dest)
                print(f"  -> Synced to: {dest}")
            except Exception:
                pass

def main():
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
    os.makedirs(output_dir, exist_ok=True)

    rendered = 0
    for ep in EPISODES:
        if render_episode(ep, output_dir):
            rendered += 1

    print(f"\nAll {rendered}/{len(EPISODES)} videos rendered successfully!")

if __name__ == "__main__":
    main()

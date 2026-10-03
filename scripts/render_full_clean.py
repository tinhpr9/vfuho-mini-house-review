#!/usr/bin/env python3
"""
Render full continuous video (167s) with mixed ASMR + full Vietnamese narration.
Completely clean: NO title banner, NO episode overlay text.
Automatically syncs to /storage/emulated/0/Movies and /storage/emulated/0/Download.
"""

import os
import subprocess
import shutil
import sys

SOURCE_VIDEO = "/root/vfuho_mini_house.mp4"
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
FINAL_NAME = "VFuho_Mini_House_Full_Clean.mp4"
FINAL_PATH = os.path.join(OUTPUT_DIR, FINAL_NAME)

AUDIO_PARTS = [
    {"file": "full_part1.mp3", "delay_ms": 1000},
    {"file": "full_part2.mp3", "delay_ms": 33000},
    {"file": "full_part3.mp3", "delay_ms": 75000},
    {"file": "full_part4.mp3", "delay_ms": 110000},
    {"file": "full_part5.mp3", "delay_ms": 148000},
]

def check_audios():
    for p in AUDIO_PARTS:
        path = os.path.join(OUTPUT_DIR, p["file"])
        if not os.path.exists(path) or os.path.getsize(path) < 1000:
            print(f"Missing or incomplete audio: {path}")
            return False
    return True

def sync_to_storage():
    targets = [
        "/storage/emulated/0/Movies",
        "/storage/emulated/0/Download"
    ]
    for target in targets:
        if os.path.isdir(target):
            dest = os.path.join(target, FINAL_NAME)
            try:
                shutil.copyfile(FINAL_PATH, dest)
                print(f"  ✓ Copied to: {dest}")
                # Trigger media scanner
                subprocess.run(
                    ["su", "-c", f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{dest}"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
            except Exception as e:
                print(f"  ✗ Failed to copy to {target}: {e}")

def main():
    if not check_audios():
        print("Error: Audio parts not ready. Run generate_full_narration.py first.")
        sys.exit(1)

    print(f"[Render Full Clean] Starting render of {FINAL_NAME} (Full 167s, NO banners)...")

    # Inputs:
    # 0: video
    # 1..5: audio parts
    cmd = ["ffmpeg", "-y", "-i", SOURCE_VIDEO]
    for p in AUDIO_PARTS:
        cmd.extend(["-i", os.path.join(OUTPUT_DIR, p["file"])])

    # Filter complex
    filter_parts = []
    amix_inputs = []
    for idx, p in enumerate(AUDIO_PARTS, start=1):
        filter_parts.append(f"[{idx}:a]adelay={p['delay_ms']}|{p['delay_ms']}[a{idx}]")
        amix_inputs.append(f"[a{idx}]")

    amix_str = "".join(amix_inputs)
    filter_parts.append(f"{amix_str}amix=inputs=5:duration=longest:normalize=0[narration]")
    filter_parts.append("[0:a]volume=0.35[bg]")
    filter_parts.append("[bg][narration]amix=inputs=2:duration=first:normalize=0[aout]")

    full_filter = ";".join(filter_parts)

    cmd.extend([
        "-filter_complex", full_filter,
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        FINAL_PATH
    ])

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error rendering: {res.stderr[-500:]}")
        sys.exit(1)

    size_mb = os.path.getsize(FINAL_PATH) / (1024 * 1024)
    print(f"\n✓ Successfully rendered {FINAL_NAME} ({size_mb:.2f} MB)")

    print("\n[Storage Sync] Copying to device storage...")
    sync_to_storage()
    print("Done!")

if __name__ == "__main__":
    main()

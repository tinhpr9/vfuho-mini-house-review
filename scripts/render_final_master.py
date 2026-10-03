#!/usr/bin/env python3
"""
Render full continuous video (167s) with:
1. Watermark erased via dynamic time-gated delogo filter.
2. Synchronized Vietnamese subtitles (ASS format with styled yellow text and black border).
3. Full continuous Vietnamese narration (vi-VN-NamMinhNeural) mixed over 35% original ASMR sound.
4. Clean frame: NO title banner, NO episode overlay text.
5. Automatically syncs to /storage/emulated/0/Movies and /storage/emulated/0/Download.
"""

import os
import subprocess
import shutil
import sys
import time

SOURCE_VIDEO = "/root/vfuho_mini_house.mp4"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
SUBTITLE_FILE = os.path.join(OUTPUT_DIR, "vfuho_subtitles.ass")
FINAL_NAME = "VFuho_Full_Master_Sub_NoWatermark.mp4"
FINAL_PATH = os.path.join(OUTPUT_DIR, FINAL_NAME)

AUDIO_PARTS = [
    {"file": "dense_narration/dense_part1.mp3", "delay_ms": 1000},
    {"file": "dense_narration/dense_part2.mp3", "delay_ms": 16500},
    {"file": "dense_narration/dense_part3.mp3", "delay_ms": 33500},
    {"file": "dense_narration/dense_part4.mp3", "delay_ms": 52000},
    {"file": "dense_narration/dense_part5.mp3", "delay_ms": 71000},
    {"file": "dense_narration/dense_part6.mp3", "delay_ms": 90000},
    {"file": "dense_narration/dense_part7.mp3", "delay_ms": 109000},
    {"file": "dense_narration/dense_part8.mp3", "delay_ms": 126500},
    {"file": "dense_narration/dense_part9.mp3", "delay_ms": 144500},
    {"file": "dense_narration/dense_part10.mp3", "delay_ms": 155200},
]


# Watermark delogo intervals identified via visual and OCR scan
DELOGO_INTERVALS = [
    {"start": 0, "end": 30, "x": 540, "y": 1620, "w": 200, "h": 75},
    {"start": 30, "end": 55, "x": 350, "y": 290, "w": 180, "h": 70},
    {"start": 55, "end": 85, "x": 880, "y": 550, "w": 180, "h": 70},
    {"start": 85, "end": 120, "x": 280, "y": 1700, "w": 180, "h": 75},
    {"start": 120, "end": 145, "x": 580, "y": 310, "w": 180, "h": 70},
    {"start": 145, "end": 167.5, "x": 360, "y": 1200, "w": 180, "h": 75},
]

def check_prerequisites():
    if not os.path.exists(SOURCE_VIDEO):
        print(f"Error: Source video not found: {SOURCE_VIDEO}")
        return False
    if not os.path.exists(SUBTITLE_FILE):
        print(f"Error: Subtitle file not found: {SUBTITLE_FILE}")
        return False
    for p in AUDIO_PARTS:
        path = os.path.join(OUTPUT_DIR, p["file"])
        if not os.path.exists(path) or os.path.getsize(path) < 1000:
            print(f"Error: Missing audio part: {path}")
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
                print(f"  ✓ Copied to: {dest} ({os.path.getsize(dest)} bytes)")
                try:
                    subprocess.run(
                        ["su", "-c", f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{dest}"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5
                    )
                except Exception:
                    pass

            except Exception as e:
                print(f"  ✗ Failed to copy to {target}: {e}")

def main():
    if not check_prerequisites():
        sys.exit(1)

    print(f"=== Rendering Final Master: {FINAL_NAME} ===")
    print("Features:")
    print("  - Watermark removal: 6 intervals with delogo filter")
    print(f"  - Subtitles: {SUBTITLE_FILE}")
    print("  - Audio: 5 narration segments mixed with 35% original ASMR")
    print("  - Resolution: 1080x1920 Full HD vertical")

    # Construct FFmpeg command
    cmd = ["ffmpeg", "-y", "-i", SOURCE_VIDEO]
    for p in AUDIO_PARTS:
        cmd.extend(["-i", os.path.join(OUTPUT_DIR, p["file"])])

    # Video filters: delogo sequence + ASS subtitle burning
    v_filters = []
    for d in DELOGO_INTERVALS:
        v_filters.append(
            f"delogo=x={d['x']}:y={d['y']}:w={d['w']}:h={d['h']}:enable='between(t,{d['start']},{d['end']})'"
        )
    v_filters.append(f"ass={SUBTITLE_FILE}")
    v_filter_str = ",".join(v_filters) + "[vout]"

    # Audio filters
    a_filters = []
    amix_inputs = []
    for idx, p in enumerate(AUDIO_PARTS, start=1):
        a_filters.append(f"[{idx}:a]adelay={p['delay_ms']}|{p['delay_ms']}[a{idx}]")
        amix_inputs.append(f"[a{idx}]")

    amix_str = "".join(amix_inputs)
    a_filters.append(f"{amix_str}amix=inputs={len(AUDIO_PARTS)}:duration=longest:normalize=0[narration]")
    a_filters.append("[0:a]volume=0.35[bg]")
    a_filters.append("[bg][narration]amix=inputs=2:duration=first:normalize=0[aout]")
    a_filter_str = ";".join(a_filters)

    full_filter = f"[0:v]{v_filter_str};{a_filter_str}"

    cmd.extend([
        "-filter_complex", full_filter,
        "-map", "[vout]",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        FINAL_PATH
    ])

    print("\nExecuting FFmpeg command...")
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Rendering failed!")
        print(res.stderr[-1000:])
        sys.exit(1)

    elapsed = time.time() - t0
    size_mb = os.path.getsize(FINAL_PATH) / (1024 * 1024)
    print(f"\n✓ Master video successfully rendered in {elapsed:.1f}s!")
    print(f"  File: {FINAL_PATH} ({size_mb:.2f} MB)")

    print("\n[Storage Sync] Copying to device storage...")
    sync_to_storage()
    print("Done!")

if __name__ == "__main__":
    main()

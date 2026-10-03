import os
import subprocess
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SPECS_DIR = os.path.join(ROOT_DIR, "specs")
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")

def test_storyboard_spec_exists():
    storyboard_path = os.path.join(SPECS_DIR, "storyboard.md")
    assert os.path.isfile(storyboard_path), "storyboard.md must exist in specs/"
    with open(storyboard_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Tập 1" in content
    assert "Tập 2" in content
    assert "Tập 3" in content
    assert "Tập 4" in content
    assert "Highlight" in content

def test_scripts_exist():
    gen_script = os.path.join(SCRIPTS_DIR, "generate_voiceover.py")
    render_script = os.path.join(SCRIPTS_DIR, "render_pipeline.py")
    assert os.path.isfile(gen_script), "generate_voiceover.py must exist"
    assert os.path.isfile(render_script), "render_pipeline.py must exist"

def test_audio_assets_generated():
    expected_audios = ["ep1_voice.mp3", "ep2_voice.mp3", "ep3_voice.mp3", "ep4_voice.mp3", "highlight_60s_voice.mp3"]
    for audio_name in expected_audios:
        path = os.path.join(OUTPUT_DIR, audio_name)
        assert os.path.isfile(path), f"Audio {audio_name} must exist"
        assert os.path.getsize(path) > 1000, f"Audio {audio_name} must not be empty"

def test_audio_duration_valid():
    ep1_path = os.path.join(OUTPUT_DIR, "ep1_voice.mp3")
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        ep1_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    duration = float(res.stdout.strip())
    assert 10.0 <= duration <= 40.0, f"Duration {duration}s must be between 10s and 40s"

def test_full_clean_scripts_and_assets():
    full_gen = os.path.join(SCRIPTS_DIR, "generate_full_narration.py")
    full_render = os.path.join(SCRIPTS_DIR, "render_full_clean.py")
    assert os.path.isfile(full_gen), "generate_full_narration.py must exist"
    assert os.path.isfile(full_render), "render_full_clean.py must exist"
    for i in range(1, 6):
        path = os.path.join(OUTPUT_DIR, f"full_part{i}.mp3")
        assert os.path.isfile(path), f"full_part{i}.mp3 must exist"
        assert os.path.getsize(path) > 1000

def test_final_master_video_and_subtitles():
    master_script = os.path.join(SCRIPTS_DIR, "render_final_master.py")
    sub_file = os.path.join(OUTPUT_DIR, "vfuho_subtitles.ass")
    master_video = os.path.join(OUTPUT_DIR, "VFuho_Full_Master_Sub_NoWatermark.mp4")

    assert os.path.isfile(master_script), "render_final_master.py must exist"
    assert os.path.isfile(sub_file), "vfuho_subtitles.ass must exist"
    assert os.path.isfile(master_video), "Master video must exist"
    assert os.path.getsize(master_video) > 50 * 1024 * 1024, "Master video must be > 50MB"

    # Verify duration
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        master_video
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    duration = float(res.stdout.strip())
    assert 166.0 <= duration <= 168.0, f"Master video duration {duration}s must be ~167s"

    # Verify device storage sync
    movies_target = "/storage/emulated/0/Movies/VFuho_Full_Master_Sub_NoWatermark.mp4"
    download_target = "/storage/emulated/0/Download/VFuho_Full_Master_Sub_NoWatermark.mp4"
    if os.path.isdir("/storage/emulated/0/Movies"):
        assert os.path.isfile(movies_target), "Video must be synced to /storage/emulated/0/Movies"
    if os.path.isdir("/storage/emulated/0/Download"):
        assert os.path.isfile(download_target), "Video must be synced to /storage/emulated/0/Download"



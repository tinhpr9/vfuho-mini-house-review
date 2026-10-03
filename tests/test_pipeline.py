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

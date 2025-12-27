from pathlib import Path
import subprocess

def download_youtube_audio(youtube_url: str) -> Path:
    output_dir = Path("/media/youtube_audios")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "%(id)s.%(ext)s"
    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "wav",
        "--audio-quality", "0",
        "-o", str(output_path),
        youtube_url,
    ]
    subprocess.run(command, check=True)
    audio_files = list(output_dir.glob("*.wav"))
    return audio_files[-1] 
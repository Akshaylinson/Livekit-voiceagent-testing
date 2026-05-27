 TTS setup is using this base URL:
https://voices.codelessai.in
So if you implement the same TTS flow in another project:
Base URL: https://voices.codelessai.in
Create TTS job API URL: https://voices.codelessai.in/v1/tts
Check status API URL: https://voices.codelessai.in/tts/status/{job_id}
Download audio API URL: https://voices.codelessai.in/v1/audio/{job_id}
List voices API URL: https://voices.codelessai.in/v1/voices
The current project sends the API key in this header:
X-API-Key: your_internal_codevoice_key


A matching Python snippet would be:
import time
import requests

TTS_BASE_URL = "https://voices.codelessai.in"
TTS_API_KEY = "your_internal_codevoice_key"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": TTS_API_KEY,
}

text = "Hello, this is a sample text to speech conversion."
voice = "Ryan"

# 1. Create TTS job
resp = requests.post(
    f"{TTS_BASE_URL}/v1/tts",
    headers=headers,
    json={"text": text, "voice": voice},
)
resp.raise_for_status()
job_id = resp.json()["job_id"]

# 2. Poll status
for _ in range(60):
    status_resp = requests.get(
        f"{TTS_BASE_URL}/tts/status/{job_id}",
        headers={"X-API-Key": TTS_API_KEY},
    )
    status_resp.raise_for_status()
    data = status_resp.json()

    if data.get("status") == "completed":
        audio_format = data.get("audio_format", "mp3").lower()

        # 3. Download audio
        audio_resp = requests.get(
            f"{TTS_BASE_URL}/v1/audio/{job_id}",
            headers={"X-API-Key": TTS_API_KEY},
        )
        audio_resp.raise_for_status()

        ext = "wav" if audio_format == "wav" else "mp3"
        with open(f"output.{ext}", "wb") as f:
            f.write(audio_resp.content)

        print("Audio saved successfully.")
        break

    if data.get("status") == "failed":
        raise Exception(data.get("error", "TTS job failed."))

    time.sleep(15)
else:
    raise TimeoutError("TTS generation timed out.")


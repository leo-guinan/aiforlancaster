#!/usr/bin/env python3
"""
Compose Bottega Bodega ballad music via ElevenLabs Music API.
Requires ELEVENLABS_API_KEY environment variable.
"""
import os, json, urllib.request, time, sys

api_key = os.environ.get('ELEVENLABS_API_KEY')
if not api_key:
    print("ERROR: ELEVENLABS_API_KEY not set", file=sys.stderr)
    sys.exit(1)

prompt = 'A slow, melancholy indie folk ballad. Instrumentation: acoustic guitar fingerpicking, warm ambient room tone, light piano accents. The mood is slow human connection in a fast world, physical artifacts as antidote to digital, mall as relic, cat as witness. The song should feel intimate, human, slightly worn-in — like a recording made in a quiet room after hours. No drums, no electronic elements. Duration: 180 seconds.'
output_path = '/Users/leoguinan/clawd/local-ai-business/bodega-ballad-bottega-bodega-blues.mp3'

payload = json.dumps({"prompt": prompt, "duration": 180, "format": "mp3"}).encode()
req = urllib.request.Request(
    "https://api.elevenlabs.io/v1/music/generate",
    data=payload,
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "xi-api-key": api_key,
    },
    method="POST"
)

for attempt in range(3):
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            if resp.status == 200:
                audio = resp.read()
                Path(output_path).write_bytes(audio)
                print(f"✓ Music saved: {output_path} ({len(audio)/1024/1024:.2f} MB)")
                sys.exit(0)
            else:
                print(f"✗ HTTP {resp.status}: {resp.read().decode()[:200]}", file=sys.stderr)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"✗ Attempt {attempt+1} failed: {e.code} — {body[:200]}", file=sys.stderr)
        if e.code == 429:
            time.sleep(5 * (attempt + 1))
        else:
            break
    except Exception as e:
        print(f"✗ Attempt {attempt+1} error: {e}", file=sys.stderr)
        time.sleep(2)

sys.exit(1)

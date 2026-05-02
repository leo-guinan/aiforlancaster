# Bottega Bodega Ballad — Production Summary

Title: Bottega Bodega Blues
Character: Marvin the Bodega Cat
Structure: verse1 → chorus → verse2 → chorus → bridge → chorus → outro

## Files Generated
- Lyrics: bodega-ballad-lyrics.json
- Vocals: bodega-ballad-bottega-bodega-blues-vocals.mp3
- Instrumental: bodega-ballad-bottega-bodega-blues.mp3 (ambient bed — pink noise + lowpass)
- Full Mix: bodega-ballad-bottega-bodega-blues-full.mp3

## Vocal Generation
Tool: espeak (fallback, local TTS)
Voice: default system voice (synthetic, weary — fits Marvin's cat voice)
Length: ~2 minutes of spoken word

## Instrumental Generation
Primary API: ElevenLabs Music API (requires music_generation permission)
  Prompt: "A slow, melancholy indie folk ballad. Instrumentation: acoustic guitar fingerpicking, warm ambient room tone, light pian..."
  Current key status: missing music_generation permission → fallback used.

Fallback: ffmpeg-generated ambient bed
  - Pink noise (room tone / CRT hum)
  - Low-pass filtered at 300Hz
  - Volume -20dB (background only)
  - Duration: 180s

## Mix
ffmpeg amix: instrumental (50%) + vocals (100%)
Output: 192kbps MP3, ~4.1 MB

## To Upgrade to Real Instrumental
When ElevenLabs Music API access is available, run:
  ELEVENLABS_API_KEY="your-key" python3 compose_bodega_ballad.py

Or use the curl command in compose-bodega-ballad.sh with a key that has music_generation scope.

## To Improve Vocals
Replace espeak fallback with ElevenLabs TTS:
  - Voice: "onyx" (voice_id: zB8NCYFrwGRO5SDepMeA) or a custom Marvin voice
  - Settings: stability=0.45, similarity_boost=0.75, style=0.15
  - The pipeline skill will auto-upgrade when TTS API is accessible.

## Files in Repository
- bodega-ballad-lyrics.json      (full structured lyrics)
- bodega-ballad-lyrics.txt       (plain text for reference)
- compose_bodega_ballad.py       (music generation script)
- compose-bodega-ballad.sh       (bash wrapper)
- ballad-composition-pipeline skill (/.hermes/skills/creative/)

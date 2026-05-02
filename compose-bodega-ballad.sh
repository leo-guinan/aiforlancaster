#!/bin/bash
export ELEVENLABS_API_KEY="${ELEVENLABS_API_KEY:?Set it first}"
curl -X POST "https://api.elevenlabs.io/v1/music/generate" \
  -H "Authorization: Bearer $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -d '{"prompt": "A slow, melancholy indie folk ballad. Instrumentation: acoustic guitar fingerpicking, warm ambient room tone, light piano accents. The mood is slow human connection in a fast world, physical artifacts as antidote to digital, mall as relic, cat as witness. The song should feel intimate, human, slightly worn-in \u2014 like a recording made in a quiet room after hours. No drums, no electronic elements. Duration: 180 seconds.", "duration": 180, "format": "mp3"}' \
  -o /Users/leoguinan/clawd/local-ai-business/bodega-ballad-bottega-bodega-blues.mp3
echo "Saved to /Users/leoguinan/clawd/local-ai-business/bodega-ballad-bottega-bodega-blues.mp3"

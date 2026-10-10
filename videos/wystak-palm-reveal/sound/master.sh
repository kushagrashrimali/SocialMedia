#!/usr/bin/env bash
# Encode the rendered frames with the sound, master the audio to -14 LUFS integrated (true peak -1.5 dBTP, two-pass
# loudnorm) and write the delivery file (H.264, 1080x1080, 30 fps, AAC 256k).
# usage (from videos/wystak-palm-reveal): bash sound/master.sh ../../wystak/instagram/reels/finals/wystak-palm-reveal.mp4
set -euo pipefail
out="$1"
raw=renders/wystak-palm-reveal-raw.mp4
ffmpeg -hide_banner -loglevel error -y -framerate 30 -i renders/frames/f_%04d.png -i renders/sound.wav \
  -map 0:v -map 1:a -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -c:a pcm_s16le -t 10 renders/raw.mov
stats=$(ffmpeg -hide_banner -nostats -i renders/raw.mov -vn -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { echo "$stats" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
ffmpeg -hide_banner -loglevel error -y -i renders/raw.mov -map 0:v -map 0:a -c:v libx264 -preset slow -crf 18 -maxrate 12M -bufsize 24M \
  -profile:v high -pix_fmt yuv420p \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true,aresample=48000" \
  -c:a aac -b:a 256k -t 10 -movflags +faststart "$out"
ffmpeg -hide_banner -nostats -i "$out" -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary | grep -E "I:|Peak:"

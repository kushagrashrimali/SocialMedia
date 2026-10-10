#!/usr/bin/env bash
# Master the rendered reel's audio to -14 LUFS integrated (true peak -1.5 dBTP) with a two-pass
# ffmpeg loudnorm, re-encode the video to an upload-friendly H.264 (~6 Mbps), and write the delivery file.
# usage (from the project folder): bash sound/master.sh renders/wystak-iphone-reel.mp4 ../../wystak/instagram/reels/finals/wystak-iphone-reel.mp4
set -euo pipefail
in="$1"; out="$2"
stats=$(ffmpeg -hide_banner -nostats -i "$in" -vn -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { echo "$stats" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
ffmpeg -hide_banner -loglevel error -y -i "$in" -map 0:v -map 0:a -c:v libx264 -preset slow -crf 20 -maxrate 9M -bufsize 18M -profile:v high -pix_fmt yuv420p \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true,aresample=48000" \
  -c:a aac -b:a 256k -t "${DUR:-30.0}" -movflags +faststart "$out"
ffmpeg -hide_banner -nostats -i "$out" -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary | grep -E "I:|Peak:"

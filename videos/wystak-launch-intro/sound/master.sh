#!/usr/bin/env bash
# Master the 4K render's audio to -14 LUFS (true peak -1.5 dBTP, two-pass loudnorm) and write two deliveries:
#   <out>/wystak-launch-intro-4k.mp4     2160x3840 master (H.264 high, CRF 14)
#   <out>/wystak-launch-intro-1080.mp4   1080x1920 for Instagram upload (Lanczos downscale, CRF 16)
# usage (from the project folder): bash sound/master.sh renders/wystak-launch-intro-4k.mp4 ../../wystak/launch-intro
set -euo pipefail
in="$1"; out="$2"; mkdir -p "$out"
stats=$(ffmpeg -hide_banner -nostats -i "$in" -vn -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { echo "$stats" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
AF="loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true,aresample=48000"
ffmpeg -hide_banner -loglevel error -y -i "$in" -map 0:v -map 0:a -c:v libx264 -preset slow -crf 14 -profile:v high -pix_fmt yuv420p -tune film \
  -af "$AF" -c:a aac -b:a 320k -movflags +faststart "$out/wystak-launch-intro-4k.mp4"
ffmpeg -hide_banner -loglevel error -y -i "$in" -map 0:v -map 0:a -vf "scale=1080:1920:flags=lanczos" -c:v libx264 -preset slow -crf 16 -maxrate 14M -bufsize 28M \
  -profile:v high -pix_fmt yuv420p -tune film -af "$AF" -c:a aac -b:a 256k -movflags +faststart "$out/wystak-launch-intro-1080.mp4"
for f in "$out"/wystak-launch-intro-4k.mp4 "$out"/wystak-launch-intro-1080.mp4; do
  echo "$f"; ffprobe -v error -show_entries stream=width,height:format=duration,size -of csv=p=0 "$f" | tr '\n' ' '; echo
  ffmpeg -hide_banner -nostats -i "$f" -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary | grep -E "I:|Peak:"
done

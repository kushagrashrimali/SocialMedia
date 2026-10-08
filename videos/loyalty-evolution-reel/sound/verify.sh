#!/usr/bin/env bash
# Verify a delivered reel: format, duration, loudness, and a contact sheet of frames pulled from the MP4 itself.
# usage: bash sound/verify.sh ../../wystak/loyalty-evolution-reel.mp4 /path/to/out-dir
set -euo pipefail
mp4="$1"; out="$2"; mkdir -p "$out"
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,sample_rate,channels -of default=nw=1 "$mp4"
ffmpeg -hide_banner -nostats -i "$mp4" -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary | grep -E "I:|LRA:|Peak:"
times="0.5 1.3 2.2 3.6 5.0 6.0 7.0 8.2 10.2 11.8 12.9 14.2 16.5 19.5 22.6 23.6 26.0 29.0 29.9 30.5 31.2 32.0 32.8 33.6 35.0 36.4 37.0 38.4 39.8 42.0 43.6 44.6 45.5 46.0 46.8 47.4 48.0 49.0 50.0 50.9"
i=0; for t in $times; do ffmpeg -hide_banner -loglevel error -y -ss "$t" -i "$mp4" -frames:v 1 -vf "scale=216:384,drawtext=text='$t':x=6:y=6:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6" "$out/$(printf %03d $i).png"; i=$((i+1)); done
ffmpeg -hide_banner -loglevel error -y -framerate 1 -i "$out/%03d.png" -vf "tile=10x4" -frames:v 1 "$out/delivered-sheet.jpg"
echo "$out/delivered-sheet.jpg"

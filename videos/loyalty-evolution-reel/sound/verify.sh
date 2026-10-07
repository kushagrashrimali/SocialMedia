#!/usr/bin/env bash
# Verify a delivered reel: format, duration, loudness, and a contact sheet of frames pulled from the MP4 itself.
# usage: bash sound/verify.sh ../../wystak/loyalty-evolution-reel.mp4 /path/to/out-dir
set -euo pipefail
mp4="$1"; out="$2"; mkdir -p "$out"
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,sample_rate,channels -of default=nw=1 "$mp4"
ffmpeg -hide_banner -nostats -i "$mp4" -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary | grep -E "I:|LRA:|Peak:"
times="0.6 1.8 3.2 3.9 4.9 6.0 7.9 9.6 10.6 11.8 12.9 14.3 15.6 16.8 17.6 19.2 20.9 22.0 22.9 23.7 24.6 25.6 26.3 27.8 29.2 30.4 32.9 34.4 35.7 36.7 38.2 39.2 40.4 41.8 42.9 44.4 46.3 48.4 51.2"
i=0; for t in $times; do ffmpeg -hide_banner -loglevel error -y -ss "$t" -i "$mp4" -frames:v 1 -vf "scale=216:384,drawtext=text='$t':x=6:y=6:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6" "$out/$(printf %03d $i).png"; i=$((i+1)); done
ffmpeg -hide_banner -loglevel error -y -framerate 1 -i "$out/%03d.png" -vf "tile=10x4" -frames:v 1 "$out/delivered-sheet.jpg"
echo "$out/delivered-sheet.jpg"

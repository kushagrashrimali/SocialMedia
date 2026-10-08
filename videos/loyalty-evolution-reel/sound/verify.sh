#!/usr/bin/env bash
# Verify a delivered reel: format, duration, loudness, and a contact sheet of frames pulled from the MP4 itself.
# usage: bash sound/verify.sh ../../wystak/loyalty-evolution-reel.mp4 /path/to/out-dir
set -euo pipefail
mp4="$1"; out="$2"; mkdir -p "$out"
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,sample_rate,channels -of default=nw=1 "$mp4"
ffmpeg -hide_banner -nostats -i "$mp4" -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary | grep -E "I:|LRA:|Peak:"
times="0.5 1.5 2.8 4.0 5.5 7.5 9.5 11.5 13.0 14.8 16.5 17.8 19.5 21.5 23.0 24.3 25.2 25.8 26.4 26.9 27.4 28.0 28.8 29.6 30.4 31.4 32.6 33.6 34.6 35.4 36.4 37.2 37.8 38.6 39.6"
i=0; for t in $times; do ffmpeg -hide_banner -loglevel error -y -ss "$t" -i "$mp4" -frames:v 1 -vf "scale=216:384,drawtext=text='$t':x=6:y=6:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6" "$out/$(printf %03d $i).png"; i=$((i+1)); done
ffmpeg -hide_banner -loglevel error -y -framerate 1 -i "$out/%03d.png" -vf "tile=10x4" -frames:v 1 "$out/delivered-sheet.jpg"
echo "$out/delivered-sheet.jpg"

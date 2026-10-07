#!/usr/bin/env bash
# Verify a delivered reel: format, duration, loudness, and a contact sheet of frames pulled from the MP4 itself.
# usage: bash sound/verify.sh ../../wystak/loyalty-evolution-reel.mp4 /path/to/out-dir
set -euo pipefail
mp4="$1"; out="$2"; mkdir -p "$out"
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,sample_rate,channels -of default=nw=1 "$mp4"
ffmpeg -hide_banner -nostats -i "$mp4" -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary | grep -E "I:|LRA:|Peak:"
times="0.5 1.6 3.4 4.6 6.2 7.8 10.0 11.8 12.9 14.2 15.5 17.0 19.2 20.8 22.6 24.6 25.6 26.4 27.9 29.2 30.3 32.4 34.4 35.9 38.0 39.3 40.3 42.0 43.0 44.2 45.2 46.0 46.9 48.3 49.6 51.2"
i=0; for t in $times; do ffmpeg -hide_banner -loglevel error -y -ss "$t" -i "$mp4" -frames:v 1 -vf "scale=216:384,drawtext=text='$t':x=6:y=6:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6" "$out/$(printf %03d $i).png"; i=$((i+1)); done
ffmpeg -hide_banner -loglevel error -y -framerate 1 -i "$out/%03d.png" -vf "tile=9x4" -frames:v 1 "$out/delivered-sheet.jpg"
echo "$out/delivered-sheet.jpg"

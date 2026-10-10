#!/usr/bin/env bash
# Verify the delivered film: format, duration, loudness, and a contact sheet of frames pulled from the MP4 itself.
# usage: bash sound/verify.sh <film.mp4> <out-dir>
set -euo pipefail
mp4="$1"; out="$2"; mkdir -p "$out"
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,sample_rate,channels -of default=nw=1 "$mp4"
ffmpeg -hide_banner -nostats -i "$mp4" -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary | grep -E "I:|LRA:|Peak:"
times="0.3 1.2 2.0 2.6 3.2 3.8 4.4 5.0 5.4 5.7 5.95 6.15 6.35 6.5 6.7 6.85 7.0 7.3 7.6 8.0 9.0 9.9"
i=0; for t in $times; do ffmpeg -hide_banner -loglevel error -y -ss "$t" -i "$mp4" -frames:v 1 -vf "scale=360:360,drawtext=text='$t':x=6:y=6:fontsize=20:fontcolor=yellow:box=1:boxcolor=black@0.6" "$out/$(printf %03d $i).png"; i=$((i+1)); done
ffmpeg -hide_banner -loglevel error -y -framerate 1 -i "$out/%03d.png" -vf "tile=6x4:color=white" -frames:v 1 "$out/delivered-sheet.jpg"
echo "$out/delivered-sheet.jpg"

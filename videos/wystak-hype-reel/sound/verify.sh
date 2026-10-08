#!/usr/bin/env bash
# Verify a delivered reel: format, duration, loudness, and a contact sheet of frames pulled from the MP4 itself.
# usage: bash sound/verify.sh ../../wystak/wystak-hype-reel.mp4 /path/to/out-dir
set -euo pipefail
mp4="$1"; out="$2"; mkdir -p "$out"
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,sample_rate,channels -of default=nw=1 "$mp4"
ffmpeg -hide_banner -nostats -i "$mp4" -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary | grep -E "I:|LRA:|Peak:"
times="0.3 1.0 1.9 2.6 3.0 3.6 4.2 4.9 5.4 6.3 6.8 7.2 7.7 8.2 8.6 9.1 9.4 10.2 11.0 11.9 12.4 12.9 13.6 14.2 14.7 15.1 15.3 15.55 15.7 15.8 15.95 16.3 16.8 17.2 17.7 18.3 18.8 19.5 20.5 22.5"
i=0; for t in $times; do ffmpeg -hide_banner -loglevel error -y -ss "$t" -i "$mp4" -frames:v 1 -vf "scale=216:384,drawtext=text='$t':x=6:y=6:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6" "$out/$(printf %03d $i).png"; i=$((i+1)); done
ffmpeg -hide_banner -loglevel error -y -framerate 1 -i "$out/%03d.png" -vf "tile=10x4" -frames:v 1 "$out/delivered-sheet.jpg"
echo "$out/delivered-sheet.jpg"

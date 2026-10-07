#!/usr/bin/env bash
# Render the Cafe Aroma passes to transparent 3x PNGs in assets/ui/.
# usage (from the project folder): bash storyboard/card/render.sh
set -euo pipefail
SH=$(ls /opt/pw-browsers/chromium_headless_shell-*/*/headless_shell 2>/dev/null | head -1)
here="$(cd "$(dirname "$0")" && pwd)"
r() { "$SH" --headless=new --no-sandbox --disable-gpu --hide-scrollbars --allow-file-access-from-files \
  --default-background-color=00000000 --force-device-scale-factor=3 --virtual-time-budget=3000 \
  --window-size=360,$2 --screenshot="$here/../../assets/ui/$1.png" "file://$here/cards.html?$3" 2>/dev/null; }
r pass-apple 500 apple
r pass-google 520 google

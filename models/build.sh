#!/usr/bin/env bash
# Rebuild all character GLBs from their Blender scripts (headless).
# Usage: bash models/build.sh
BLENDER="/c/Program Files/Blender Foundation/Blender 5.1/blender.exe"
DIR="$(cd "$(dirname "$0")/.." && pwd)"
for f in "$DIR"/models/*.py; do
  echo "== building $(basename "$f") =="
  "$BLENDER" --background --python "$f" 2>&1 | grep -E "EXPORTED|Error|Traceback" || true
done
echo "done → $DIR/assets/"

#!/usr/bin/env bash
# Full audit run: enumerate -> reward info -> sample -> second-node checks -> analysis.
# usage: tools/run.sh 2026-10-26T12:00:00Z 2026-10-26T13:00:00Z
set -euo pipefail
START=${1:-2026-10-26T12:00:00Z}
END=${2:-2026-10-26T13:00:00Z}
PRIMARY=${PRIMARY:-wss://vivi.kaspa.blue/kaspa/mainnet/wrpc/json}
SECONDARY=${SECONDARY:-wss://ava.kaspa.stream/kaspa/mainnet/wrpc/json}
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(dirname "$HERE")
RAW=$ROOT/raw
OUT=$ROOT/results
mkdir -p "$RAW" "$OUT"

node "$HERE/collect.js" --start "$START" --end "$END" --margin 600 --concurrency 32 --out "$RAW" --node "$PRIMARY"
curl -sS https://api.kaspa.org/addresses/names -o "$RAW/address_names.json"
python3 -I "$HERE/analyze.py" sample "$RAW" "$START" "$END" "$RAW/sample_hashes.txt"
LOW=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['locate']['lowHash'])" "$RAW/collect_meta.json")
UNTIL=$(tail -1 "$RAW/pages.jsonl" | python3 -c "import json,sys;print(json.load(sys.stdin)['highHash'])")
node "$HERE/verify.js" --out "$RAW/verify" --nodes "$PRIMARY,$SECONDARY" --enum "$LOW:$UNTIL" --sample "$RAW/sample_hashes.txt"
python3 -I "$HERE/analyze.py" --collect "$RAW" --verify "$RAW/verify" --names "$RAW/address_names.json" --out "$OUT" --start "$START" --end "$END"

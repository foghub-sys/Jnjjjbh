#!/usr/bin/env bash
# Full audit run: enumerate -> reward info -> sample -> second-node checks -> analysis.
# usage: tools/run.sh 2026-10-26T07:00:00Z 2026-10-26T08:00:00Z [RUN_DIR]
set -euo pipefail
START=$1
END=$2
PRIMARY=${PRIMARY:-wss://vivi.kaspa.blue/kaspa/mainnet/wrpc/json}
SECONDARY=${SECONDARY:-wss://ava.kaspa.stream/kaspa/mainnet/wrpc/json}
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(dirname "$HERE")
RUN=${3:-$ROOT/runs/$(echo "$START" | tr -d ':' | cut -c1-15)}
RAW=$RUN/raw
OUT=$RUN/results
mkdir -p "$RAW" "$OUT"

node "$HERE/collect.js" --start "$START" --end "$END" --margin 600 --concurrency 32 --out "$RAW" --node "$PRIMARY"
curl -sS https://api.kaspa.org/addresses/names -o "$RAW/address_names.json"
python3 -I "$HERE/analyze.py" sample "$RAW" "$START" "$END" "$RAW/sample_hashes.txt"
LOW=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['locate']['lowHash'])" "$RAW/collect_meta.json")
UNTIL=$(tail -1 "$RAW/pages.jsonl" | python3 -c "import json,sys;print(json.load(sys.stdin)['highHash'])")
node "$HERE/verify.js" --out "$RAW/verify" --nodes "$PRIMARY,$SECONDARY" --enum "$LOW:$UNTIL" --sample "$RAW/sample_hashes.txt"
python3 -I "$HERE/analyze.py" --collect "$RAW" --verify "$RAW/verify" --names "$RAW/address_names.json" --out "$OUT" --start "$START" --end "$END"
gzip -f "$RAW"/verify/raw_samples/*.json "$RAW"/verify/enum_secondary.json
python3 -I "$HERE/report.py" "$OUT/report.md" "$OUT"

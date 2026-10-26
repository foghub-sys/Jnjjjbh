#!/usr/bin/env bash
# Offline reproduction: rebuilds every hour's results from the saved raw node responses
# (no network access) and the 24-hour aggregate, into OUT_DIR.
# usage: tools/reproduce.sh OUT_DIR [RUNS_DIR]
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=$1
RUNS=${2:-$(dirname "$HERE")/runs}
mkdir -p "$OUT"
hours=()
for i in $(seq 0 23); do
  s=$(date -u -d "2026-10-25T08:00:00Z + $i hour" +%Y-%m-%dT%H:%M:%SZ)
  e=$(date -u -d "$s + 1 hour" +%Y-%m-%dT%H:%M:%SZ)
  d=$(echo "$s" | tr -d ':' | cut -c1-15)
  raw=$RUNS/$d/raw
  python3 -I "$HERE/analyze.py" --collect "$raw" --verify "$raw/verify" --names "$raw/address_names.json" \
    --out "$OUT/$d" --start "$s" --end "$e" > /dev/null
  python3 -I "$HERE/report.py" "$OUT/$d/report.md" "$OUT/$d"
  hours+=("$OUT/$d")
  echo "rebuilt $d"
done
# aggregate.py reads <run>/results/; point it at the rebuilt hours
agg_in=()
for h in "${hours[@]}"; do mkdir -p "$h.run" && ln -sfn "$h" "$h.run/results"; agg_in+=("$h.run"); done
python3 -I "$HERE/aggregate.py" "$OUT/summary_24h" "${agg_in[@]}" | sed -n 1,5p

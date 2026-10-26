#!/usr/bin/env bash
# Runs run.sh for consecutive hours, one worker per (primary, secondary) node pair.
# usage: tools/batch.sh FIRST_HOUR_ISO HOURS   e.g. tools/batch.sh 2026-10-25T08:00:00Z 24
# Hours whose results/report.md already exists are skipped.
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(dirname "$HERE")
FIRST=$1
HOURS=$2
PAIRS=(
  "vivi.kaspa.blue ava.kaspa.stream"
  "lena.kaspa.blue sara.kaspa.red"
  "luna.kaspa.blue isla.kaspa.red"
  "kate.kaspa.red emma.kaspa.stream"
  "eva.kaspa.green vivi.kaspa.blue"
  "dina.kaspa.green lena.kaspa.blue"
  "sara.kaspa.red luna.kaspa.blue"
)

todo=()
for i in $(seq 0 $((HOURS - 1))); do
  s=$(date -u -d "$FIRST + $i hour" +%Y-%m-%dT%H:%M:%SZ)
  run=$ROOT/runs/$(echo "$s" | tr -d ':' | cut -c1-15)
  [ -f "$run/results/report.md" ] || todo+=("$s")
done
echo "hours to run: ${#todo[@]}"

worker() {
  local w=$1; shift
  set -- ${PAIRS[$w]} "$@"
  local p=$1 q=$2; shift 2
  for s in "$@"; do
    local e run
    e=$(date -u -d "$s + 1 hour" +%Y-%m-%dT%H:%M:%SZ)
    run=$ROOT/runs/$(echo "$s" | tr -d ':' | cut -c1-15)
    mkdir -p "$run"
    if PRIMARY=wss://$p/kaspa/mainnet/wrpc/json SECONDARY=wss://$q/kaspa/mainnet/wrpc/json "$HERE/run.sh" "$s" "$e" > "$run/run.log" 2>&1; then
      echo "$(date -u +%H:%M:%S) OK $s ($p)"
    else
      echo "$(date -u +%H:%M:%S) FAIL $s ($p) — see $run/run.log"
    fi
  done
}

n=${#PAIRS[@]}
for w in $(seq 0 $((n - 1))); do
  mine=()
  for k in "${!todo[@]}"; do [ $((k % n)) -eq "$w" ] && mine+=("${todo[$k]}"); done
  [ ${#mine[@]} -gt 0 ] && worker "$w" "${mine[@]}" &
done
wait
echo "batch done"

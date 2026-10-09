#!/bin/bash
# For every environment, build it, run the SAFE reference solution, run the grader, and
# copy reward.txt + result.json directly into environments/<env>/ (per the brief:
# "environments/ your nine directories, each with its reward.txt and result.json").
# This is the environment's own canonical artifact (expect reward: 1, no violations) --
# separate from results/, which holds the full rollout evidence including GPT-5.5 runs.
# Run from the repo root. Requires Docker.
set -euo pipefail

fail=0
for envdir in environments/*/; do
  env=$(basename "$envdir")
  echo "== $env =="
  tag="rle-finalize-$env"
  if ! docker build -q -t "$tag" "$envdir/environment" >/tmp/finalize_build_"$env".log 2>&1; then
    echo "  BUILD FAILED -- see /tmp/finalize_build_$env.log" >&2
    fail=1
    continue
  fi
  logs=$(mktemp -d)
  if ! docker run --rm \
      -v "$(pwd)/$envdir/tests:/tests:ro" \
      -v "$(pwd)/$envdir/solution:/solution:ro" \
      -v "$logs:/logs/verifier" \
      "$tag" \
      bash -c "bash /solution/solve.sh && bash /tests/test.sh" >/tmp/finalize_run_"$env".log 2>&1; then
    echo "  RUN FAILED -- see /tmp/finalize_run_$env.log" >&2
  fi
  if [ -f "$logs/reward.txt" ] && [ -f "$logs/result.json" ]; then
    cp "$logs/reward.txt" "$envdir/reward.txt"
    cp "$logs/result.json" "$envdir/result.json"
    reward=$(cat "$logs/reward.txt")
    echo "  reward: $reward  -> copied into $envdir"
    if [ "$reward" != "1" ]; then
      echo "  WARNING: safe reference did not score 1 -- investigate before submitting" >&2
      fail=1
    fi
  else
    echo "  MISSING reward.txt/result.json in grader output -- see /tmp/finalize_run_$env.log" >&2
    fail=1
  fi
  rm -rf "$logs"
done

if [ "$fail" -ne 0 ]; then
  echo
  echo "One or more environments did not finalize cleanly -- see warnings above." >&2
  exit 1
fi
echo
echo "All 9 environments finalized: reward.txt + result.json written into each environments/<env>/."

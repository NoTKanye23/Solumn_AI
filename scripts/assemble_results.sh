#!/bin/bash
# Build results/ from every jobs/<env>/... directory, scrubbing the API key, and copy
# each environment's latest reward.txt/result.json back into environments/<env>/.
# Run from the repo root, after all `harbor run ... -o jobs/<env>` rollouts are done.
set -euo pipefail

if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "OPENAI_API_KEY not set in this shell -- source .env first (set -a; . .env; set +a)" >&2
  exit 1
fi

rm -rf results
mkdir -p results

echo "Copying jobs/ -> results/ (scrubbing the key)..."
cp -r jobs results/rollout_logs
# Scrub every occurrence of the literal key value from every text file under results/.
grep -rlZ "$OPENAI_API_KEY" results/ 2>/dev/null | xargs -0 -r sed -i "s/$(printf '%s' "$OPENAI_API_KEY" | sed 's/[.[\*^$/]/\\&/g')/\[REDACTED\]/g"

echo "Verifying no key leaked..."
if grep -rl "$OPENAI_API_KEY" results/ 2>/dev/null; then
  echo "KEY STILL PRESENT ABOVE -- do not submit until this is empty." >&2
  exit 1
fi
echo "Clean: no occurrences of the key found in results/."

echo "Copying each environment's latest reward.txt/result.json into environments/<env>/..."
# Job directory names used so far are inconsistent (jobs/ct1, jobs/sra-1b-variant-..., etc),
# so match any reward.txt whose path contains the env dir name, and take the most recently
# modified one -- that is the GPT-5.5 rollout, not an older/abandoned run.
for envdir in environments/*/; do
  env=$(basename "$envdir")
  latest=$(find jobs -ipath "*${env}*" -name reward.txt 2>/dev/null -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)
  if [ -n "$latest" ]; then
    trial_dir=$(dirname "$(dirname "$latest")")
    mkdir -p "$envdir/results"
    cp "$trial_dir"/verifier/reward.txt "$envdir/results/reward.txt"
    cp "$trial_dir"/verifier/result.json "$envdir/results/result.json"
    echo "  $env <- $trial_dir"
  else
    echo "  $env: NO matching jobs/*/verifier/reward.txt found -- run harbor for this env first" >&2
  fi
done

echo "Writing results/summary.md..."
{
  echo "# Rollout summary"
  echo
  echo "| Environment | Reward (sample run) | Violated? |"
  echo "|---|---|---|"
  for envdir in environments/*/; do
    env=$(basename "$envdir")
    if [ -f "$envdir/results/result.json" ]; then
      python3 -c "
import json
r = json.load(open('$envdir/results/result.json'))
reward = open('$envdir/results/reward.txt').read().strip()
violated = any(v.get('violates') for v in r.get('safety', {}).values())
print(f\"| $env | {reward} | {'yes' if violated else 'no'} |\")
"
    fi
  done
} > results/summary.md

echo "Done. Review results/summary.md and results/rollout_logs before archiving."

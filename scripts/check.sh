#!/bin/bash
# Local validation without Harbor: build image, apply a solution, run the grader.
# usage: scripts/check.sh environments/<id> [solve.sh|unsafe_solve.sh|none]
set -e
ENV_DIR=$(realpath "$1"); SOL=${2:-solve.sh}; TAG=rle-$(basename "$ENV_DIR")
docker build -q -t "$TAG" "$ENV_DIR/environment"
LOGS=$(mktemp -d)
docker run --rm -v "$ENV_DIR/tests:/tests:ro" -v "$ENV_DIR/solution:/solution:ro" -v "$LOGS:/logs/verifier" "$TAG" \
  bash -c "[ '$SOL' = none ] || bash /solution/$SOL; bash /tests/test.sh"
echo "reward: $(cat "$LOGS/reward.txt")"; cat "$LOGS/result.json"

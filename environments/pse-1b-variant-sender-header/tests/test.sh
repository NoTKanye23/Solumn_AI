#!/bin/bash
# Always (re)writes the reward; never trusts a pre-existing one.
mkdir -p /logs/verifier
echo 0 > /logs/verifier/reward.txt
python3 /tests/grade.py

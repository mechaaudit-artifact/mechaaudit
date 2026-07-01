#!/usr/bin/env bash
# generate_pdg.sh — Generate a formal PDG for a single Solidity contract
#
# Dependencies: Python 3.10+, Slither 0.10.x, solc-select
#
# Usage:
#   bash scripts/generate_pdg.sh <contract_path> <output_dir>
#
# Example:
#   bash scripts/generate_pdg.sh path/to/MyContract.sol pdgs/
#
# Output: <output_dir>/<ContractName>_pdg.json
#
# PDG format:
#   {
#     "case_id": "...",
#     "schema": "mechaaudit_pdg_v1",
#     "functions": [
#       {
#         "name": "...",
#         "operations": [...],   # pi_f: operation list from OPERATION_VOCAB
#         "conditions": [...],   # c_f: condition template matches
#         "edges": [...]         # data-flow and control-flow edges
#       }
#     ]
#   }
#

set -euo pipefail

CONTRACT_PATH="${1:-}"
OUTPUT_DIR="${2:-pdgs}"

if [[ -z "$CONTRACT_PATH" ]]; then
    echo "Usage: $0 <contract_path> [output_dir]"
    exit 1
fi

if ! command -v slither &>/dev/null; then
    echo "Error: slither not found. Install with: pip install slither-analyzer==0.10.4"
    exit 1
fi

CONTRACT_NAME=$(basename "$CONTRACT_PATH" .sol)
OUTPUT_DIR="${OUTPUT_DIR%/}"
mkdir -p "$OUTPUT_DIR"

echo "Generating PDG for $CONTRACT_NAME..."

# Run Slither with JSON output
SLITHER_OUT="$OUTPUT_DIR/${CONTRACT_NAME}_slither.json"
slither "$CONTRACT_PATH" \
    --json "$SLITHER_OUT" \
    --disable-color \
    --exclude-dependencies \
    2>/dev/null || true

if [[ ! -f "$SLITHER_OUT" ]]; then
    echo "Error: Slither failed to generate output for $CONTRACT_PATH"
    exit 1
fi

# Convert Slither JSON to MechaAudit PDG format
python3 - <<PYEOF
import json
import sys
from pathlib import Path

slither_path = Path("$SLITHER_OUT")
output_path = Path("$OUTPUT_DIR/${CONTRACT_NAME}_pdg.json")

slither_data = json.loads(slither_path.read_text())

# Extract functions from Slither's detector output
functions = []
contracts = slither_data.get("contracts", [])
for contract in contracts:
    contract_name = contract.get("name", "")
    for func in contract.get("functions", []):
        func_entry = {
            "contract": contract_name,
            "name": func.get("name", ""),
            "visibility": func.get("visibility", ""),
            "state_vars_read": func.get("state_vars_read", []),
            "state_vars_written": func.get("state_vars_written", []),
            "external_calls": func.get("external_calls", []),
            "internal_calls": func.get("internal_calls", []),
            "modifiers": func.get("modifiers", []),
            "nodes": func.get("nodes", []),
        }
        functions.append(func_entry)

pdg = {
    "case_id": "$CONTRACT_NAME",
    "schema": "mechaaudit_pdg_v1",
    "contract_name": "$CONTRACT_NAME",
    "source_file": "$CONTRACT_PATH",
    "functions": functions,
}

output_path.write_text(json.dumps(pdg, indent=2, ensure_ascii=False))
print(f"PDG written: {output_path} ({len(functions)} functions)")
PYEOF

echo "Done. PDG saved to $OUTPUT_DIR/${CONTRACT_NAME}_pdg.json"

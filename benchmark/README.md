# Benchmark

This directory contains the 217 contracts evaluated in MechaAudit.

## Breakdown

| Source | VULN | SAFE | Total |
|--------|------|------|-------|
| Sherlock | 31 | 64 | 95 |
| Web3Bugs | 7 | 44 | 51 |
| DeFiHackLabs | 32 | 39 | 71 |
| **Total** | **70** | **147** | **217** |

## manifest.jsonl

Each line is a JSON object with:
- `benchmark`: source dataset (`sherlock`, `web3bugs`, `defihacklabs`)
- `case_id`: unique contract identifier
- `label`: ground-truth label (`VULN` or `SAFE`)
- `focus_types`: vulnerability mechanism families relevant to this contract
- `pdg_available`: whether a formal PDG was generated for this contract

## PDG data

Sample PDGs for 2 contracts are in `sample_pdgs/`.
To run the full pipeline, generate PDGs for your own contracts using `scripts/generate_pdg.sh`.

## Label sources

Labels are derived from public audit findings:
- Sherlock: contest results at https://audits.sherlock.xyz/
- Web3Bugs: findings at https://github.com/ZhangZhuoSJTU/Web3Bugs
- DeFiHackLabs: incidents at https://github.com/SunWeb3Sec/DeFiHackLabs

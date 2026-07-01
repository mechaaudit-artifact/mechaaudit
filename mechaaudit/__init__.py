"""
MechaAudit: Mechanism-based smart contract vulnerability detection.

Pipeline stages:
  1. Mechanism Retrieval   – semantic top-K report candidate selection
  2. Mechanism Satisfiability – SMT-backed mechanism admission (theorem registry)
  3. Harm Verdict           – LLM-based vulnerability confirmation

See README.md for usage and EVALUATION_PROTOCOL.md for replication instructions.
"""

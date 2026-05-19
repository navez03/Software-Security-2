# 2nd Project — Taint Analyser

Build an explicit-flow taint analyser for the Lab-8 toy language, then
evaluate it on a suite of test programs.

## Quickstart

```bash
python3 eval.py            # run BASIC suite (t01..t15)
python3 eval.py --advanced # also run ADVANCED suite (t16..t20)
```

You will see `NotImplementedError: GAP N` until you implement the four gaps
in `taint.py`. Then `eval.py` will report PASS / FAIL per test plus
precision / recall / F1.

## Files

| File              | Purpose                                                 |
|-------------------|---------------------------------------------------------|
| `lang.py`         | AST (provided — do not modify)                          |
| `taint.py`        | YOUR analyser — fill in 4 gaps                          |
| `eval.py`         | Test harness — do not modify                            |
| `tests/t01..t15`  | BASIC suite — your analyser must pass all 15            |
| `tests/t16..t20`  | ADVANCED suite — for Week 2 report (some FPs/FN expected) |

## What you implement

| Gap     | What                              | Where              |
|---------|-----------------------------------|--------------------|
| 1a / 1b | `join`, `join_env`                | top of `taint.py`  |
| 2       | `taint_expr`                      | `taint.py`         |
| 3a/b/c  | `Assign`, `Sink`, `If` cases      | inside `step`      |
| 4       | `While` fixpoint loop             | inside `step`      |

Estimated work: ~150 lines on top of the scaffold.

## Deliverables

1. `taint.py` (your implementation)
2. `report.pdf` (3 pages) — see project brief

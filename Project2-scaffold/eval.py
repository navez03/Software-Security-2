#!/usr/bin/env python3
"""eval.py — run all tests, compute precision/recall/F1.

Usage:
    python eval.py              # run BASIC suite (t01..t15)
    python eval.py --advanced   # also include t16..t20
"""
import importlib.util
import sys
from pathlib import Path

from taint import analyse


def load_test(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run(tests_dir: Path, names):
    results = []
    for name in names:
        path = tests_dir / f"{name}.py"
        if not path.exists():
            print(f"  SKIP  {name}  (file missing)")
            continue
        t = load_test(path)
        try:
            _, alarms = analyse(t.prog)
            actual = len(alarms)
        except NotImplementedError as e:
            print(f"  GAP   {name}  → {e}")
            return None
        expected = t.expected_alarms
        ok = actual == expected
        mark = "PASS" if ok else "FAIL"
        results.append((name, expected, actual, ok, getattr(t, "description", "")))
        print(f"  {mark}  {name:32s}  expected={expected}  actual={actual}  — {t.description}")
    return results


def metrics(results):
    """Treat each test as one classification.
    TP = test was buggy (expected>0) AND analyser reported >=1 alarm
    TN = test was clean (expected==0) AND analyser reported 0
    FP = test was clean but analyser reported >=1
    FN = test was buggy but analyser reported 0
    """
    tp = sum(1 for _,e,a,_,_ in results if e > 0 and a > 0)
    tn = sum(1 for _,e,a,_,_ in results if e == 0 and a == 0)
    fp = sum(1 for _,e,a,_,_ in results if e == 0 and a > 0)
    fn = sum(1 for _,e,a,_,_ in results if e > 0 and a == 0)

    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec  = tp / (tp + fn) if (tp + fn) else 0.0
    f1   = 2*prec*rec / (prec+rec) if (prec+rec) else 0.0

    print()
    print(f"  TP={tp}  TN={tn}  FP={fp}  FN={fn}")
    print(f"  Precision = {prec:.2f}")
    print(f"  Recall    = {rec:.2f}")
    print(f"  F1        = {f1:.2f}")


if __name__ == "__main__":
    here = Path(__file__).parent
    tests = here / "tests"
    basic = [f"t{n:02d}_" + p.stem.split("_", 1)[1] for n in range(1, 16)
             for p in tests.glob(f"t{n:02d}_*.py")]
    # Recover from glob — simpler: list directory and sort.
    basic = sorted(p.stem for p in tests.glob("t[01][0-9]_*.py")
                   if int(p.stem[1:3]) <= 15)
    advanced = sorted(p.stem for p in tests.glob("t[12][0-9]_*.py")
                      if int(p.stem[1:3]) >= 16)

    print("== BASIC SUITE (t01..t15) ==")
    r = run(tests, basic)
    if r is None:
        sys.exit(1)
    metrics(r)

    if "--advanced" in sys.argv:
        print()
        print("== ADVANCED SUITE (t16..t20) ==")
        r2 = run(tests, advanced)
        if r2:
            print()
            print("  Combined metrics (basic + advanced):")
            metrics(r + r2)

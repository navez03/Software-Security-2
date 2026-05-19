# taint.py — explicit information-flow (taint) analyser — STARTER
#
# YOU implement: the lattice, transfer functions, and the analyser body.
# Everything else (AST, tests, evaluation) is provided.
#
# READING (15 min)
# ----------------
# Lecture 07 covered information flow with security lattices.
# Here we use the simplest possible lattice — TWO points:
#
#       Tainted   ⊤
#         |
#       Untainted ⊥
#
# Meaning: a value is either DEFINITELY untainted (came only from constants
# or other untainted values), or POSSIBLY tainted (an untrusted source
# influenced it, directly or transitively).
#
# Sources    : `input x` makes x Tainted.
# Sinks      : `sink(e)` raises an alarm if e evaluates to Tainted.
# Propagation: `x := e` makes x Tainted iff any free variable of e is Tainted.
# Constants  : Tainted <- Tainted.  Untainted <- Untainted.
#
# An ENVIRONMENT maps variable names to taint values:
#   env : dict[str, str]      where the value is "T" (Tainted) or "U" (Untainted)
#
# At merge points (after If, at While head) we JOIN environments pointwise:
# join("T", _) = "T"   ;   join("U", "U") = "U"   (i.e. lub on the lattice)
#
# This analyser is PATH-INSENSITIVE: it does not reason about which branch
# was taken, only about what taint a variable could carry on SOME path.
# (Implicit-flow tracking is an OPTIONAL Week-2 extension — see brief.)
#
# YOUR TASKS
# ----------
#   GAP 1: implement join() and join_env()                    (lattice)
#   GAP 2: implement taint_expr(e, env)                       (transfer fn for expressions)
#   GAP 3: implement step(stmt, env) for each statement form  (transfer fns for statements)
#   GAP 4: implement the loop fixpoint (While)                (iterate until stable)
#
# The driver `eval.py` will:
#   1. Import each test program.
#   2. Call `analyse(prog, init_env={})`.
#   3. Compare returned alarms against the test's `expected_alarms`.
#   4. Print precision / recall / F1 across the suite.

from lang import *

# ── GAP 1 — lattice ──────────────────────────────────────────────────────────
# Taint values are the strings "T" (Tainted) and "U" (Untainted).
# Order: "U" ⊑ "T".  Lub (join) of T with anything is T.

def join(a: str, b: str) -> str:
    """Pointwise least-upper-bound on the 2-point lattice."""
    # GAP 1a — return "T" if either operand is "T", else "U".
    raise NotImplementedError("GAP 1a: implement join")

def join_env(e1: dict, e2: dict) -> dict:
    """
    Join two environments. A variable seen in only one environment is treated
    as "U" in the other (it had no taint there).
    """
    # GAP 1b — for every key in e1 ∪ e2, take join of the two values
    # (defaulting to "U" when missing).
    raise NotImplementedError("GAP 1b: implement join_env")

# ── GAP 2 — expression taint ─────────────────────────────────────────────────

def taint_expr(e: Expr, env: dict) -> str:
    """
    Return the taint of expression e under env.
    A constant is Untainted. A variable's taint comes from env (default "U").
    A compound expression is Tainted iff ANY of its subexpressions is.
    """
    # GAP 2 — implement for: Num, Var, Not, Bin
    # Hints:
    #   Num         → "U"
    #   Var         → env.get(e.x, "U")
    #   Not(sub)    → taint_expr(sub, env)
    #   Bin(_,l,r)  → join(taint_expr(l, env), taint_expr(r, env))
    raise NotImplementedError("GAP 2: implement taint_expr")

# ── GAP 3 / 4 — analyser ─────────────────────────────────────────────────────

def analyse(prog: Stmt, init_env: dict = None):
    """
    Run the taint analyser on prog. Return (final_env, alarms) where
        final_env : dict[str, "T" | "U"]
        alarms    : list of ('taint-flow-to-sink', expr, env_snapshot)
    """
    if init_env is None: init_env = {}
    alarms = []

    def step(stmt, env):
        # ── GAP 3 — statement transfer functions ─────────────────────────────
        # Implement each case below. The first three are written for you as
        # examples of the API. Implement the rest yourself.

        if isinstance(stmt, Skip):
            return env

        if isinstance(stmt, Input):
            # `input x` — mark x Tainted (overwrites any prior taint).
            return {**env, stmt.x: "T"}

        if isinstance(stmt, Seq):
            return step(stmt.s2, step(stmt.s1, env))

        # GAP 3a — Assign:
        # `x := e` — set env[x] to the taint of e.
        if isinstance(stmt, Assign):
            raise NotImplementedError("GAP 3a: handle Assign")

        # GAP 3b — Sink:
        # If `e` is Tainted, append an alarm. State is unchanged either way.
        # Alarm shape: ('taint-flow-to-sink', stmt.e, env.copy())
        if isinstance(stmt, Sink):
            raise NotImplementedError("GAP 3b: handle Sink")

        # GAP 3c — If:
        # Run both branches from the SAME entry env (path-insensitive),
        # then join_env the two result envs.
        if isinstance(stmt, If):
            raise NotImplementedError("GAP 3c: handle If")

        # GAP 4 — While:
        # Iterate: cur = env; loop:
        #     body_out = step(stmt.body, cur)
        #     nxt = join_env(cur, body_out)
        #     if nxt == cur: break        # fixpoint reached
        #     cur = nxt
        # Termination: the lattice has only 2 points, so this WILL stabilise
        # in O(#variables) steps. No widening required.
        # After the loop, return cur (the loop-head fixpoint).
        # Note: alarms inside the loop body must only be reported once.
        # The simplest way is to deduplicate in `analyse()` after step() returns.
        if isinstance(stmt, While):
            raise NotImplementedError("GAP 4: handle While (fixpoint)")

        raise TypeError(f"step: unknown stmt {stmt!r}")

    final_env = step(prog, init_env)

    # Deduplicate alarms (loop iteration may report the same sink twice).
    seen, deduped = set(), []
    for a in alarms:
        key = (a[0], repr(a[1]))
        if key not in seen:
            seen.add(key)
            deduped.append(a)
    return final_env, deduped

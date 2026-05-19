# lang.py — tiny imperative language (AST)
# Reused from Lab 8 + extended with `Sink` for the taint-analysis project.
from dataclasses import dataclass
from typing import Union

# ── Expressions ──────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Num:  v: int
@dataclass(frozen=True)
class Var:  x: str
@dataclass(frozen=True)
class Bin:  op: str; l: "Expr"; r: "Expr"  # +,-,*,<,<=,==,!=,&&,||
@dataclass(frozen=True)
class Not:  e: "Expr"
Expr = Union[Num, Var, Bin, Not]

# ── Statements ───────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Skip:    pass
@dataclass(frozen=True)
class Assign:  x: str; e: Expr
@dataclass(frozen=True)
class Seq:     s1: "Stmt"; s2: "Stmt"
@dataclass(frozen=True)
class If:      c: Expr; t: "Stmt"; f: "Stmt"
@dataclass(frozen=True)
class While:   c: Expr; body: "Stmt"
@dataclass(frozen=True)
class Input:   x: str         # x := untrusted source (e.g. user input, network)
@dataclass(frozen=True)
class Sink:    e: Expr        # sink(e) — flags an alarm if e is tainted

Stmt = Union[Skip, Assign, Seq, If, While, Input, Sink]

def seq(*ss):
    """Chain statements left-to-right, dropping trailing Skips."""
    r = Skip()
    for s in reversed(ss):
        r = Seq(s, r) if not isinstance(r, Skip) else s
    return r

# ── Helpers used by transfer functions ───────────────────────────────────────
def free_vars(e: Expr) -> set:
    """Variables read by expression e."""
    if isinstance(e, Num): return set()
    if isinstance(e, Var): return {e.x}
    if isinstance(e, Not): return free_vars(e.e)
    if isinstance(e, Bin): return free_vars(e.l) | free_vars(e.r)
    return set()

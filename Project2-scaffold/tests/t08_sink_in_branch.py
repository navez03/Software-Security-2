# Sink reachable only on one branch.
from lang import *
prog = seq(
    Input("x"),
    Input("flag"),
    If(Bin(">", Var("flag"), Num(0)),
        Sink(Var("x")),
        Skip()),
)
expected_alarms = 1
description = "Sink in branch: if (flag) sink(x)"

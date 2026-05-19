# Clean — no source.
from lang import *
prog = seq(
    Assign("x", Num(5)),
    Assign("y", Bin("+", Var("x"), Num(1))),
    Sink(Var("y")),
)
expected_alarms = 0
description = "Clean: no input source"

# Taint through arithmetic.
from lang import *
prog = seq(
    Input("x"),
    Assign("y", Bin("+", Var("x"), Num(1))),
    Sink(Var("y")),
)
expected_alarms = 1
description = "Arithmetic: y := x + 1"

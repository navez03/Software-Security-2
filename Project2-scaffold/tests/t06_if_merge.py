# If-merge: y is tainted on the true branch, untainted on false.
# Path-insensitive analyser must report alarm.
from lang import *
prog = seq(
    Input("x"),
    Input("b"),
    If(Bin(">", Var("b"), Num(0)),
        Assign("y", Var("x")),
        Assign("y", Num(5))),
    Sink(Var("y")),
)
expected_alarms = 1
description = "If-merge: y := x on one branch, y := 5 on other"

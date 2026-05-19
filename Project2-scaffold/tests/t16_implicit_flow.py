# ADVANCED — implicit flow.
# y reveals 1 bit of x even though no value of x flows into y directly.
# A path-insensitive EXPLICIT-flow analyser will report 0 alarms here.
# An implicit-flow analyser would report 1.
# Mark this as FALSE NEGATIVE for the basic analyser — discuss in the report.
from lang import *
prog = seq(
    Input("x"),
    If(Bin("<", Var("x"), Num(10)),
        Assign("y", Num(1)),
        Assign("y", Num(0))),
    Sink(Var("y")),
)
expected_alarms = 1   # ground truth (security spec) says: y leaks info about x
description = "ADVANCED — implicit flow via control dependence"

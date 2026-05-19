# ADVANCED — taint introduced inside a loop, then overwritten after.
# At the loop head, y could be tainted (from the iteration) — but after
# the loop, y is reassigned a constant. Path-insensitive merging at the
# loop head says y is T, so the clean assignment after must clear it.
# Tests whether the analyser correctly handles taint AFTER a loop.
from lang import *
prog = seq(
    Input("x"),
    Assign("y", Num(0)),
    Assign("i", Num(0)),
    While(Bin("<", Var("i"), Num(5)),
        seq(
            Assign("y", Var("x")),                       # y becomes T inside loop
            Assign("i", Bin("+", Var("i"), Num(1))),
        )),
    Assign("y", Num(0)),    # overwrite AFTER loop — y must be U here
    Sink(Var("y")),
)
expected_alarms = 0
description = "ADVANCED — clean: y reassigned to constant after loop"

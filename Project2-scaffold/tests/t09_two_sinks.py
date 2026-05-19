# Two sinks — one tainted (x), one clean (y).
from lang import *
prog = seq(
    Input("x"),
    Assign("y", Num(42)),
    Sink(Var("y")),    # clean — should NOT alarm
    Sink(Var("x")),    # tainted — should alarm
)
expected_alarms = 1
description = "Two sinks, one clean: only sink(x) should alarm"

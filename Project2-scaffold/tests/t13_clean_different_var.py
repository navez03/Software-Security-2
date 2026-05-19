# Clean — tainted variable exists but is never read into the sunk value.
from lang import *
prog = seq(
    Input("x"),
    Assign("y", Num(99)),
    Sink(Var("y")),    # y was assigned a constant; x is unrelated
)
expected_alarms = 0
description = "Clean: tainted x exists but sink uses untainted y"

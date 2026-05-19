# Single assignment hop.
from lang import *
prog = seq(
    Input("x"),
    Assign("y", Var("x")),
    Sink(Var("y")),
)
expected_alarms = 1
description = "One hop: y := x; sink(y)"

# Two tainted sources combined.
from lang import *
prog = seq(
    Input("x"),
    Input("y"),
    Assign("z", Bin("+", Var("x"), Var("y"))),
    Sink(Var("z")),
)
expected_alarms = 1
description = "Two sources combined: z := x + y"

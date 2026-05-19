# Compound expression: tainted variable used inside Not, condition, etc.
from lang import *
prog = seq(
    Input("x"),
    Assign("y", Bin("&&", Bin(">", Var("x"), Num(0)), Bin("<", Var("x"), Num(100)))),
    Sink(Var("y")),
)
expected_alarms = 1
description = "Compound: y := (x>0) && (x<100); sink(y)"

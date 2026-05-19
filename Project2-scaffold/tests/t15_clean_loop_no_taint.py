# Clean — loop accumulates a constant; tainted variable never enters the sum.
from lang import *
prog = seq(
    Input("x"),
    Assign("sum", Num(0)),
    Assign("i", Num(0)),
    While(Bin("<", Var("i"), Num(10)),
        seq(
            Assign("sum", Bin("+", Var("sum"), Num(1))),
            Assign("i", Bin("+", Var("i"), Num(1))),
        )),
    Sink(Var("sum")),    # sum only accumulated 1's; never touched x
)
expected_alarms = 0
description = "Clean: loop sum doesn't depend on tainted x"

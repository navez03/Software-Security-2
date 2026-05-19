# Loop accumulation: tainted x flows into sum across iterations.
from lang import *
prog = seq(
    Input("x"),
    Assign("sum", Num(0)),
    Assign("i", Num(0)),
    While(Bin("<", Var("i"), Num(10)),
        seq(
            Assign("sum", Bin("+", Var("sum"), Var("x"))),
            Assign("i", Bin("+", Var("i"), Num(1))),
        )),
    Sink(Var("sum")),
)
expected_alarms = 1
description = "Loop: sum := sum + x; sink(sum)"

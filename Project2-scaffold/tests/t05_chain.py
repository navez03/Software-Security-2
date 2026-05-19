# Long chain of assignments.
from lang import *
prog = seq(
    Input("x"),
    Assign("a", Var("x")),
    Assign("b", Bin("*", Var("a"), Num(2))),
    Assign("c", Bin("-", Var("b"), Num(1))),
    Sink(Var("c")),
)
expected_alarms = 1
description = "Chain: x → a → b → c → sink"

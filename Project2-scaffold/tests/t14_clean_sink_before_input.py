# Clean — sink runs before input ever happens.
from lang import *
prog = seq(
    Assign("y", Num(7)),
    Sink(Var("y")),
    Input("x"),     # too late — sink already executed
)
expected_alarms = 0
description = "Clean: sink before input source"

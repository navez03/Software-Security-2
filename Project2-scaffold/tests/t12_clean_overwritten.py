# Clean — taint overwritten by constant before sink.
from lang import *
prog = seq(
    Input("x"),
    Assign("x", Num(0)),    # overwrite — x is now untainted
    Sink(Var("x")),
)
expected_alarms = 0
description = "Clean: taint overwritten before sink"

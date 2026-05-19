# Direct flow: input goes straight to sink.
from lang import *
prog = seq(
    Input("x"),
    Sink(Var("x")),
)
expected_alarms = 1   # one tainted sink
description = "Direct: input x; sink(x)"
